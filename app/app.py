# ui.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from pathlib import Path
from datetime import datetime
from werkzeug.utils import secure_filename
from bson import ObjectId
from db.sql.db import get_db_connection
from db.sql.initDB import initialize_database
from db.nosql.nosql import MongoCRUD

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # needed for flash messages
app.config["MONGO_URI"] = "mongodb://localhost:27017/allergen-free-recipes"
mongo_crud = MongoCRUD()       # NoSQL CRUD object

db_path = Path(__file__).resolve().parents[1] / "allergen-free-recipes.db"

# Initialize if DB does not exist
if not db_path.exists():
    initialize_database(db_path=db_path)

# Location to stored uploaded review medias
APP_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = APP_DIR / "static" / "uploads"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)    # create folder if it does not exist
ALLOWED_IMAGE_EXT = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
ALLOWED_VIDEO_EXT = {'mp4', 'mov', 'avi', 'mkv', 'webm', 'ogg'}

app.config['UPLOAD_FOLDER'] = str(UPLOAD_FOLDER)


def allowed_file(filename, allowed_ext):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_ext


# File size
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  


# track per-user allergies
ALL_ALLERGENS = [
    'shellfish', 'eggs', 'cow’s milk',
    'nuts', 'grains', 'soy',
    'wheat', 'sesame', 'fish'
]
USER_ALLERGIES = {}  # username -> list of selected allergens
@app.route('/edit_allergies', methods=['GET','POST'])
def edit_allergies():
    user = session.get('username')
    if not user:
        flash('Please log in first.', 'warning')
        return redirect(url_for('index'))
    if request.method == 'POST':
        # grab all the checked boxes
        selected = request.form.getlist('allergies')
        USER_ALLERGIES[user] = selected
        return redirect(url_for('homepage'))
    # GET → show the form with their current choices
    current = USER_ALLERGIES.get(user, [])
    return render_template('allergies.html',
                           all_allergens=ALL_ALLERGENS,
                           user_allergies=current)

# USERS
@app.route('/')
def index():
    return render_template('login.html')

# LOGIN
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    print("[DEBUG] Connecting to SQL...")
    conn = get_db_connection()
    print("[DEBUG] Connection established.")
    cursor = conn.cursor()
    print("[DEBUG] Executing SELECT...")
    cursor.execute(
        "SELECT user_id, user_password FROM user_profile WHERE user_name = ?",
        (username,)
    )
    row = cursor.fetchone()
    print("[DEBUG] Query done.")
    cursor.close()
    conn.close()
    if row and row['user_password'] == password:
        session['user_id']   = row['user_id']
        session['username'] = username
        return redirect(url_for('homepage'))
    else:
        flash('Invalid username or password', 'danger')
        return redirect(url_for('index'))
    
# Registration
    
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        if request.method == 'POST':
            uname  = request.form['username'].strip()
            pwd    = request.form['password']
            cpwd   = request.form['confirm_password']
            if pwd != cpwd:
                flash('Passwords must match', 'danger')
                return redirect(url_for('register'))
            
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
                """
                INSERT INTO user_profile (
                    user_name, 
                    user_password
                ) VALUES (?,?)
                """,
                (uname, pwd)
            )
        conn.commit()
        cur.close()
        conn.close()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('index'))
    return render_template('register.html')
# Profile view (Read)
@app.route('/profile', methods=['GET'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    uid = session['user_id']
    conn = get_db_connection()
    cur = conn.cursor()
    # fetch the user row
    cur.execute("SELECT * FROM user_profile WHERE user_id=?", (uid,))
    user = cur.fetchone()
    # fetch just the allergen names
    cur.execute("""
        SELECT a.allergen_name
        FROM user_allergen ua
        JOIN allergen a ON ua.allergen_id = a.allergen_id
        WHERE ua.user_id = ?
    """, (uid,))
    allergens = [ r['allergen_name'] for r in cur.fetchall() ]
    cur.close()
    conn.close()
    # map each allergen to a Font-Awesome icon and a Bootstrap color
    allergen_icons = {
        'Milk':            'fas fa-glass-whiskey',
        'Eggs':            'fas fa-egg',
        'Fish':            'fas fa-fish',
        'Crustacean Shellfish': 'fas fa-shrimp',
        'Tree Nuts':       'fas fa-acorn',
        'Peanuts':         'fas fa-peanut',
        'Wheat':           'fas fa-bread-slice',
        'Soybean':         'fas fa-seedling',
        'Mustard':         'fas fa-seedling',
        'Celery':          'fas fa-leaf',
        # …add more as needed…
    }
    badge_colors = {
        'Milk':            'primary',
        'Eggs':            'warning',
        'Fish':            'info',
        'Crustacean Shellfish': 'danger',
        'Tree Nuts':       'dark',
        'Peanuts':         'secondary',
        'Wheat':           'success',
        'Soybean':         'light',
        'Mustard':         'warning',
        'Celery':          'success',
        # …etc…
    }
    return render_template('profile.html',
                           user=user,
                           allergens=allergens,
                           allergen_icons=allergen_icons,
                           badge_colors=badge_colors)
# Edit profile (Update)
@app.route('/profile/edit', methods=['GET','POST'])
def edit_profile():
    uid = session.get('user_id')
    if not uid:
        flash("Please log in first.", "warning")
        return redirect(url_for('index'))
    conn = get_db_connection()
    cur  = conn.cursor(dictionary=True)
    if request.method == 'POST':
        #fields
        new_height = request.form.get('height') or None
        new_weight = request.form.get('weight') or None
        new_gender = request.form.get('gender') or None
        new_age = request.form.get('age') or None
        new_budget = request.form.get('caloric_budget') or None
        new_level = request.form.get('activity_level') or None

        
        cur.execute(
        """
        UPDATE user_profile
        SET height=?, weight=?, gender=?, age=?, caloric_budget=?, activity_level=?
        WHERE user_id=?
        """,
        (new_height, new_weight, new_gender, new_age, new_budget, new_level, uid)
    )
        
        #update allergens
        selected = request.form.getlist('allergens')
        cur.execute("DELETE FROM user_allergen WHERE user_id = ?", (uid,))
        for alg_id in selected:
            cur.execute(
                "INSERT INTO user_allergen (user_id, allergen_id) VALUES (?, ?)",
                (uid, alg_id)
            )

        # 4) commit once, then close
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('profile'))

    # GET
    cur.execute("""
      SELECT age, gender, caloric_budget, height, weight, activity_level
      FROM user_profile
      WHERE user_id = ?
    """, (uid,))
    user = cur.fetchone()
    # list all possible allergens
    cur.execute("SELECT allergen_id, allergen_name FROM allergen")
    # list of dicts
    all_allergens = cur.fetchall()  
    # fetch this user’s currently selected IDs
    cur.execute("SELECT allergen_id FROM user_allergen WHERE user_id = ?", (uid,))
    current = {str(r['allergen_id']) for r in cur.fetchall()}
    cur.close()
    conn.close()
    return render_template(
      'edit_profile.html',
      user=user,
      all_allergens=all_allergens,
      current_allergens=current
    )

# Delete account (Delete)
@app.route('/profile/delete', methods=['GET','POST'])
def delete_account():
    uid = session.get('user_id')
    if not uid:
        return redirect(url_for('index'))
    if request.method == 'POST':
        # actually delete
        conn = get_db_connection()
        cur  = conn.cursor()
        cur.execute("DELETE FROM user_profile WHERE user_id=?", (uid,))
        conn.commit()
        cur.close()
        conn.close()
        session.clear()
        flash('Account deleted', 'info')
        return redirect(url_for('index'))
    # GET → show confirmation page
    return render_template('delete_account.html')

def format_duration(minutes):
    hours, mins = divmod(minutes, 60)
    parts = []
    if hours:
        parts.append(f"{hours} hr" + ("s" if hours > 1 else ""))
    if mins:
        parts.append(f"{mins} min")
    return " ".join(parts) or "0 min"

@app.route('/homepage')
def homepage():
    # grab their current allergies so you could, for example, grey-out recipes
    user = session.get('username')
    allergies = USER_ALLERGIES.get(user, []) if user else []
    q = request.args.get('q', '').strip().lower()
    cuisine = request.args.get('cuisine', '')
    query = {}
    if q:
        query['name'] = {'$regex': q, '$options': 'i'}
    if cuisine:
        query['cusine_path'] = cuisine
        
    recipes = mongo_crud.find_many('Recipes', query)
    cuisines = mongo_crud.distinct('Recipes', 'cusine_path')
    
    # Add temporary display values
    for recipe in recipes:
        recipe['prep_time_display'] = format_duration(recipe['prep_time'])
        recipe['cook_time_display'] = format_duration(recipe['cook_time'])

    return render_template('homepage.html',
                            recipes=recipes,
                            user_allergies=allergies,
                            cuisines = sorted([c for c in cuisines if c])
    )


@app.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    # 1. Fetch the recipe document from MongoDB (all fields from DB)
    recipe = mongo_crud.find_one('Recipes', {"_id": recipe_id})
    reviews = mongo_crud.find_many('Reviews', {"recipe_id": recipe_id})
    print(reviews)
    
    # Add temporary display values
    recipe['prep_time_display'] = format_duration(recipe['prep_time'])
    recipe['cook_time_display'] = format_duration(recipe['cook_time'])

    # Map recipe ingredients to their respective name
    recipe_ingredients = recipe['ingredients']
    # recipe['ingredient_name'] = 
    
    # Map review user_id with the respective username
    # reviews = reviews['user_id']
    # reviews['username'] = 
    
    # 2. MOCK: Add fake allergens and substitutions for demo only
    # (remove these lines once your ETL inserts real data!)
    if recipe:
        # Show these blocks even if recipe from DB doesn't have those fields
        recipe['ingredient_allergens'] = [
            {"name": "Eggs", "description": "May contain traces of eggs"},
            {"name": "Milk"}
        ]
        recipe['ingredient_substitutions'] = [
            {"ingredient": "Milk", "substitute": "Soy Milk"},
            {"ingredient": "Butter", "substitute": "Margarine"}
        ]

    # 3. Allergy warning logic as before (using mock user's allergies)
    allergy_warning = None
    MOCK_USER_ALLERGIES = ["Eggs", "Milk"]
    def get_substitute_for_allergen(allergen):
        # Just match to mock above
        subs = {"Eggs": "Egg Replacer", "Milk": "Soy Milk"}
        return subs.get(allergen, "See Substitutions")
    if recipe:
        for alg in recipe['ingredient_allergens']:
            if alg['name'] in MOCK_USER_ALLERGIES:
                allergy_warning = {
                    'allergen': alg['name'],
                    'substitute': get_substitute_for_allergen(alg['name'])
                }
                break

    return render_template(
        "recipe_detail.html",
        recipe=recipe,
        reviews=reviews,
        allergy_warning=allergy_warning
    )

@app.route('/recipe/<int:recipe_id>/review', methods=['POST'])
def add_review(recipe_id):
    if 'user_id' not in session:
        flash("Please log in to submit a review.", "warning")
        return redirect(url_for('recipe_detail', recipe_id=recipe_id))
    
    description = request.form.get('description')
    rating = int(request.form.get('rating', 0))
    imgs, videos = [], []

    # Handle image uploads
    files = request.files.getlist("media")
    for file in files:
        if file and allowed_file(file.filename, ALLOWED_IMAGE_EXT | ALLOWED_VIDEO_EXT):
            filename = secure_filename(file.filename)
            ext = filename.rsplit('.', 1)[1].lower()
            file_path = Path(app.config['UPLOAD_FOLDER']) / filename
            file.save(str(file_path))
            if ext in ALLOWED_IMAGE_EXT:
                imgs.append(filename)
            elif ext in ALLOWED_VIDEO_EXT:
                videos.append(filename)
                
    video_url = request.form.get('video_url')
    
    review = {
        "recipe_id": recipe_id,
        "user_id": session['user_id'],
        "description": description,
        "rating": rating,
        "imgs": imgs,
        "videos": videos,
        "video_url": video_url,
        "created_at": datetime.utcnow()
    }
    mongo_crud.insert('Reviews', review)
    
    flash("Review added!", "success")
    return redirect(url_for('recipe_detail', recipe_id=recipe_id))

@app.route('/review/<review_id>/edit', methods=['GET', 'POST'])
def edit_review(review_id):
    
    review = mongo_crud.find_one('Reviews', {"_id": ObjectId(review_id)})
    
    if not review or str(review['user_id']) != str(session.get('user_id')):
        flash("Unauthorized.", "danger")
        return redirect(url_for('homepage'))
    
    if request.method == 'POST':
        description = request.form.get('description')
        rating = int(request.form.get('rating', 0))
        video_url = request.form.get('video_url')
        imgs, videos = [], []
        
        files = request.files.getlist("imgs")
        for file in files:
            if file and allowed_file(file.filename, ALLOWED_IMAGE_EXT | ALLOWED_VIDEO_EXT):
                filename = secure_filename(file.filename)
                ext = filename.rsplit('.', 1)[1].lower()
                file_path = Path(app.config['UPLOAD_FOLDER']) / filename
                file.save(str(file_path))
                if ext in ALLOWED_IMAGE_EXT:
                    imgs.append(filename)
                elif ext in ALLOWED_VIDEO_EXT:
                    videos.append(filename)
        
        # Prepare update dictionary
        update_data = {
            "description": description,
            "rating": rating,
            "video_url": video_url,
            "updated_at": datetime.utcnow(),
        }
        
        # Only overwrite media if user uploaded new ones
        if imgs:
            update_data["imgs"] = imgs
        if videos:
            update_data["videos"] = videos
        
        mongo_crud.update_one(
            "Reviews",
            {"_id": ObjectId(review_id)},
            update_data
        )

        flash("Review updated!", "success")
        return redirect(url_for('recipe_detail', recipe_id=review['recipe_id']))
    return render_template("edit_review.html", review=review)


@app.route('/review/<review_id>/delete', methods=['GET', 'POST'])
def delete_review(review_id):
    
    review = mongo_crud.find_one('Reviews', {"_id": ObjectId(review_id)})

    if review and str(review['user_id']) == str(session.get('user_id')):
        recipe_id = review['recipe_id']
        mongo_crud.delete_one('Reviews', {"_id": ObjectId(review_id)})
        flash("Review deleted!", "info")
        return redirect(url_for('recipe_detail', recipe_id=recipe_id))
    flash("Unauthorized or review not found.", "danger")
    return redirect(url_for('homepage'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


# For using uv package manager
def main():
    app.run(debug=True)
    
# For manual testing 
if __name__ == '__main__':
    app.run(debug=True)