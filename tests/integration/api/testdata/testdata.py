import uuid

EMAIL = "test_email@gmail.com"

data_welcome = {
    "meta": {"urgency": "immediate", "scale": "bulk", "periodic": False},
    "type": "welcome",
    "custom_template": "string",
    "fields": {"email": EMAIL, "user_id": str(uuid.uuid4()), "confirmation_url": "http://localhost:8000/api/"},
}

data_info = {
    "meta": {"urgency": "immediate", "scale": "bulk", "periodic": False},
    "type": "info",
    "custom_template": "string",
    "fields": {"content": "some content"},
}

data_show_subs = {
    "meta": {"urgency": "immediate", "scale": "bulk", "periodic": False},
    "type": "show_subs",
    "custom_template": "string",
    "fields": {"movie_id": "8da16f93-e3db-4b8f-bfa7-aa339127cade"},
}
