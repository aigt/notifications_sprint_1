import uuid

EMAIL = "test_email@gmail.com"
data_1 = {
    "meta": {"urgency": "immediate", "scale": "bulk", "periodic": True},
    "type": "show_subs",
    "custom_template": "string",
    "fields": {
        "email": EMAIL,
        "user_id": str(uuid.uuid4()),
    },
}
