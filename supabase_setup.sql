-- ============================================================
--  CodeQuest — Setup do banco de dados no Supabase
--  Execute este SQL no Supabase > SQL Editor
-- ============================================================

-- Tabela de usuários
CREATE TABLE IF NOT EXISTS users (
    id      BIGSERIAL PRIMARY KEY,
    nome    TEXT NOT NULL,
    email   TEXT NOT NULL UNIQUE,
    senha   TEXT NOT NULL,
    xp      INTEGER NOT NULL DEFAULT 0,
    nivel   INTEGER NOT NULL DEFAULT 1,
    criado_em TIMESTAMPTZ DEFAULT NOW()
);

-- Tabela de progresso
CREATE TABLE IF NOT EXISTS progress (
    id          BIGSERIAL PRIMARY KEY,
    user_id     BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    linguagem   TEXT NOT NULL,
    fase        INTEGER NOT NULL,
    concluido   BOOLEAN NOT NULL DEFAULT TRUE,
    concluido_em TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (user_id, linguagem, fase)
);

-- Índices para performance
CREATE INDEX IF NOT EXISTS idx_progress_user ON progress(user_id);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Row Level Security (RLS) — recomendado para produção
-- ALTER TABLE users ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE progress ENABLE ROW LEVEL SECURITY;
-- (configure as políticas conforme sua estratégia de auth)
