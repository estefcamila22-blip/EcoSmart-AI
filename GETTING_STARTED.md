# Getting Started with ESAI

## ⚡ Quick Installation (5 minutes)

### Step 1: Prerequisites
Make sure you have installed:
- Docker Desktop ([download](https://www.docker.com/products/docker-desktop))
- Git ([download](https://git-scm.com/))
- Code editor (VS Code recommended)

### Step 2: Clone Repository
```bash
git clone https://github.com/estefcamila22-blip/EcoSmart-AI.git
cd EcoSmart-AI
```

### Step 3: Configure Environment
```bash
# Copy example config
cp .env.example .env

# Edit .env with your settings
nano .env  # or use your favorite editor
```

**Minimum required settings:**
```env
ENVIRONMENT=development
OPENAI_API_KEY=sk-...  # Get from https://platform.openai.com
WHATSAPP_ACCESS_TOKEN=...  # Optional, get from Meta Business Platform
```

### Step 4: Start Services
```bash
# Start all containers
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f backend
```

### Step 5: Access ESAI

| Service | URL | Purpose |
|---------|-----|----------|
| **API** | http://localhost:8000 | REST API |
| **Docs** | http://localhost:8000/docs | Interactive API documentation |
| **Dashboard** | http://localhost:3000 | Web dashboard |
| **Adminer** | http://localhost:8080 | Database browser (optional) |

---

## 🧪 Test the System

### Test API Health
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy", "timestamp": "2026-06-08T..."}
```

### Test Energy Endpoint
```bash
curl http://localhost:8000/api/v1/energy/current
```

### View Interactive Docs
Open browser to: http://localhost:8000/docs

You can test all API endpoints directly from this interface!

---

## 💬 WhatsApp Integration (Optional)

To enable WhatsApp notifications:

1. **Get Access Token**
   - Go to [Meta Business Platform](https://business.facebook.com)
   - Create/select your business account
   - Create a WhatsApp Business Account
   - Get your access token and phone ID

2. **Update .env**
```env
WHATSAPP_PHONE_ID=1234567890
WHATSAPP_ACCESS_TOKEN=EAABsxxxxxx...
WHATSAPP_WEBHOOK_TOKEN=your_webhook_token
```

3. **Test WhatsApp Send**
```bash
curl -X POST http://localhost:8000/api/v1/whatsapp/send \\
  -H "Content-Type: application/json" \\
  -d '{
    "recipient": "1234567890",
    "message": "Test message from ESAI",
    "channels": ["whatsapp"]
  }'
```

---

## 🔧 Development Setup

### Backend Development

```bash
# Enter backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Run server (with auto-reload)
python -m uvicorn main:app --reload
```

### Frontend Development

```bash
# Enter frontend directory
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

---

## 📊 Simulated Data

ESAI comes with simulated data for testing. The system will generate:
- Realistic energy consumption patterns
- Device status updates
- Anomalies for testing
- ML predictions

To use real IoT data, connect ESP32 sensors via MQTT (see IoT section).

---

## 🌐 ESP32 IoT Sensor Setup (Optional)

### Hardware
- ESP32 microcontroller
- ACS712 current sensor (or similar)
- DHT22 temperature sensor
- PIR motion sensor
- USB cable for programming

### Firmware Upload

1. **Install Arduino IDE**
   - Download from [arduino.cc](https://www.arduino.cc/en/software)
   - Install ESP32 board support

2. **Configure Firmware**
   - Open `iot/esp32_firmware/esai_sensor.ino`
   - Update WiFi credentials:
     ```cpp
     const char* ssid = "YOUR_WIFI_SSID";
     const char* password = "YOUR_WIFI_PASSWORD";
     const char* mqtt_server = "YOUR_MQTT_BROKER_IP";
     ```

3. **Upload to ESP32**
   - Connect ESP32 via USB
   - Select board: "ESP32 Dev Module"
   - Select port: COM3 (Windows) or /dev/ttyUSB0 (Linux/Mac)
   - Click Upload

4. **Verify Connection**
   ```bash
   # Check MQTT messages
   mosquitto_sub -h localhost -t "esai/devices/+/data"
   ```

---

## 🧪 Run Tests

### Unit Tests
```bash
cd backend
pytest tests/test_integration.py -v
```

### Test Coverage
```bash
pytest --cov=. tests/
```

### Test Specific Endpoint
```bash
pytest tests/test_integration.py::TestEnergyEndpoints::test_get_current_consumption -v
```

---

## 📚 Documentation Shortcuts

| Document | Purpose |
|----------|----------|
| [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) | Complete feature overview |
| [docs/ESAI_VIRTUAL_ASSISTANT.md](docs/ESAI_VIRTUAL_ASSISTANT.md) | AI assistant details |
| [docs/DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md) | Production deployment |
| [architecture.md](architecture.md) | System architecture |
| [README.md](README.md) | Project overview |

---

## 🐛 Troubleshooting

### Issue: Containers won't start
```bash
# Check logs
docker-compose logs backend

# Rebuild containers
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Issue: Database connection error
```bash
# Check if PostgreSQL is running
docker-compose logs postgres

# Reset database
docker-compose down -v
docker-compose up -d postgres
sleep 10  # Wait for initialization
docker-compose up -d
```

### Issue: API not responding
```bash
# Check if backend is healthy
curl http://localhost:8000/health

# View backend logs
docker-compose logs -f backend

# Restart backend
docker-compose restart backend
```

### Issue: MQTT not receiving data
```bash
# Check MQTT broker
docker-compose logs mosquitto

# Test MQTT connection
mosquitto_pub -h localhost -t test -m "hello"
mosquitto_sub -h localhost -t "#"
```

---

## 🚀 Next Steps

1. **Explore the Dashboard**
   - Open http://localhost:3000
   - Check real-time energy data
   - View recommendations

2. **Test API Endpoints**
   - Open http://localhost:8000/docs
   - Try different endpoints
   - Understand data structure

3. **Setup WhatsApp Integration**
   - Get access token from Meta
   - Configure .env
   - Test WhatsApp notifications

4. **Connect IoT Devices**
   - Flash ESP32 firmware
   - Configure WiFi and MQTT
   - Monitor sensor data

5. **Customize for Your Home**
   - Add your devices
   - Create automation rules
   - Set preferences

---

## 💡 Common Commands

```bash
# View all containers
docker-compose ps

# View logs for specific service
docker-compose logs backend
docker-compose logs frontend
docker-compose logs postgres

# Stop all services
docker-compose down

# Stop and remove volumes (clean slate)
docker-compose down -v

# Restart a service
docker-compose restart backend

# Execute command in container
docker-compose exec backend bash
docker-compose exec postgres psql -U esai

# View resource usage
docker stats

# Check network
docker-compose exec backend ping postgres
```

---

## 🎯 Quick Reference

**Default Credentials:**
- Database User: `esai`
- Database Password: `esai_password`
- API Base URL: `http://localhost:8000`
- API Prefix: `/api/v1`

**Ports:**
- API Backend: 8000
- React Frontend: 3000
- PostgreSQL: 5432
- Redis: 6379
- MQTT: 1883
- InfluxDB: 8086

**Useful URLs:**
- Swagger Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

---

## 📞 Support

If you encounter issues:

1. Check the [troubleshooting section](#troubleshooting) above
2. Review logs: `docker-compose logs -f`
3. Open an issue: [GitHub Issues](https://github.com/estefcamila22-blip/EcoSmart-AI/issues)
4. Read documentation: [docs/](docs/)

---

**Welcome to ESAI! Happy energy optimization!** 🌱⚡