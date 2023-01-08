CREATE EXTENSION IF NOT EXISTS "uuid-ossp";


CREATE SCHEMA IF NOT EXISTS notify_history;


CREATE TABLE IF NOT EXISTS notify_history.notification (
      id           uuid PRIMARY KEY DEFAULT uuid_generate_v4()
    , user_id      uuid NOT NULL
    , notification TEXT NOT NULL
    , created_at   TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);


CREATE INDEX IF NOT EXISTS user_id_idx
ON notify_history.notification (user_id);
