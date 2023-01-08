CREATE EXTENSION IF NOT EXISTS "uuid-ossp";


CREATE SCHEMA IF NOT EXISTS notify_schedule;


CREATE TABLE IF NOT EXISTS notify_schedule.personal (
      id           uuid PRIMARY KEY DEFAULT uuid_generate_v4()
    , user_id      uuid NOT NULL
    , notification JSONB NOT NULL
    , created_at   TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS notify_schedule.mass (
      id           uuid PRIMARY KEY DEFAULT uuid_generate_v4()
    , notification JSONB NOT NULL
    , created_at   TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);


CREATE INDEX IF NOT EXISTS personal_user_id_idx
ON notify_schedule.personal (user_id);
