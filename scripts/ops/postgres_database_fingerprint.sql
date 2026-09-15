\pset tuples_only on
\pset format unaligned
\pset fieldsep '|'
SELECT format(
  'SELECT %L, count(*), md5(COALESCE(string_agg(to_jsonb(t)::text, %L ORDER BY to_jsonb(t)::text), %L)) FROM public.%I AS t;',
  tablename, '|', '', tablename
)
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY tablename;
\gexec
