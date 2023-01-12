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

meta_2 = Meta(
    urgency=NotificationUrgency.immediate,
    scale=NotificationScale.bulk,
    periodic=False,
)

welcome_1 = NotificationFromNotifications(
    meta=meta_1,
    type=NotificationType.welcome,
    fields={
        "user_id": uuid.uuid4(),
        "confirmation_url": "http://localhost/confirmation?user_id=uuid&tmp=16234234",
        "user_name": "user_1",
        "email": "test_1@gmail.com",
    },
)

new_series = NotificationFromNotifications(
    meta=meta_2, type=NotificationType.show_subs, fields={"movie_id": "3b241101-e2bb-4255-8caf-4136c566a962"}
)
