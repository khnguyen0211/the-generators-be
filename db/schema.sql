-- =============================================================
-- The Generators - Database Schema Reference
-- =============================================================
-- This file is for REFERENCE ONLY. It documents the current
-- database structure for easy reading and review.
--
-- The actual init script is: db/init/001_initial_schema.sql
-- Schema changes go in: db/migrations/{version}_{name}.sql
-- =============================================================

-- ===== USERS =====
-- Future extensibility for authentication and per-user tracking.
--
-- id          UUID         Primary key, auto-generated
-- email       VARCHAR(255) Unique, nullable
-- api_key     VARCHAR(255) Unique, nullable
-- name        VARCHAR(200) Display name
-- is_active   BOOLEAN      Default TRUE
-- created_at  TIMESTAMPTZ  Auto-set on insert
-- updated_at  TIMESTAMPTZ  Auto-set on insert

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE,
    api_key VARCHAR(255) UNIQUE,
    name VARCHAR(200),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ===== JOBS =====
-- Persistent storage for all AI generation jobs.
-- Mirrors the in-memory/Redis Job model but with durable storage.
--
-- id          UUID         Primary key, auto-generated
-- job_type    VARCHAR(50)  e.g. 'text_to_image', 'text_to_video', 'text_to_speech'
-- status      VARCHAR(20)  One of: 'pending', 'processing', 'completed', 'failed'
-- payload     JSONB        Original request data (prompt, provider, size, etc.)
-- result      JSONB        Generation result (output_url, provider, model)
-- error       TEXT         Error message if job failed
-- provider    VARCHAR(50)  AI provider used (openai, replicate, stability)
-- model       VARCHAR(100) Model name (dall-e-3, flux-pro, etc.)
-- user_id     UUID         FK to users table (nullable, for future use)
-- created_at  TIMESTAMPTZ  Auto-set on insert
-- updated_at  TIMESTAMPTZ  Auto-set on insert
--
-- Indexes: status, job_type, created_at
-- Constraint: status must be one of pending/processing/completed/failed

CREATE TABLE jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_type VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    payload JSONB NOT NULL,
    result JSONB,
    error TEXT,
    provider VARCHAR(50),
    model VARCHAR(100),
    user_id UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT jobs_status_check CHECK (status IN ('pending', 'processing', 'completed', 'failed'))
);

CREATE INDEX idx_jobs_status ON jobs(status);
CREATE INDEX idx_jobs_job_type ON jobs(job_type);
CREATE INDEX idx_jobs_created_at ON jobs(created_at);

-- ===== GENERATION HISTORY =====
-- Detailed record of completed generations with rich metadata.
-- One-to-one with jobs (created when job completes successfully).
--
-- id              UUID         Primary key, auto-generated
-- job_id          UUID         FK to jobs table (NOT NULL)
-- job_type        VARCHAR(50)  Denormalized for query convenience
-- provider        VARCHAR(50)  AI provider that handled the generation
-- model           VARCHAR(100) Specific model used
-- input_params    JSONB        Full input parameters sent to AI provider
-- output_url      TEXT         URL/path to generated content
-- output_metadata JSONB        Additional output info (dimensions, format, etc.)
-- duration_ms     INTEGER      Processing time in milliseconds
-- user_id         UUID         FK to users table (nullable, for future use)
-- created_at      TIMESTAMPTZ  Auto-set on insert
--
-- Indexes: job_type, provider, created_at

CREATE TABLE generation_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id UUID NOT NULL REFERENCES jobs(id),
    job_type VARCHAR(50) NOT NULL,
    provider VARCHAR(50) NOT NULL,
    model VARCHAR(100) NOT NULL,
    input_params JSONB NOT NULL,
    output_url TEXT,
    output_metadata JSONB,
    duration_ms INTEGER,
    user_id UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_generation_history_job_type ON generation_history(job_type);
CREATE INDEX idx_generation_history_provider ON generation_history(provider);
CREATE INDEX idx_generation_history_created_at ON generation_history(created_at);

-- ===== API USAGE =====
-- Tracks every API request for monitoring and analytics.
--
-- id               BIGSERIAL    Auto-incrementing primary key
-- endpoint         VARCHAR(200) API endpoint path (e.g. /api/text-to-image/generate)
-- method           VARCHAR(10)  HTTP method (GET, POST, etc.)
-- status_code      INTEGER      HTTP response status code
-- response_time_ms INTEGER      Response time in milliseconds
-- ip_address       VARCHAR(45)  Client IP (supports IPv6)
-- user_id          UUID         FK to users table (nullable, for future use)
-- created_at       TIMESTAMPTZ  Auto-set on insert
--
-- Indexes: endpoint, created_at

CREATE TABLE api_usage (
    id BIGSERIAL PRIMARY KEY,
    endpoint VARCHAR(200) NOT NULL,
    method VARCHAR(10) NOT NULL,
    status_code INTEGER NOT NULL,
    response_time_ms INTEGER,
    ip_address VARCHAR(45),
    user_id UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_api_usage_endpoint ON api_usage(endpoint);
CREATE INDEX idx_api_usage_created_at ON api_usage(created_at);

-- ===== SCHEMA MIGRATIONS =====
-- Tracks which database migrations have been applied.
-- Used by db/migrate.py to determine pending migrations.
--
-- id         SERIAL       Auto-incrementing primary key
-- version    VARCHAR(50)  Migration version number (e.g. '001', '002')
-- name       VARCHAR(200) Migration description
-- applied_at TIMESTAMPTZ  When the migration was applied

CREATE TABLE schema_migrations (
    id SERIAL PRIMARY KEY,
    version VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(200) NOT NULL,
    applied_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
