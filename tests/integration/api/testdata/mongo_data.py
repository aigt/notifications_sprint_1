from uuid import UUID

from bson import Binary

user_1 = Binary.from_uuid(UUID("c2a3342b-6e8e-4293-9d70-f0e7bc623914"))
user_2 = Binary.from_uuid(UUID("5358a10e-a177-41e9-a714-3dc3cc3a99e8"))

bookmark_1 = {
    "user_id": user_1,
    "bookmarks": [
        Binary.from_uuid(UUID("3b241101-e2bb-4255-8caf-4136c566a962")),
        Binary.from_uuid(UUID("5b245401-e2bb-4255-8caf-4136c566a962")),
    ],
}

bookmark_2 = {
    "user_id": user_2,
    "bookmarks": [
        Binary.from_uuid(UUID("8bf4c549-8c3b-4e76-90dc-3d4996fb3f88")),
        Binary.from_uuid(UUID("8da16f93-e3db-4b8f-bfa7-aa339127cade")),
        Binary.from_uuid(UUID("3b241101-e2bb-4255-8caf-4136c566a962")),
    ],
}
