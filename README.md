# The Generators

AI Content Generation API - Generate images, videos, and audio from text using multiple AI providers.

---

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

```bash
# 1. Configure environment
cp env/.env.example env/.env.dev
# Edit env/.env.dev with your API keys

# 2. Start all services
docker-compose up -d

# 3. Check logs
docker-compose logs -f api
```

Server runs at `http://localhost:5000`
Swagger docs at `http://localhost:5000/docs`

### Option 2: Local Development

#### 1. Setup Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

#### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 3. Start Redis (required)

```bash
# Using Docker
docker run -d --name redis -p 6379:6379 redis:7-alpine
```

#### 4. Start PostgreSQL (required)

```bash
# Using Docker
docker run -d --name postgres -p 5432:5432 \
  -e POSTGRES_DB=the_generators \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -v ./db/init:/docker-entrypoint-initdb.d \
  postgres:16-alpine
```

#### 5. Configure Environment

```bash
# Copy example config
cp env/.env.example env/.env.dev

# Edit env/.env.dev and add your API keys
APP_ENV=dev
OPENAI_API_KEY=your_openai_key_here
TEXT_TO_IMAGE_DEFAULT=openai
TEXT_TO_IMAGE_MODELS=openai
TEXT_TO_IMAGE_OPENAI_MODEL=dall-e-3
FLASK_PORT=5000
FLASK_DEBUG=true
OUTPUT_DIR=output
LOG_DIR=src/logs
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Database (PostgreSQL) - loaded via ConfigService
DB_HOST=localhost
DB_PORT=5432
DB_NAME=the_generators
DB_USER=postgres
DB_PASSWORD=postgres
```

#### 6. Run Server

```bash
python src/server/app.py
```

Server runs at `http://localhost:5000`

---

## ✨ Features

| Feature | Status | Providers |
|---------|--------|-----------|
| Text to Image | ✅ Available | OpenAI DALL-E |
| Text to Video | 🔜 Coming Soon | Replicate |
| Text to Speech | 🔜 Coming Soon | OpenAI, ElevenLabs |
| Image to Video | 🔜 Coming Soon | Replicate |

---

## 📡 API Endpoints

### Health Check

```
GET /api/health
```

### Jobs (Global)

```
GET /api/jobs/{job_id}
```

Get job status. Returns `pending`, `processing`, `completed`, or `failed`.

### Text to Image

```
POST /api/text-to-image/generate
GET /api/text-to-image/models
```

---

## 📖 API Documentation (English)

### POST /api/text-to-image/generate

Generate an image from text prompt.

**Request:**
```json
{
  "prompt": "A beautiful sunset over mountains",
  "provider": "openai",
  "size": "1024x1024",
  "quality": "standard"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| prompt | string | Yes | Text description of the image |
| provider | string | No | AI provider (default: from config) |
| size | string | No | Image size: `1024x1024`, `1024x1792`, `1792x1024`, `512x512` |
| quality | string | No | OpenAI only: `standard` or `hd` |

**Response (202 Accepted):**
```json
{
  "status_code": 202,
  "message": "Job submitted",
  "data": {
    "job_id": "abc-123-def",
    "status": "pending"
  }
}
```

### GET /api/jobs/{job_id}

Check job status and get result.

**Response (Processing):**
```json
{
  "status_code": 200,
  "message": "Success",
  "data": {
    "job_id": "abc-123-def",
    "job_type": "text_to_image",
    "status": "processing",
    "result": null
  }
}
```

**Response (Completed):**
```json
{
  "status_code": 200,
  "message": "Success",
  "data": {
    "job_id": "abc-123-def",
    "job_type": "text_to_image",
    "status": "completed",
    "result": {
      "output_url": "/output/images/abc123.png",
      "provider": "openai",
      "model": "dall-e-3"
    }
  }
}
```

### GET /api/text-to-image/models

Get available providers.

**Response:**
```json
{
  "status_code": 200,
  "message": "Success",
  "data": {
    "models": [
      {
        "provider": "openai",
        "model": "dall-e-3",
        "is_default": true
      }
    ]
  }
}
```

---

## 📖 Tài liệu API (Tiếng Việt)

### POST /api/text-to-image/generate

Tạo ảnh từ mô tả văn bản.

**Request:**
```json
{
  "prompt": "Hoàng hôn tuyệt đẹp trên dãy núi",
  "provider": "openai",
  "size": "1024x1024",
  "quality": "standard"
}
```

| Trường | Kiểu | Bắt buộc | Mô tả |
|--------|------|----------|-------|
| prompt | string | Có | Mô tả văn bản của ảnh cần tạo |
| provider | string | Không | Nhà cung cấp AI (mặc định: từ config) |
| size | string | Không | Kích thước: `1024x1024`, `1024x1792`, `1792x1024`, `512x512` |
| quality | string | Không | Chỉ OpenAI: `standard` hoặc `hd` |

**Response (202 Accepted):**
```json
{
  "status_code": 202,
  "message": "Job submitted",
  "data": {
    "job_id": "abc-123-def",
    "status": "pending"
  }
}
```

### GET /api/jobs/{job_id}

Kiểm tra trạng thái job và lấy kết quả.

**Trạng thái:**
- `pending` - Đang chờ xử lý
- `processing` - Đang xử lý
- `completed` - Hoàn thành
- `failed` - Thất bại

**Response (Hoàn thành):**
```json
{
  "status_code": 200,
  "message": "Success",
  "data": {
    "job_id": "abc-123-def",
    "job_type": "text_to_image",
    "status": "completed",
    "result": {
      "output_url": "/output/images/abc123.png",
      "provider": "openai",
      "model": "dall-e-3"
    }
  }
}
```

### GET /api/text-to-image/models

Lấy danh sách providers khả dụng.

**Response:**
```json
{
  "status_code": 200,
  "message": "Success",
  "data": {
    "models": [
      {
        "provider": "openai",
        "model": "dall-e-3",
        "is_default": true
      }
    ]
  }
}
```

---

## 🏗️ Architecture

```
src/
├── common/              # Base classes
├── domain/              # Feature modules
│   └── text_to_image/   # Text to Image feature
│       ├── routes.py
│       ├── service.py
│       ├── validator.py
│       └── strategies/  # AI provider implementations
├── services/            # Shared services
│   ├── config_service.py
│   ├── logger_service.py
│   ├── db_service.py
│   ├── queue_service.py
│   └── worker_service.py
└── server/              # Flask app

db/
├── init/                # Auto-executed on first PostgreSQL start
│   └── 001_initial_schema.sql
├── migrations/          # Incremental schema changes
├── migrate.py           # Migration CLI: python db/migrate.py
└── schema.sql           # Schema reference (read-only)
```

**Design Patterns:**
- Strategy Pattern - Swap AI providers without changing business logic
- Singleton - ConfigService, DatabaseService, QueueService
- Factory - Service creates strategy based on provider

---

## 📝 License

MIT
