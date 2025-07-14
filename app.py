# ui.py
from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session, abort
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import os
import csv

app = Flask(__name__)

app.config.from_pyfile('config.py')

app.secret_key = 'your-secret-key'  # needed for flash messages
app.config['SQLALCHEMY_DATABASE_URI'] = (
    "mariadb+mariadbconnector://"
    "flask:flaskpass@127.0.0.1:3306/recipe_app_db"
)

app.config['SQLALCHEMY_ECHO'] = True

mongo = PyMongo(app)
db = SQLAlchemy(app)

BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
FILTERED_CSV = os.path.join(BASE_DIR, 'data', 'filtered_recipe.csv')

# 1) user_profile
class UserProfile(db.Model):
    __tablename__ = 'user_profile'

    user_id             = db.Column(db.Integer,   primary_key=True, autoincrement=True)
    user_name           = db.Column(db.String(15), nullable=False)
    user_password       = db.Column(db.String(20), nullable=False)
    height              = db.Column(db.Float)
    weight              = db.Column(db.Float)
    gender              = db.Column(
        db.Enum('male', 'female', 'prefer_not_to_say'),
        nullable=True
    )
    age                 = db.Column(db.Integer)
    caloric_budget      = db.Column(db.Integer)
    dietary_preferences = db.Column(db.Text)
    activity_level      = db.Column(
        db.Enum('sedentary', 'light', 'moderate', 'active', 'very_active'),
        nullable=True
    )

    # relationship to allergens
    allergens = db.relationship(
        'Allergen',
        secondary='user_allergen',
        back_populates='users',
        cascade='all, delete'
    )


# 2) allergen
class Allergen(db.Model):
    __tablename__ = 'allergen'

    allergen_id          = db.Column(db.Integer, primary_key=True)
    allergen_name        = db.Column(db.String(255), nullable=False)
    allergen_description = db.Column(db.String(255))

    # back-ref to users
    users = db.relationship(
        'UserProfile',
        secondary='user_allergen',
        back_populates='allergens'
    )

    # relationship to ingredients
    ingredients = db.relationship(
        'Ingredient',
        secondary='ingredient_allergen',
        back_populates='allergens'
    )


# 3) user_allergen (association table)
class UserAllergen(db.Model):
    __tablename__ = 'user_allergen'

    user_id     = db.Column(
        db.Integer,
        db.ForeignKey('user_profile.user_id', ondelete='CASCADE'),
        primary_key=True
    )
    allergen_id = db.Column(
        db.Integer,
        db.ForeignKey('allergen.allergen_id'),
        primary_key=True
    )


# 4) ingredient
class Ingredient(db.Model):
    __tablename__ = 'ingredient'

    ingredient_id    = db.Column(db.String(5),   primary_key=True)
    ingredient_name  = db.Column(db.String(255), nullable=False)
    nutritional_info = db.Column(db.Float,       nullable=False)

    # allergens on this ingredient
    allergens = db.relationship(
        'Allergen',
        secondary='ingredient_allergen',
        back_populates='ingredients'
    )

    # substitutions (self-referential M2M)
    substitutes = db.relationship(
        'Ingredient',
        secondary='ingredient_substitution',
        primaryjoin='Ingredient.ingredient_id==IngredientSubstitution.original_ingredient_id',
        secondaryjoin='Ingredient.ingredient_id==IngredientSubstitution.substitute_ingredient_id',
        backref='substituted_from'
    )


# 5) ingredient_allergen (association table)
class IngredientAllergen(db.Model):
    __tablename__ = 'ingredient_allergen'

    allergen_id   = db.Column(
        db.Integer,
        db.ForeignKey('allergen.allergen_id'),
        primary_key=True
    )
    ingredient_id = db.Column(
        db.String(5),
        db.ForeignKey('ingredient.ingredient_id'),
        primary_key=True
    )


# 6) ingredient_substitution (association table)
class IngredientSubstitution(db.Model):
    __tablename__ = 'ingredient_substitution'

    original_ingredient_id   = db.Column(
        db.String(5),
        db.ForeignKey('ingredient.ingredient_id'),
        primary_key=True
    )
    substitute_ingredient_id = db.Column(
        db.String(5),
        db.ForeignKey('ingredient.ingredient_id'),
        primary_key=True
    )
    
# 7) Caloric Budget Log
class MealLog(db.Model):
    __tablename__ = 'meal_log'

    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profile.user_id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.recipe_id'), nullable=False)
    calories = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('UserProfile', backref='meal_logs')
    recipe = db.relationship('Recipe', backref='meal_logs')

# 8) Recipe (placeholder)
class Recipe(db.Model):
    __tablename__ = 'recipe'

    recipe_id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(255), nullable=False)

def init_db():
    # ensure any SQLAlchemy models are created (optional)
    db.create_all()

    # load your .sql file
    sql_path = os.path.join(app.root_path, 'project_sql_script_300625.sql')
    with open(sql_path, 'r', encoding='utf-8') as f:
        full_sql = f.read()

    # split on semicolons and strip out any empty bits
    statements = [stmt.strip() for stmt in full_sql.split(';') if stmt.strip()]

    # execute each DDL/DML in its own call, inside one transaction
    with db.engine.begin() as conn:
        for stmt in statements:
            conn.execute(text(stmt))

    print("✅ All statements applied via manual split.")
    
@app.route('/edit_allergies', methods=['GET','POST'])
def edit_allergies():
    if 'username' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('index'))

    user = UserProfile.query.filter_by(user_name=session['username']).first_or_404()
    all_allergens = Allergen.query.order_by(Allergen.allergen_name).all()

    if request.method == 'POST':
        # 🔍 debug prints:
        print("▶️ RAW form data:", request.form)  
        chosen = request.form.getlist('allergies')
        print("▶️ chosen list:", chosen)

        selected = Allergen.query.filter(
            Allergen.allergen_name.in_(chosen)
        ).all()
        print("▶️ selected ORM rows:", [a.allergen_name for a in selected])

        # overwrite the user’s M2M list
        user.allergens = selected
        db.session.commit()
        # redirect back here so you immediately see the ticked boxes
        return redirect(url_for('edit_allergies'))

    return render_template(
        'allergies.html',
        all_allergens=[a.allergen_name for a in all_allergens],
        user_allergies=[a.allergen_name for a in user.allergens]
    )


@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/login', methods=['POST'])
def login():
    uname = request.form.get('username', '').strip()
    pwd   = request.form.get('password', '')

    print("🔑 Login attempt for:", repr(uname))
    print("🔐 Password entered:", repr(pwd))

    user = UserProfile.query.filter_by(user_name=uname).first()
    print("👤  Lookup result:", user)
    if user:
        print("💾 Stored pw:", repr(user.user_password))

    if user and user.user_password == pwd:
        session['username'] = uname
        return redirect(url_for('menu'))

    flash('Invalid username or password', 'danger')
    return redirect(url_for('index'))


@app.route('/menu')
def menu():
    # ——— user & allergies logic stays the same ———
    if 'username' in session:
        user      = UserProfile.query.filter_by(user_name=session['username']).first()
        allergies = [a.allergen_name for a in user.allergens]
    else:
        allergies = []

    # ——— read your filtered_recipe.csv ———
    recipes = []
    with open(FILTERED_CSV, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            recipes.append({
                # use the original index as an ID, or enumerate() if you prefer
                'id':        row['Unnamed: 0'],
                'name':      row['recipe_name'],
                'img_src':   row['img_src'],       # matches your template’s filename
                'prep_time': row['prep_time'],     # e.g. "15 mins"
                'cook_time': row.get('cook_time') or '0 mins',
            })

    return render_template(
        'menu.html',
        recipes=recipes,
        user_allergies=allergies
    )


@app.route('/logout')
def logout():
    # drop the username from session
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/profile', methods=['GET','POST'])
def profile():
    if 'username' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('index'))

    user = UserProfile.query.\
        filter_by(user_name=session['username']).\
        first_or_404()

    if request.method == 'POST':
        new_name = request.form['username'].strip()
        if new_name and new_name != user.user_name:
            user.user_name = new_name
            db.session.commit()
            session['username'] = new_name
            flash('Username updated!', 'success')
        else:
            flash('No change made.', 'info')
        return redirect(url_for('profile'))

    return render_template(
        'profile.html',
        username=user.user_name
    )

@app.route('/recipe/<recipe_id>')
def recipe_detail(recipe_id):
    import csv, os
    BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
    CSV_PATH     = os.path.join(BASE_DIR, 'data', 'filtered_recipe.csv')

    recipe = None
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            if row['Unnamed: 0'] == recipe_id:
                recipe = {
                    'id':                row['Unnamed: 0'],
                    'name':              row['recipe_name'],
                    'img_src':           row['img_src'],
                    'prep_time':         row['prep_time'],
                    'cook_time':         row['cook_time'],
                    'total_time':        row['total_time'],
                    'servings':          row['servings'],
                    'yield':             row.get('yield'),
                    'rating':            row.get('rating'),
                    'url':               row.get('url'),
                    'cuisine_path':      row.get('cuisine_path'),
                    'nutrition':         row.get('nutrition'),
                    'timing':            row.get('timing'),
                    'ingredients':       row.get('ingredients'),
                    'directions':        row.get('directions'),
                    'cleaned_ingredients': row.get('cleaned_ingredients'),
                    'quantity':          row.get('quantity'),
                }
                break

    if not recipe:
        abort(404)

    return render_template('recipe_detail.html',
                           recipe=recipe)

# @app.route('/log-meal')
# def log_meal():
#     if 'user_id' not in session:
#         return redirect(url_for('/'))
#     recipes = Recipe.query.all()
#     return render_template('log_meal.html', recipes=recipes)


if __name__ == '__main__':
    with app.app_context():
        init_db()
        db.create_all()
        print("Database schema updated.")
    app.run(debug=True)
