import uuid

EMAIL = "test_email@gmail.com"

data_welcome = {
    "meta": {"urgency": "immediate", "scale": "bulk", "periodic": True},
    "type": "welcome",
    "custom_template": "string",
    "fields": {"email": EMAIL, "user_id": str(uuid.uuid4()), "confirmation_url": "http://localhost:8000/api/"},
}

data_info = {
    "meta": {"urgency": "immediate", "scale": "bulk", "periodic": True},
    "type": "welcome",
    "custom_template": "string",
    "fields": {"email": EMAIL, "user_id": str(uuid.uuid4()), "confirmation_url": "http://localhost:8000/api/"},
}

data_show_subs = {
    "meta": {"urgency": "immediate", "scale": "bulk", "periodic": True},
    "type": "welcome",
    "custom_template": "string",
    "fields": {"email": EMAIL, "user_id": str(uuid.uuid4()), "confirmation_url": "http://localhost:8000/api/"},
}
