from app import app, db, UserProfile, MealLog, Recipe
from datetime import datetime, timedelta
from caloric_utils import compute_and_store_caloric_budget, get_remaining_calories, reset_weekly_meal_logs

def create_test_user(name, gender):
    user = UserProfile(
        user_name=name,
        user_password="test123",
        height=170,
        weight=70,
        age=30,
        gender=gender,
        dietary_preferences="none",
        activity_level="moderate",
        caloric_budget=0
    )
    db.session.add(user)
    db.session.commit()
    return user

def ensure_recipe_exists():
    recipe = Recipe.query.get(1)
    if not recipe:
        recipe = Recipe(recipe_id=1, recipe_name="Test Recipe")
        db.session.add(recipe)
        db.session.commit()

# def test_compute_and_remaining():
#     ensure_recipe_exists()
#     users = [
#         create_test_user("male_user", "male"),
#         create_test_user("female_user", "female"),
#         create_test_user("neutral_user", "prefer_not_to_say")
#     ]

#     for user in users:
#         budget = compute_and_store_caloric_budget(user)
#         print(f"\nUser: {user.user_name}, Budget: {budget} kcal")

#         # log one meal of 500 kcal
#         MealLog.query.filter_by(user_id=user.user_id).delete()
#         db.session.commit()

#         log = MealLog(
#             user_id=user.user_id,
#             recipe_id=1,
#             calories=500,
#             timestamp=datetime.now()
#         )
#         db.session.add(log)
#         db.session.commit()

#         remaining = get_remaining_calories(user)
#         print(f"Remaining for {user.user_name}: {remaining} kcal")
#         print(f"\n📊 DEBUG for user: {user.user_name}")
#         print(f"🗓️ Today is: {datetime.utcnow().strftime('%A')}")
#         print(f"💾 Caloric budget: {budget}")
#         print(f"🍽️ Logged calories this week: {budget - remaining}")
#         print(f"📉 Remaining calories: {remaining}")
#         print(f"🧮 Expected: {budget - 500}")
#         assert abs(remaining - (budget - 500)) <= 1

def test_reset():
    user = create_test_user("reset_user", "male")
    ensure_recipe_exists()

    db.session.add(MealLog(
        user_id=user.user_id, recipe_id=1, calories=500,
        timestamp=datetime.now() - timedelta(days=8)
    ))

    # One from now (should remain)
    db.session.add(MealLog(
        user_id=user.user_id, recipe_id=1, calories=300,
        timestamp=datetime.now()
    ))
    db.session.commit()

    reset_weekly_meal_logs()
    logs = MealLog.query.filter_by(user_id=user.user_id).all()
    assert len(logs) == 1 and logs[0].calories == 300
    print("\n✅ Weekly reset test passed")

if __name__ == '__main__':
    with app.app_context():
        # test_compute_and_remaining()
        test_reset()