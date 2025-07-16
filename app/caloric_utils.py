from datetime import datetime
from db.sql.db import get_db_connection
from datetime import datetime, timedelta

def compute_and_store_caloric_budget(user: dict) -> int:
    """
    Calculates the user’s remaining weekly caloric budget based on
    their height, weight, age, gender, and activity level—then
    stores it in the user_profile.caloric_budget field.
    Returns the new budget (in kcal).
    """
    # 1) Compute BMR (Mifflin-St Jeor)
    w      = user['weight']   or 0
    h      = user['height']   or 0
    a      = user['age']      or 0
    gender = user['gender']   or 'prefer_not_to_say'
    uid    = user['user_id']

    if gender == 'male':
        bmr = 10*w + 6.25*h - 5*a + 5
    elif gender == 'female':
        bmr = 10*w + 6.25*h - 5*a - 161
    else:
        # average of male & female if unspecified
        m = 10*w + 6.25*h - 5*a + 5
        f = 10*w + 6.25*h - 5*a - 161
        bmr = (m + f) / 2

    # 2) Apply activity factor
    factor_map = {
        'sedentary':   1.2,
        'light':       1.375,
        'moderate':    1.55,
        'active':      1.725,
        'very_active': 1.9
    }
    factor = factor_map.get(user.get('activity_level', 'sedentary'), 1.2)
    daily_cal = bmr * factor

    # 3) Scale to remaining days in this week
    today_wday = datetime.now().weekday()  # Monday=0 … Sunday=6
    days_left   = 7 - today_wday
    weekly_cal  = round(daily_cal * days_left)

    # 4) Persist into SQL
    conn = get_db_connection()
    cur  = conn.cursor()
    cur.execute(
      "UPDATE user_profile SET caloric_budget = ? WHERE user_id = ?",
      (weekly_cal, uid)
    )
    conn.commit()
    cur.close()
    conn.close()

    return weekly_cal

def get_remaining_calories(user):
    now = datetime.now()
    start_dt = (now - timedelta(days=now.weekday())).replace(
        hour=0, minute=0, second=0, microsecond=0)
    start_str = start_dt.strftime("%Y-%m-%d %H:%M:%S")

    conn = get_db_connection()
    cur  = conn.cursor()
    cur.execute(
      "SELECT COALESCE(SUM(calories),0) AS total "
      "FROM meal_log WHERE user_id = ? AND timestamp >= ?",
      (user['user_id'], start_str)
    )
    total = cur.fetchone()['total']
    cur.close()
    conn.close()

    budget = user['caloric_budget'] or 0
    return budget - total


def reset_weekly_meal_logs() -> int:
    """
    Deletes all meal_log entries older than the start of the current week.
    Returns the number of rows deleted.
    """
    now = datetime.now()
    # find Monday 00:00 of this week
    start_of_week = now - timedelta(days=now.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)

    conn = get_db_connection()
    cur  = conn.cursor()
    cur.execute(
        """
        DELETE FROM meal_log
         WHERE timestamp < ?
        """,
        (start_of_week,)
    )
    deleted = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()

    return deleted