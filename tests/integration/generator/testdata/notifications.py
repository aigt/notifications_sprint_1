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
    urgency=NotificationUrgency.immediate, scale=NotificationScale.individual, email="test_1@gmail.com", periodic=False
)
meta_2 = Meta(
    urgency=NotificationUrgency.immediate, scale=NotificationScale.individual, email="test_2@gmail.com", periodic=False
)
meta_3 = Meta(
    urgency=NotificationUrgency.immediate, scale=NotificationScale.individual, email="test_3@gmail.com", periodic=False
)

welcome_1 = NotificationFromNotifications(
    meta=meta_1, type=NotificationType.welcome, fields={"user_id": uuid.uuid4(), "user_name": "user_1"}
)
welcome_2 = NotificationFromNotifications(
    meta=meta_2, type=NotificationType.welcome, fields={"user_id": uuid.uuid4(), "user_name": "user_2"}
)
welcome_3 = NotificationFromNotifications(
    meta=meta_3, type=NotificationType.welcome, fields={"user_id": uuid.uuid4(), "user_name": "user_3"}
)
