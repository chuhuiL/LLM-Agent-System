# Setup Guide

Detailed setup instructions for the Clinical Documentation Platform.

## Prerequisites

### Required Software

1. **Docker Desktop** (Recommended for easiest setup)
   - Download: https://www.docker.com/products/docker-desktop
   - Minimum version: 20.10+
   - Ensure Docker Compose is included

2. **Git**
   - Download: https://git-scm.com/downloads
   - Used for version control

3. **OpenAI API Account**
   - Sign up at: https://platform.openai.com
   - Obtain an API key from the dashboard
   - Ensure you have credits/billing set up

### Optional (For Local Development)

4. **Python 3.11+**
   - Download: https://www.python.org/downloads/

5. **Node.js 20+**
   - Download: https://nodejs.org/

6. **PostgreSQL 16+**
   - Download: https://www.postgresql.org/download/

## Installation Steps

### Option 1: Docker Compose (Recommended)

This is the fastest way to get started.

#### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd LLM_Agent
```

#### Step 2: Configure Environment Variables

**Backend Configuration:**

```bash
cd backend
cp .env.example .env
```

Edit `backend/.env` and configure:

```env
# Required: OpenAI API Key
OPENAI_API_KEY=sk-your-actual-openai-api-key-here

# Required: Secret key for JWT (generate a secure random string)
SECRET_KEY=your-very-secure-random-secret-key-here

# Optional: Adjust if needed
DEBUG=True
ENVIRONMENT=development
```

**Frontend Configuration:**

```bash
cd ../frontend
cp .env.example .env
```

The default configuration should work, but you can adjust if needed:

```env
VITE_API_URL=http://localhost:8000
```

#### Step 3: Start All Services

From the root directory:

```bash
docker-compose up -d
```

This will:
- Pull required Docker images
- Build the backend and frontend containers
- Start PostgreSQL, Redis, RabbitMQ, and ChromaDB
- Start the backend API server
- Start the frontend development server

Wait for all services to start (usually 1-2 minutes).

#### Step 4: Verify Installation

Check that all containers are running:

```bash
docker-compose ps
```

You should see all services with status "Up":
- clinical_postgres
- clinical_redis
- clinical_rabbitmq
- clinical_backend
- clinical_frontend
- clinical_chromadb

#### Step 5: Initialize the Database

The database schema is automatically created when the backend starts. To verify:

```bash
docker-compose logs backend
```

Look for log messages indicating successful database initialization.

#### Step 6: Access the Application

Open your browser and navigate to:
- **Frontend Application**: http://localhost:5173
- **API Documentation**: http://localhost:8000/api/docs
- **Health Check**: http://localhost:8000/health

### Option 2: Local Development Setup

For development without Docker.

#### Backend Setup

1. **Install PostgreSQL**

```bash
# On macOS with Homebrew
brew install postgresql@16
brew services start postgresql@16

# On Ubuntu/Debian
sudo apt-get install postgresql-16

# On Windows
# Download and install from postgresql.org
```

2. **Create Database**

```bash
psql postgres
CREATE DATABASE clinical_db;
CREATE USER clinical_user WITH PASSWORD 'clinical_pass';
GRANT ALL PRIVILEGES ON DATABASE clinical_db TO clinical_user;
\q
```

3. **Install Redis**

```bash
# On macOS
brew install redis
brew services start redis

# On Ubuntu/Debian
sudo apt-get install redis-server
sudo systemctl start redis

# On Windows
# Download from https://redis.io/download
```

4. **Install RabbitMQ**

```bash
# On macOS
brew install rabbitmq
brew services start rabbitmq

# On Ubuntu/Debian
sudo apt-get install rabbitmq-server
sudo systemctl start rabbitmq-server
```

5. **Set Up Python Backend**

```bash
cd backend

# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Run database migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env

# Start development server
npm run dev
```

## Post-Installation

### Create Your First User

1. Navigate to http://localhost:5173/register
2. Fill in the registration form:
   - Email: admin@example.com
   - Password: (at least 8 characters)
   - Role: Clinician (or Admin)
   - First Name: Your first name
   - Last Name: Your last name
   - Specialty: (if Clinician)
3. Click "Create account"
4. You'll be automatically logged in

### Test the API

You can test the API using the interactive documentation:

1. Navigate to http://localhost:8000/api/docs
2. Click on an endpoint to expand it
3. Click "Try it out"
4. Fill in the required parameters
5. Click "Execute"

### Verify Database

Connect to the database to verify tables were created:

```bash
# Using Docker
docker exec -it clinical_postgres psql -U clinical_user -d clinical_db

# Locally
psql -U clinical_user -d clinical_db

# List tables
\dt

# Expected tables:
# - users
# - user_profiles
# - patients
# - encounters
# - clinical_notes
# - templates
# - agent_tasks
# - fhir_mappings
# - audit_trail
# ... and more
```

## Common Issues and Solutions

### Issue: Port Already in Use

**Error**: "Bind for 0.0.0.0:5432 failed: port is already allocated"

**Solution**:
```bash
# Find what's using the port
sudo lsof -i :5432

# Kill the process or change the port in docker-compose.yml
```

### Issue: OpenAI API Key Error

**Error**: "AuthenticationError: No API key provided"

**Solution**:
- Verify your `.env` file has `OPENAI_API_KEY=sk-...`
- Restart the backend container: `docker-compose restart backend`

### Issue: Frontend Can't Connect to Backend

**Error**: "Network Error" or "CORS Error"

**Solution**:
- Verify backend is running: http://localhost:8000/health
- Check CORS settings in `backend/app/core/config.py`
- Ensure `CORS_ORIGINS` includes `http://localhost:5173`

### Issue: Database Migration Errors

**Error**: "alembic.util.exc.CommandError: Can't locate revision identified by..."

**Solution**:
```bash
# Reset migrations (WARNING: This will delete all data)
docker-compose down -v
docker-compose up -d
```

### Issue: Node Modules Not Found

**Error**: "Cannot find module..."

**Solution**:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## Updating the Application

### Pull Latest Changes

```bash
git pull origin main
```

### Rebuild Containers

```bash
docker-compose down
docker-compose build
docker-compose up -d
```

### Update Dependencies

**Backend:**
```bash
docker-compose exec backend pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

## Stopping the Application

### Stop All Services

```bash
docker-compose down
```

### Stop and Remove All Data

**WARNING**: This will delete all database data!

```bash
docker-compose down -v
```

## Next Steps

After successful installation:

1. **Read the User Guide**: See README.md for usage instructions
2. **Explore the API**: http://localhost:8000/api/docs
3. **Review the Database Schema**: See docs/DATABASE.md
4. **Start Development**: See docs/DEVELOPMENT.md

## Getting Help

If you encounter issues:

1. Check the logs:
   ```bash
   docker-compose logs backend
   docker-compose logs frontend
   ```

2. Verify all services are healthy:
   ```bash
   docker-compose ps
   ```

3. Restart specific services:
   ```bash
   docker-compose restart backend
   ```

4. Open an issue on GitHub with:
   - Error message
   - Relevant logs
   - Steps to reproduce
