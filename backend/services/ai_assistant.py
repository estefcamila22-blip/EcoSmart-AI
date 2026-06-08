"""ESAI AI Assistant - Natural Language Processing Module"""
import logging
from typing import Optional, Dict, List
from datetime import datetime
import openai

logger = logging.getLogger(__name__)

class ESAIAssistant:
    """ESAI AI-powered virtual assistant"""
    
    def __init__(self, api_key: str):
        openai.api_key = api_key
        self.system_prompt = """
        You are ESAI, an intelligent sustainable energy management assistant.
        Your role is to help users optimize their energy consumption, provide sustainability insights,
        and make smart automation recommendations.
        
        Be friendly, professional, and eco-conscious. Provide specific, actionable advice.
        Always consider energy efficiency, cost savings, and environmental impact.
        """
    
    async def process_user_query(self, user_id: str, query: str, context: Dict = None) -> Dict:
        """Process user query with AI"""
        try:
            # Build context for AI
            context_str = ""
            if context:
                context_str = f"""
                Current energy data:
                - Power consumption: {context.get('power_w', 0)}W
                - Daily usage: {context.get('daily_kwh', 0)} kWh
                - EcoScore: {context.get('eco_score', 0)}/100
                - Active devices: {context.get('devices', [])}
                """
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"{context_str}\n\nUser query: {query}"}
                ],
                temperature=0.7,
                max_tokens=500,
            )
            
            assistant_response = response.choices[0].message.content
            logger.info(f"AI response generated for user {user_id}")
            
            return {
                "status": "success",
                "response": assistant_response,
                "timestamp": datetime.utcnow(),
            }
        except Exception as e:
            logger.error(f"AI processing error: {e}")
            return {
                "status": "error",
                "response": "I'm having trouble processing your request. Please try again.",
                "error": str(e),
            }
    
    async def generate_recommendations(
        self,
        user_id: str,
        consumption_data: Dict,
        device_list: List[str],
    ) -> List[Dict]:
        """Generate AI-powered recommendations"""
        try:
            prompt = f"""
            Based on this energy consumption data, provide 3 specific, actionable recommendations
            to reduce energy consumption and carbon footprint:
            
            Consumption data: {consumption_data}
            Active devices: {device_list}
            
            For each recommendation, provide:
            1. Title
            2. Description
            3. Estimated monthly savings (kWh and $)
            4. Implementation difficulty (easy/moderate/hard)
            5. Priority (high/medium/low)
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=1000,
            )
            
            logger.info(f"Generated recommendations for user {user_id}")
            return {
                "status": "success",
                "recommendations": response.choices[0].message.content,
            }
        except Exception as e:
            logger.error(f"Recommendation generation error: {e}")
            return {"status": "error", "error": str(e)}
    
    async def analyze_consumption_pattern(
        self,
        user_id: str,
        historical_data: List[Dict],
    ) -> Dict:
        """Analyze consumption patterns with AI"""
        try:
            prompt = f"""
            Analyze this energy consumption pattern and provide insights:
            - Identify peak consumption times
            - Highlight unusual patterns
            - Suggest optimization opportunities
            - Compare with typical household patterns
            
            Data: {historical_data}
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=1000,
            )
            
            logger.info(f"Analyzed consumption pattern for user {user_id}")
            return {
                "status": "success",
                "analysis": response.choices[0].message.content,
            }
        except Exception as e:
            logger.error(f"Pattern analysis error: {e}")
            return {"status": "error", "error": str(e)}