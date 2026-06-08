"""ESAI Deployment Guide and Production Setup"""

# ESAI Production Deployment Guide

## Prerequisites
- Docker & Docker Compose
- Kubernetes cluster (for large-scale)
- AWS/GCP account
- PostgreSQL 13+
- Node.js 16+

## Local Development

```bash
# Clone repository
git clone https://github.com/estefcamila22-blip/EcoSmart-AI.git
cd EcoSmart-AI

# Setup environment
cp .env.example .env
# Edit .env with your configuration

# Start services
docker-compose up -d

# Initialize database
python backend/db_init.py

# Install frontend dependencies
cd frontend
npm install
npm run dev

# Backend API will be at http://localhost:8000
# Frontend at http://localhost:3000
# API Docs at http://localhost:8000/docs
```

## Docker Deployment

```bash
# Build image
docker build -t esai:latest .

# Run container
docker run -p 8000:8000 \\
  -e DATABASE_URL=postgresql://user:pass@host/db \\
  -e REDIS_URL=redis://host:6379 \\
  -e MQTT_BROKER=host \\
  -e OPENAI_API_KEY=sk-xxx \\
  -e WHATSAPP_ACCESS_TOKEN=xxx \\
  esai:latest
```

## Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: esai-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: esai-backend
  template:
    metadata:
      labels:
        app: esai-backend
    spec:
      containers:
      - name: esai-backend
        image: esai:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: esai-secrets
              key: database_url
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: esai-service
spec:
  selector:
    app: esai-backend
  type: LoadBalancer
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
```

## AWS Deployment

### ECS Fargate
```bash
# Create task definition
aws ecs register-task-definition \\
  --family esai-task \\
  --network-mode awsvpc \\
  --requires-compatibilities FARGATE \\
  --cpu 512 \\
  --memory 1024 \\
  --container-definitions file://task-def.json

# Create service
aws ecs create-service \\
  --cluster esai-cluster \\
  --service-name esai-service \\
  --task-definition esai-task \\
  --desired-count 2 \\
  --launch-type FARGATE
```

### RDS PostgreSQL
```bash
aws rds create-db-instance \\
  --db-instance-identifier esai-db \\
  --db-instance-class db.t3.micro \\
  --engine postgres \\
  --master-username esai \\
  --allocated-storage 20
```

## Configuration Management

### Environment Variables
```bash
# Core
ENVIRONMENT=production
DEBUG=false

# Database
DATABASE_URL=postgresql://user:pass@host:5432/esai
DATABASE_POOL_SIZE=20

# Cache
REDIS_URL=redis://host:6379/0
REDIS_CACHE_TTL=3600

# MQTT
MQTT_BROKER=mqtt.example.com
MQTT_PORT=8883
MQTT_USERNAME=esai
MQTT_PASSWORD=secure_password
MQTT_TLS=true

# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4

# WhatsApp
WHATSAPP_PHONE_ID=...
WHATSAPP_ACCESS_TOKEN=...
WHATSAPP_WEBHOOK_TOKEN=...

# Blockchain
POLYGON_RPC_URL=https://polygon-rpc.com
POLYGON_PRIVATE_KEY=...

# Security
SECRET_KEY=generate-secure-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Monitoring
LOG_LEVEL=INFO
METRICS_ENABLED=true
METRICS_PORT=9090
```

## Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "Add user table"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Monitoring & Logging

### Prometheus Metrics
```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'esai'
    static_configs:
      - targets: ['localhost:9090']
```

### ELK Stack
```bash
# Start ELK
docker run -d --name elasticsearch \\
  -e "discovery.type=single-node" \\
  docker.elastic.co/elasticsearch/elasticsearch:8.0.0

docker run -d --name kibana \\
  -p 5601:5601 \\
  docker.elastic.co/kibana/kibana:8.0.0
```

## Performance Optimization

### Database Indexes
```sql
CREATE INDEX idx_consumption_timestamp ON energy_readings(timestamp DESC);
CREATE INDEX idx_device_user ON devices(user_id, device_type);
CREATE INDEX idx_automation_enabled ON automations(enabled, user_id);
```

### Caching Strategy
```python
# Cache energy readings for 5 minutes
cache.set(f'energy_current_{user_id}', data, ttl=300)

# Cache user preferences for 1 hour
cache.set(f'preferences_{user_id}', prefs, ttl=3600)
```

## Security Best Practices

1. **HTTPS Only**: Use TLS 1.3
2. **API Keys**: Rotate regularly
3. **Database**: Encrypted connections
4. **Secrets**: Use AWS Secrets Manager
5. **Firewalls**: Restrict MQTT to whitelist IPs
6. **Rate Limiting**: 100 req/min per user

## CI/CD Pipeline

```yaml
# GitHub Actions
name: CI/CD
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: pytest backend/tests
      - name: Build Docker image
        run: docker build -t esai:${{ github.sha }} .
      - name: Push to registry
        run: docker push esai:${{ github.sha }}
```

## Troubleshooting

### MQTT Connection Issues
```bash
# Test MQTT connection
mosquitto_pub -h broker -u user -P pass -t test -m "hello"

# Check broker logs
docker logs mosquitto
```

### Database Connection
```bash
# Test connection
psql $DATABASE_URL -c "SELECT 1"

# Check migrations
alembic current
```

### API Health Check
```bash
curl http://localhost:8000/health
curl http://localhost:8000/docs  # Interactive API docs
```

---

**ESAI: Enterprise-Ready Energy Management System**