# Al-La'eeb (اللعيب) - AI Football Talent Intelligence Platform

> **Enterprise-grade, award-winning AI-powered football talent scouting platform** bridging the gap between raw athletic performance and elite professional standards.

## 🏆 Platform Overview

Al-La'eeb is an end-to-end AI platform for football talent identification using:
- **Computer Vision** (OpenCV, MediaPipe) - 33-point skeletal tracking at 30 FPS
- **Machine Learning** (PyTorch, ResNet, U-Net) - 47 distinct performance metrics
- **Natural Language Processing** (GPT-4o, Claude, Gemini) - Arabic/English virtual coach
- **Vector Search** (Qdrant) - 10,000+ FIFA/UEFA professional player benchmarks

## 🏗️ Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Flutter App    │────▶│  API Gateway     │────▶│  Auth Service   │
│  (iOS/Android)  │     │  (FastAPI)       │     │  (JWT + Face)   │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        ▼                      ▼                      ▼
┌──────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ AI Engine    │    │ NLP Coach       │    │ Scout Service   │
│ (CV + ML)    │    │ (500+ Drills)   │    │ (Discovery)     │
└──────────────┘    └─────────────────┘    └─────────────────┘
        │                      │                      │
        ▼                      ▼                      ▼
┌──────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ PostgreSQL   │    │ Qdrant Vector   │    │ Redis Cache     │
│ (Relational) │    │ DB (Embeddings) │    │ (Sessions)      │
└──────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Flutter 3.0+
- NVIDIA GPU (optional, for CV acceleration)

### Local Development

```bash
# 1. Clone and enter directory
cd al-laeeb-platform

# 2. Copy environment variables
cp .env.example .env
# Edit .env with your API keys

# 3. Start all services
docker-compose up --build

# 4. Access services
# API Gateway:    http://localhost:8000
# Auth Service:   http://localhost:8001
# AI Engine:      http://localhost:8003
# NLP Coach:      http://localhost:8004
# PostgreSQL:     localhost:5432
# Redis:          localhost:6379
# Qdrant:         localhost:6333
# Grafana:        http://localhost:3000
# Prometheus:     http://localhost:9090
```

### Flutter Mobile App

```bash
cd frontend
flutter pub get
flutter run
```

## 📁 Project Structure

```
al-laeeb-platform/
├── backend/
│   ├── api-gateway/          # Unified API Gateway (FastAPI)
│   ├── services/
│   │   ├── auth-service/     # JWT + Dual-layer biometric verification
│   │   ├── player-service/   # Player profiles & stats
│   │   ├── video-service/    # Video upload & streaming (RTMP)
│   │   ├── ai-engine/        # CV pipeline, metrics, ball tracking
│   │   ├── nlp-coach/        # Arabic/English virtual coach
│   │   └── scout-service/    # Talent discovery & search
│   └── shared/               # Common models, config, utils
├── frontend/                 # Flutter cross-platform app
├── infrastructure/
│   ├── docker/              # Dockerfiles for all services
│   ├── k8s/                 # Kubernetes manifests
│   ├── terraform/           # AWS EKS infrastructure
│   ├── monitoring/          # Prometheus + Grafana
│   └── nginx/               # Reverse proxy config
└── .github/workflows/       # CI/CD pipelines
```

## 🔐 Core Features

### 1. Dual-Layer Biometric Verification
- **Layer 1**: Facial recognition (InsightFace) - < 2s processing
- **Layer 2**: Kit ID matching (OCR + color histogram)
- **Geofencing**: 50-meter GPS accuracy threshold
- **Anti-fraud**: Liveness detection + spoof prevention

### 2. Computer Vision Engine
- **33 skeletal keypoints** per player at **30 FPS**
- **47 performance metrics**: speed, acceleration, passing, shooting, positioning, biomechanics
- **Ball tracking**: Real-time trajectory analysis
- **Event detection**: Passes, shots, tackles, sprints, interceptions

### 3. AI Virtual Coach
- **Bilingual**: Modern Standard Arabic + Regional dialects + English
- **500+ drill library** with automated weakness mapping
- **Weekly training plans** generated per player
- **Interactive chat** with GPT-4o/Claude integration

### 4. Scout Marketplace
- **Vector similarity search** against 10,000+ professional profiles
- **Player discovery cards** with match scores
- **Geofenced dashboard** for proximity tracking
- **Detailed analytics** with radar charts

## 🛡️ Security

- JWT authentication with refresh tokens
- Role-based access control (RBAC)
- TLS encrypted transport
- Encrypted storage for biometric data
- API rate limiting
- Audit logging

## 📊 Performance SLAs

| Metric | Target |
|--------|--------|
| Dual-layer auth | < 2 seconds |
| 90-min match analysis | < 4 minutes |
| Streaming latency | < 3 seconds |
| Concurrent streams | 1,000+ |
| CV processing FPS | 30 per stream |

## 🚢 Deployment

### Kubernetes
```bash
kubectl apply -f infrastructure/k8s/namespace.yaml
kubectl apply -f infrastructure/k8s/
kubectl rollout status deployment/api-gateway -n allaeeb
```

### Terraform (AWS)
```bash
cd infrastructure/terraform
terraform init
terraform plan
terraform apply
```

## 📈 Monitoring

- **Prometheus**: Metrics collection
- **Grafana**: Dashboards & alerting
- **Health endpoints**: `/api/v1/health/` on all services

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

Confidential / Engineering Handover - Al-La'eeb Platform v1.0.0

## 🙏 Acknowledgments

- FIFA/UEFA professional player database
- MediaPipe for pose estimation
- Qdrant for vector similarity search
- OpenAI/Anthropic for NLP capabilities
