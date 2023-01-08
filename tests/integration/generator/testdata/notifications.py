import uuid

from models.notification import (
    Meta,
    Notification,
    NotificationFromNotifications,
    NotificationScale,
    NotificationType,
    NotificationUrgency,
)

meta_1 = Meta(
    urgency=NotificationUrgency.immediate,
    scale=NotificationScale.individual,
    periodic=False,
)

welcome_1 = NotificationFromNotifications(
    meta=meta_1,
    type=NotificationType.welcome,
    fields={"user_id": uuid.uuid4(), "user_name": "user_1", "email": "test_1@gmail.com"},
)
