-- ============================================================
--  CodeQuest — Migração para Supabase Auth
--  Execute no Supabase > SQL Editor
-- ============================================================

-- Remove coluna senha (agora gerenciada pelo Supabase Auth)
ALTER TABLE users DROP COLUMN IF EXISTS senha;

-- Garante que o id de users seja o mesmo uuid do Auth
-- (se já existe dados, limpe antes)
TRUNCATE TABLE progress;
TRUNCATE TABLE users;

-- Recria users vinculada ao auth.users
ALTER TABLE users
  DROP CONSTRAINT IF EXISTS users_pkey CASCADE;

ALTER TABLE users
  ADD CONSTRAINT users_pkey PRIMARY KEY (id);

-- Faz o id de users referenciar o auth do Supabase
ALTER TABLE users
  DROP CONSTRAINT IF EXISTS users_id_fkey;

ALTER TABLE users
  ADD CONSTRAINT users_id_fkey
  FOREIGN KEY (id) REFERENCES auth.users(id) ON DELETE CASCADE;

-- Garante constraint de progresso
ALTER TABLE progress
  DROP CONSTRAINT IF EXISTS progress_user_id_linguagem_fase_key;

ALTER TABLE progress
  ADD CONSTRAINT progress_user_id_linguagem_fase_key
  UNIQUE (user_id, linguagem, fase);

-- Índices
CREATE INDEX IF NOT EXISTS idx_progress_user ON progress(user_id);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
