# bot_logic.py
import json
import google.generativeai as genai
from typing import Dict, Any
from config import Config
from api_handlers import APIHandler

class TravelBot:
    def __init__(self):
        self.api = APIHandler()
        self.model = self._initialize_model()
        
    def _initialize_model(self):
        """Initialize the Gemini model with proper error handling"""
        try:
            genai.configure(api_key=Config.GEMINI_API_KEY)
            return genai.GenerativeModel("gemini-1.5-flash")
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Gemini model: {str(e)}")
    
    def _classify_intent(self, message: str) -> Dict[str, Any]:
        """Classify user intent using Gemini"""
        prompt = f"""Analyze this travel/entertainment query and return JSON:
{{
  "intent": "places|events|itinerary|chat",
  "keyword": "main topic",
  "city": "location if mentioned",
  "dates": "timeframe if mentioned",
  "notes": "additional context"
}}

Query: {message}"""
        
        try:
            response = self.model.generate_content(prompt)
            result = json.loads(response.text.strip().strip("`").replace("json\n", ""))
            return result
        except Exception:
            return self._basic_intent_analysis(message)
    
    def _basic_intent_analysis(self, message: str) -> Dict[str, Any]:
        """Fallback intent analysis"""
        message_lower = message.lower()
        intent = "chat"
        keyword = ""
        
        if any(k in message_lower for k in ["restaurant", "food", "cafe", "hotel", "attraction"]):
            intent = "places"
            keyword = "places to visit"
        elif any(k in message_lower for k in ["event", "concert", "show", "ticket"]):
            intent = "events"
            keyword = "events"
        elif any(k in message_lower for k in ["itinerary", "plan", "trip", "schedule"]):
            intent = "itinerary"
            keyword = "itinerary"
            
        return {
            "intent": intent,
            "keyword": keyword,
            "city": None,
            "dates": None,
            "notes": ""
        }
    
    def _generate_places_response(self, keyword: str, city: str) -> str:
        """Generate recommendations for places"""
        prompt = f"""Provide detailed recommendations for {keyword}{f' in {city}' if city else ''}.
Include:
- 5-8 diverse options (attractions, restaurants, etc.)
- Brief descriptions (1-2 sentences each)
- Notable features or specialties
- Format as markdown bullet points with **bold** names"""
        
        response = self.model.generate_content(prompt)
        return response.text or "I couldn't find any recommendations at this time."
    
    def _generate_itinerary(self, city: str, duration: str) -> str:
        """Generate a travel itinerary"""
        prompt = f"""Create a {duration or '1-day'} itinerary for {city or 'a city'}.
Include:
- Morning, afternoon, evening activities
- Meal suggestions
- Travel tips
- Estimated times
Format as a clear schedule with time slots in markdown"""
        
        response = self.model.generate_content(prompt)
        return response.text or "I couldn't generate an itinerary at this time."
    
    def process_message(self, message: str) -> str:
        """Process user message and return bot response"""
        try:
            intent_data = self._classify_intent(message)
            intent = intent_data.get("intent", "chat")
            
            if intent == "events":
                return self._handle_events(intent_data)
            elif intent == "places":
                return self._handle_places(intent_data)
            elif intent == "itinerary":
                return self._handle_itinerary(intent_data)
            else:
                return self._handle_chat(message)
                
        except Exception as e:
            return f"⚠️ Sorry, I encountered an error: {str(e)}"
    
    def _handle_events(self, intent_data: Dict[str, Any]) -> str:
        """Handle event-related queries"""
        classification = intent_data.get("keyword", "events")
        city = intent_data.get("city")
        
        events = self.api.ticketmaster_search(
            keyword=classification,
            city=city
        )
        
        if not events:
            return f"🎭 No {classification} events found{f' in {city}' if city else ''}."
            
        events_list = "\n".join(
            f"- **[{e['title']}]({e['url']})** on {e['start']}"
            for e in events[:6]  # Limit to 6 events
        )
        
        return f"""🎟️ **Upcoming {classification} events{f' in {city}' if city else ''}:**
        
{events_list}

*Click event names for more details*"""
    
    def _handle_places(self, intent_data: Dict[str, Any]) -> str:
        """Handle place recommendations"""
        return self._generate_places_response(
            keyword=intent_data.get("keyword", "places to visit"),
            city=intent_data.get("city")
        )
    
    def _handle_itinerary(self, intent_data: Dict[str, Any]) -> str:
        """Handle itinerary requests"""
        return self._generate_itinerary(
            city=intent_data.get("city"),
            duration=intent_data.get("dates", "1-day")
        )
    
    def _handle_chat(self, message: str) -> str:
        """Handle general conversation"""
        prompt = f"""You're a travel assistant. Respond helpfully to:
{message}
Keep response concise (1-2 paragraphs max) and travel-focused."""
        
        response = self.model.generate_content(prompt)
        return response.text or "I'm here to help with travel and entertainment questions!"
    
# Singleton instance
travel_bot = TravelBot()

# Helper function to maintain compatibility with app.py
def get_travel_bot() -> TravelBot:
    """Get the singleton bot instance"""
    return travel_bot