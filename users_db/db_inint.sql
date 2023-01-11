CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE SCHEMA IF NOT EXISTS users_auth;

CREATE TABLE IF NOT EXISTS users_auth.users (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    login TEXT NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    modified_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS users_auth.users_data (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id uuid,
    email TEXT NOT NULL,
    first_name TEXT,
    last_name TEXT,
    modified_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_user_id FOREIGN KEY(user_id) REFERENCES users_auth.users(id)
);
