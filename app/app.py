# ui.py
from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # needed for flash messages

# In-memory “user database” for demo
USERS = {
    'alice': { 'password': 'password123', 'email': 'alice@example.com' },
    'bob':   { 'password': 'qwerty', 'email': 'bob@example.net' }
}

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
        return redirect(url_for('menu'))

    # GET → show the form with their current choices
    current = USER_ALLERGIES.get(user, [])
    return render_template('allergies.html',
                           all_allergens=ALL_ALLERGENS,
                           user_allergies=current)

# Sample recipes for the menu page
RECIPES = [
    {
        'title': 'Creamy Meatballs & Pasta',
        'time': '35 Minutes',
        'servings': '4 Servings',
        'calories': 210,
        'image': 'p2.jpg'
    },
    {
        'title': 'Sweet And Spicy Barbecue Wings',
        'time': '15 Minutes',
        'servings': '2 Servings',
        'calories': 460,
        'image': 'p3.jpg'
    },
    {
        'title': 'Grilled Garlic Chicken & Veggies',
        'time': '35 Minutes',
        'servings': '3 Servings',
        'calories': 354,
        'image': 'p1.jpg'
    },
    {
        'title': 'Shrimp Salad With Lettuce Corn',
        'time': '20 Minutes',
        'servings': '2 Servings',
        'calories': 258,
        'image': 'p2.jpg'
    },
    {
        'title': 'Fresh Pesto Pasta With Peas',
        'time': '40 Minutes',
        'servings': '4 Servings',
        'calories': 263,
        'image': 'p3.jpg'
    },
    {
        'title': 'Stir-Fried Egg With Thai Basil And Chilli',
        'time': '45 Minutes',
        'servings': '3 Servings',
        'calories': 177,
        'image': 'p2.jpg'
    },
]

@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    user_record = USERS.get(username)
    # make sure it exists AND its 'password' field matches
    if user_record and user_record.get('password') == password:
        session['username'] = username
        return redirect(url_for('menu'))
    else:
        flash('Invalid username or password', 'danger')
        return redirect(url_for('index'))

@app.route('/menu')
def menu():
    # grab their current allergies so you could, for example, grey-out recipes
    user = session.get('username')
    allergies = USER_ALLERGIES.get(user, []) if user else []
    return render_template('menu.html',
                           recipes=RECIPES,
                           user_allergies=allergies)

@app.route('/logout')
def logout():
    # drop the username from session
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/profile', methods=['GET','POST'])
def profile():
    user = session.get('username')
    if not user:
        flash('Please log in first.', 'warning')
        return redirect(url_for('index'))

    # Grab their record
    record = USERS[user]

    if request.method == 'POST':
        # If you want to allow username changes, handle renaming here:
        new_username = request.form['username'].strip()
        new_email    = request.form['email'].strip()

        # 1) Update email
        record['email'] = new_email

        # 2) (Optional) Rename user key if they changed username
        if new_username and new_username != user:
            USERS[new_username] = USERS.pop(user)
            USER_ALLERGIES[new_username] = USER_ALLERGIES.pop(user, [])
            session['username'] = new_username
            user = new_username
            flash('Username & email updated!', 'success')
        else:
            flash('Email updated!', 'success')

        return redirect(url_for('profile'))

    # GET → render the form
    return render_template('profile.html',
                           username=user,
                           email=record.get('email',''))


if __name__ == '__main__':
    app.run(debug=True)
