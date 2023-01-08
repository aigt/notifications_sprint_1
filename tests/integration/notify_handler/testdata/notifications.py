import uuid

from models.notification import (
    Meta,
    Notification,
    NotificationScale,
    NotificationType,
    NotificationUrgency,
)

meta_welcome = Meta(urgency=NotificationUrgency.immediate, scale=NotificationScale.individual, periodic=False)

meta_personal = Meta(urgency=NotificationUrgency.usual, scale=NotificationScale.individual, periodic=False)

meta_mass = Meta(urgency=NotificationUrgency.usual, scale=NotificationScale.bulk, periodic=True)

welcome_1 = Notification(
    meta=meta_welcome,
    type=NotificationType.welcome,
    user_id=uuid.uuid4(),
    email="test@gmail.com",
    fields={"user_name": "name"},
)

personal_1 = Notification(
    meta=meta_personal,
    type=NotificationType.info,
    user_id=uuid.uuid4(),
    email="test@gmail.com",
    fields={"user_name": "name"},
)

mass_1 = Notification(
    meta=meta_mass,
    type=NotificationType.info,
    user_id=uuid.uuid4(),
    fields={"movie_id": "id"},
)
