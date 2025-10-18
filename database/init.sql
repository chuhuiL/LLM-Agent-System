-- Initial database setup script
-- This runs automatically when PostgreSQL container starts for the first time

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For fuzzy text search

-- Create indexes for common search patterns (will be managed by Alembic later)
-- This file can contain seed data or other initialization tasks
