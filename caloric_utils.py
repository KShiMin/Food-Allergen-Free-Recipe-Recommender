from datetime import datetime, timedelta
from sqlalchemy.sql import func
from app import db, UserProfile, MealLog

def compute_and_store_caloric_budget(user: UserProfile) -> int:
    """Compute and save the *weekly* caloric budget in the database, adjusted for remaining days in the week."""
    if user.gender == 'male':
        bmr = 10 * user.weight + 6.25 * user.height - 5 * user.age + 5
    elif user.gender == 'female':
        bmr = 10 * user.weight + 6.25 * user.height - 5 * user.age - 161
    else:
        male_bmr = 10 * user.weight + 6.25 * user.height - 5 * user.age + 5
        female_bmr = 10 * user.weight + 6.25 * user.height - 5 * user.age - 161
        bmr = (male_bmr + female_bmr) / 2

    factor_map = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very_active': 1.9
    }
    activity_factor = factor_map.get(user.activity_level, 1.2)
    daily_caloric_budget = bmr * activity_factor

    today = datetime.now().weekday()  # 0=Monday, 6=Sunday
    days_remaining = 7 - today
    adjusted_weekly_budget = round(daily_caloric_budget * days_remaining)

    user.caloric_budget = adjusted_weekly_budget
    db.session.commit()
    return adjusted_weekly_budget

def get_remaining_calories(user: UserProfile) -> int:
    """Calculate remaining weekly calories from meal log entries since start of week."""
    today = datetime.now()
    start_of_week = today - timedelta(days=(today.weekday() + 1) % 7)

    total_logged = db.session.query(func.sum(MealLog.calories))\
        .filter(MealLog.user_id == user.user_id)\
        .filter(MealLog.timestamp >= start_of_week)\
        .scalar() or 0

    return user.caloric_budget - total_logged

def reset_weekly_meal_logs():
    """Delete meal logs older than start of the current week."""
    now = datetime.now()
    start_of_week = now - timedelta(days=(now.weekday() + 1) % 7)
    deleted = MealLog.query.filter(MealLog.timestamp < start_of_week).delete()
    db.session.commit()
    print(f"Deleted {deleted} meal logs older than start of week.")
