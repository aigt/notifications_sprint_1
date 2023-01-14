INSERT INTO notify_history.notification (
      user_id
    , notification
)
VALUES
    (
          %(user_id)s
        , %(notification)s
    )
RETURNING *;
