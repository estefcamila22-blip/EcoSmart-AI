"""Complete Integration Testing Suite"""
import pytest
from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)

class TestEnergyEndpoints:
    """Test energy management endpoints"""
    
    def test_get_current_consumption(self):
        response = client.get("/api/v1/energy/current")
        assert response.status_code == 200
        data = response.json()
        assert "timestamp" in data
        assert "total_power_w" in data
        assert data["total_power_w"] > 0
    
    def test_get_energy_stats(self):
        response = client.get("/api/v1/energy/stats?days=7")
        assert response.status_code == 200
        data = response.json()
        assert data["device_count"] > 0
        assert data["total_consumption"] > 0
    
    def test_record_energy_reading(self):
        payload = {
            "timestamp": "2026-06-08T10:00:00",
            "consumption_kwh": 2.5,
            "device_id": "device_123",
            "room": "living_room",
            "power_factor": 0.95
        }
        response = client.post("/api/v1/energy/reading", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "recorded"

class TestDeviceEndpoints:
    """Test device management endpoints"""
    
    def test_list_devices(self):
        response = client.get("/api/v1/devices/list")
        assert response.status_code == 200
        devices = response.json()
        assert isinstance(devices, list)
        assert len(devices) > 0
    
    def test_get_device(self):
        response = client.get("/api/v1/devices/light_001")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "light_001"
        assert "status" in data
    
    def test_turn_on_device(self):
        response = client.post("/api/v1/devices/light_001/turn-on")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "executed"
        assert data["action"] == "turn_on"
    
    def test_turn_off_device(self):
        response = client.post("/api/v1/devices/light_001/turn-off")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "executed"
        assert data["action"] == "turn_off"

class TestAutomationEndpoints:
    """Test automation endpoints"""
    
    def test_list_automation_rules(self):
        response = client.get("/api/v1/automation/rules")
        assert response.status_code == 200
        rules = response.json()
        assert isinstance(rules, list)
    
    def test_create_automation_rule(self):
        payload = {
            "name": "Test Rule",
            "description": "Test automation",
            "trigger": {"type": "occupancy", "value": "empty"},
            "condition": {"type": "time"},
            "action": {"type": "turn_off", "devices": ["light_*"]},
            "enabled": True,
            "priority": 1
        }
        response = client.post("/api/v1/automation/rules", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
    
    def test_get_automation_suggestions(self):
        response = client.get("/api/v1/automation/suggestions")
        assert response.status_code == 200
        data = response.json()
        assert "suggestions" in data

class TestAnalyticsEndpoints:
    """Test analytics endpoints"""
    
    def test_get_dashboard(self):
        response = client.get("/api/v1/analytics/dashboard")
        assert response.status_code == 200
        data = response.json()
        assert "current_consumption_w" in data
        assert "eco_score" in data
    
    def test_get_eco_score(self):
        response = client.get("/api/v1/analytics/eco-score")
        assert response.status_code == 200
        data = response.json()
        assert 0 <= data["score"] <= 100
    
    def test_get_carbon_footprint(self):
        response = client.get("/api/v1/analytics/carbon-footprint")
        assert response.status_code == 200
        data = response.json()
        assert "total_carbon_kg" in data

class TestNotificationEndpoints:
    """Test notification endpoints"""
    
    def test_get_notifications(self):
        response = client.get("/api/v1/notifications/")
        assert response.status_code == 200
        notifications = response.json()
        assert isinstance(notifications, list)
    
    def test_send_test_notification(self):
        response = client.post("/api/v1/notifications/send-test",
                             json={"channels": ["whatsapp"]})
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "sent"

class TestHealthEndpoints:
    """Test health check endpoints"""
    
    def test_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_readiness_check(self):
        response = client.get("/health/ready")
        assert response.status_code == 200
        data = response.json()
        assert data["ready"] is True

class TestIntegration:
    """Integration tests"""
    
    def test_full_energy_workflow(self):
        """Test complete energy monitoring workflow"""
        # Get current consumption
        response = client.get("/api/v1/energy/current")
        assert response.status_code == 200
        
        # Get stats
        response = client.get("/api/v1/energy/stats")
        assert response.status_code == 200
        
        # Get forecast
        response = client.get("/api/v1/energy/forecast?hours=24")
        assert response.status_code == 200
    
    def test_device_automation_workflow(self):
        """Test device control and automation workflow"""
        # List devices
        response = client.get("/api/v1/devices/list")
        assert response.status_code == 200
        
        # Get automations
        response = client.get("/api/v1/automation/rules")
        assert response.status_code == 200
        
        # Get suggestions
        response = client.get("/api/v1/automation/suggestions")
        assert response.status_code == 200

if __name__ == "__main__":
    pytest.main([__file__, "-v"])