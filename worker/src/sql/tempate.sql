SELECT *
  FROM notify_templates.{table_name} AS t
 WHERE t.name = %s
 LIMIT 1;
