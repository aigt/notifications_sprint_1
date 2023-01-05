from models.notification import (
    Meta,
    Notification,
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

welcome_1 = Notification(meta=meta_1, type=NotificationType.welcome)
welcome_2 = Notification(meta=meta_2, type=NotificationType.welcome)
welcome_3 = Notification(meta=meta_3, type=NotificationType.welcome)
