CREATE EXTENSION IF NOT EXISTS "uuid-ossp";



CREATE SCHEMA IF NOT EXISTS notify_templates;



CREATE TABLE IF NOT EXISTS notify_templates.email (
      id          uuid PRIMARY KEY DEFAULT uuid_generate_v4()
    , name        VARCHAR(128) NOT NULL
    , template    TEXT NOT NULL
    , created_at  TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    , modified_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    , UNIQUE (name)
);

CREATE TABLE IF NOT EXISTS notify_templates.history (
      id          uuid PRIMARY KEY DEFAULT uuid_generate_v4()
    , name        VARCHAR(128) NOT NULL
    , template    TEXT NOT NULL
    , created_at  TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    , modified_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    , UNIQUE (name)
);



INSERT INTO notify_templates.email (
      name
    , template
)
VALUES
    (
          'welcome'

        , '<!DOCTYPE html>'
          '<html lang="ru">'
          '<head><title>Добро пожаловать!</title></head>'
          '<body>'
            '<h1>Привет {{ name }}!</h1>'
            '<p>Рады приветствовать тебя в нашем кинотеатре!</p>'
          '</body>'
          '</html>'
    ),
    (
          'info'

        , '<!DOCTYPE html>'
          '<html lang="ru">'
          '<head><title>Для информации.</title></head>'
          '<body>'
            '<h1>{{ title }}</h1>'
            '<p>{{ text }}</p>'
          '</body>'
          '</html>'
    ),
    (
          'show_subs'

        , '<!DOCTYPE html>'
          '<html lang="ru">'
          '<head><title>Вышла новая серия.</title></head>'
          '<body>'
            '<h1>{{ title }}</h1>'
            '<h2>{{ movie }}</h2>'
            '<p>{{ text }}</p>'
          '</body>'
          '</html>'
    );

INSERT INTO notify_templates.history (
      name
    , template
)
VALUES
    (
          'welcome'

        , 'Добро пожаловать!\n'
          '\n'
          'Привет {{ name }}!\n'
          'Рады приветствовать тебя в нашем кинотеатре!'
    ),
    (
          'info'

        , '{{ title }}\n'
          '\n'
          '{{ text }}'
    ),
    (
          'show_subs'

        , '{{ title }}\n'
          '{{ movie }}\n'
          '\n'
          '{{ text }}'
    );
