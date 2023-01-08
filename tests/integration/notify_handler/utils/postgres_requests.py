from typing import Any

from psycopg import Cursor

from models.notification import Meta, Notification


def get_personal_notification(cur: Cursor, notification: str, user_id: str) -> Any:
    cur.execute(
        """
    SELECT * from notify_schedule.personal
    WHERE notification = %s AND user_id = %s
    """,
        (notification, user_id),
    )
    return cur.fetchone()


def get_mass_notification(cur: Cursor, notification: str) -> Any:
    cur.execute(
        """
    SELECT * from notify_schedule.mass
    WHERE notification = %s
    """,
        (notification,),
    )
    return cur.fetchone()


def notification_format(in_postgres: dict) -> Notification:
    notification = in_postgres["notification"]
    notification["meta"] = Meta(**notification["meta"])
    return Notification(**notification)
