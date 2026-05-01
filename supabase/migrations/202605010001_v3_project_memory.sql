-- Dealix v3 Project Intelligence Memory
-- Supabase/Postgres + pgvector schema for code, docs, strategic memory, and semantic search.

create extension if not exists vector with schema extensions;

create table if not exists project_documents (
    id uuid primary key default gen_random_uuid(),
    source text not null,
    source_type text not null default 'code',
    path text not null,
    title text,
    content text not null,
    content_hash text not null,
    metadata jsonb not null default '{}'::jsonb,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    unique(source, path, content_hash)
);

create table if not exists project_chunks (
    id uuid primary key default gen_random_uuid(),
    document_id uuid not null references project_documents(id) on delete cascade,
    chunk_index integer not null,
    content text not null,
    token_estimate integer not null default 0,
    metadata jsonb not null default '{}'::jsonb,
    embedding extensions.vector(384),
    created_at timestamptz not null default now(),
    unique(document_id, chunk_index)
);

create table if not exists strategic_memory (
    id uuid primary key default gen_random_uuid(),
    memory_type text not null,
    subject text not null,
    content text not null,
    importance integer not null default 5 check (importance between 1 and 10),
    metadata jsonb not null default '{}'::jsonb,
    embedding extensions.vector(384),
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create index if not exists idx_project_documents_source_path on project_documents(source, path);
create index if not exists idx_project_documents_type on project_documents(source_type);
create index if not exists idx_project_chunks_document on project_chunks(document_id);
create index if not exists idx_strategic_memory_type on strategic_memory(memory_type);

create index if not exists idx_project_chunks_embedding_hnsw
    on project_chunks using hnsw (embedding vector_ip_ops);

create index if not exists idx_strategic_memory_embedding_hnsw
    on strategic_memory using hnsw (embedding vector_ip_ops);

create or replace function match_project_chunks(
    query_embedding extensions.vector(384),
    match_threshold float default 0.72,
    match_count int default 12
)
returns table (
    chunk_id uuid,
    document_id uuid,
    path text,
    source_type text,
    content text,
    similarity float,
    metadata jsonb
)
language sql stable
as $$
    select
        pc.id as chunk_id,
        pd.id as document_id,
        pd.path,
        pd.source_type,
        pc.content,
        1 - (pc.embedding <#> query_embedding) as similarity,
        pc.metadata || pd.metadata as metadata
    from project_chunks pc
    join project_documents pd on pd.id = pc.document_id
    where pc.embedding is not null
      and 1 - (pc.embedding <#> query_embedding) >= match_threshold
    order by pc.embedding <#> query_embedding
    limit match_count;
$$;

create or replace function match_strategic_memory(
    query_embedding extensions.vector(384),
    match_threshold float default 0.72,
    match_count int default 10
)
returns table (
    memory_id uuid,
    memory_type text,
    subject text,
    content text,
    importance integer,
    similarity float,
    metadata jsonb
)
language sql stable
as $$
    select
        id as memory_id,
        memory_type,
        subject,
        content,
        importance,
        1 - (embedding <#> query_embedding) as similarity,
        metadata
    from strategic_memory
    where embedding is not null
      and 1 - (embedding <#> query_embedding) >= match_threshold
    order by embedding <#> query_embedding
    limit match_count;
$$;

alter table project_documents enable row level security;
alter table project_chunks enable row level security;
alter table strategic_memory enable row level security;
