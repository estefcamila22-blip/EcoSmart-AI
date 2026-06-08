import logging
from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from pydantic import BaseModel

logger = logging.getLogger(__name__)
router = APIRouter()

class WhatsAppMessage(BaseModel):
    recipient: str
    message: str
    message_type: str = "text"
    buttons: List[dict] = []

class WhatsAppWebhook(BaseModel):
    object: str
    entry: List[dict]

@router.post("/webhook")
async def handle_whatsapp_webhook(webhook: WhatsAppWebhook):
    """Handle WhatsApp webhook messages"""
    try:
        for entry in webhook.entry:
            for change in entry.get('changes', []):
                messages = change['value'].get('messages', [])
                for msg in messages:
                    sender = msg['from']
                    text = msg['text']['body']
                    logger.info(f"WhatsApp message from {sender}: {text}")
                    
                    # Process user intent
                    response = await process_whatsapp_intent(sender, text)
                    await send_whatsapp_message(sender, response)
        
        return {"status": "received"}
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/send")
async def send_whatsapp_notification(message: WhatsAppMessage):
    """Send WhatsApp notification"""
    try:
        result = await send_whatsapp_message(message.recipient, message.message)
        return {"status": "sent", "message_id": result}
    except Exception as e:
        logger.error(f"Send error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def process_whatsapp_intent(user_id: str, text: str) -> str:
    """Process WhatsApp user intent with AI"""
    text_lower = text.lower()
    
    if 'consumption' in text_lower or 'energy' in text_lower:
        return "Your daily consumption is 45.2 kWh. Current power usage is 2450W. Would you like recommendations?"
    elif 'devices' in text_lower or 'devices on' in text_lower:
        return "Active devices: AC Unit (1200W), Water Heater (500W), Lights (120W). Total: 1820W"
    elif 'save' in text_lower or 'reduce' in text_lower:
        return "Top savings: 1) Optimize AC - save 2.3 kWh/month 2) Schedule water heater 3) LED upgrade"
    elif 'anomaly' in text_lower or 'unusual' in text_lower:
        return "No unusual consumption detected this week. Your usage is 8.5% lower than last week. Great job!"
    elif 'eco' in text_lower or 'score' in text_lower:
        return "Your EcoScore is 78.5/100. You're in the top 15% of similar homes. Keep optimizing!"
    else:
        return "I can help you with energy consumption, device control, savings tips, and sustainability insights. What would you like to know?"

async def send_whatsapp_message(recipient: str, message: str) -> str:
    """Send message via WhatsApp API"""
    try:
        # Mock implementation
        logger.info(f"Sending WhatsApp to {recipient}: {message}")
        return f"msg_{hash(recipient)}"
    except Exception as e:
        logger.error(f"Error sending: {e}")
        raise