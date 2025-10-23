# app.py
import streamlit as st
from config import Config
from bot_logic import get_travel_bot

class TravelApp:
    def __init__(self):
        self.bot = get_travel_bot()
        self.setup_page()
        self.setup_styles()
        
    def setup_page(self):
        st.set_page_config(
            page_title=Config.BOT_NAME,
            page_icon=Config.BOT_EMOJI,
            layout="centered",
            initial_sidebar_state="expanded"
        )
        
    def setup_styles(self):
        st.markdown(f"""
        <style>
        /* Main container */
        .stApp {{
            background-color: #000000;
            padding-bottom: 100px;
        }}
        
        /* Chat container */
        .main-container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px 0;
        }}
        
        /* Header */
        .header {{
            text-align: center;
            margin-bottom: 30px;
            color: #2d3748;
        }}
        
        /* Message container */
        .message-container {{
            display: flex;
            margin-bottom: 20px;
            align-items: flex-start;
            max-width:700px;
        }}
        
        /* Avatar */
        .avatar {{
            width: 44px;
            height: 44px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            margin: 0 12px;
            flex-shrink: 0;
        }}
        .bot-avatar {{
            background: #38a169;
            color: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .user-avatar {{
            background: #3182ce;
            color: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        /* Message bubbles */
        .message-bubble {{
            max-width: 95%;
            padding: 16px 20px;
            border-radius: 18px;
            font-size: 16px;
            line-height: 1.6;
            color: #2d3748;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            position: relative;
        }}
        .bot-bubble {{
            background: white;
            border: 1px solid #e2e8f0;
            border-bottom-left-radius: 4px;
            margin-right: 5px;
        }}
        .user-bubble {{
            background: #ebf8ff;
            border: 1px solid #bee3f8;
            border-bottom-right-radius: 4px;
            margin-left: auto;
        }}
        
        /* Input area */
        .stChatInput {{
            position: fixed !important;
            bottom: 0 !important;
            left: 0 !important;
            right: 0 !important;
            background: white !important;
            padding: 15px 0 !important;
            z-index: 100 !important;
            border-top: 1px solid #e2e8f0 !important;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.05) !important;
        }}
        .stChatInput > div {{
            max-width: 750px !important;
            margin: 0 auto !important;
            padding: 0 15px !important;
        }}
        
        /* Markdown formatting */
        .stMarkdown {{
            margin: 0 !important;
        }}
        .stMarkdown p {{
            margin: 0.5em 0 !important;
        }}
        .stMarkdown ul {{
            margin: 0.5em 0 !important;
            padding-left: 24px !important;
        }}
        .stMarkdown li {{
            margin: 0.5em 0 !important;
        }}
        </style>
        """, unsafe_allow_html=True)
        
    def render_message(self, text: str, is_user: bool):
        """Modern message rendering with better spacing"""
        bubble_class = "user-bubble" if is_user else "bot-bubble"
        avatar_class = "user-avatar" if is_user else "bot-avatar"
        avatar_emoji = "🧑" if is_user else "🤖"
        
        st.markdown(f"""
        <div class="message-container">
            <div class="avatar {avatar_class}">
                {avatar_emoji}
            </div>
            <div class="message-bubble {bubble_class}">
                {text}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    def run(self):
        # Sidebar
        with st.sidebar:
            st.header(f"{Config.BOT_EMOJI} About")
            st.markdown(f"""
            **{Config.BOT_NAME}**  
            {Config.TAGLINE}
            
            ✨ **Features:**
            - Travel recommendations
            - Event discovery
            - Itinerary planning
            - Local insights
            """)
        
        # Main chat interface
        st.markdown(f"""
        <div class='main-container'>
            <div class='header'>
                <h2>{Config.BOT_EMOJI} {Config.BOT_NAME}</h2>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = [
                (f"Hi! I'm {Config.BOT_NAME}. {Config.TAGLINE} How can I help you today?", False)
            ]
        
        # Display messages
        st.markdown("<div class='main-container'>", unsafe_allow_html=True)
        for content, is_user in st.session_state.messages:
            self.render_message(content, is_user)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # User input
        user_input = st.chat_input("Ask about places, events, or say 'plan my trip'...")
        if user_input:
            st.session_state.messages.append((user_input, True))
            try:
                response = self.bot.process_message(user_input)
                st.session_state.messages.append((response, False))
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    try:
        Config.validate_keys()
        app = TravelApp()
        app.run()
    except ValueError as e:
        st.error(f"Configuration error: {str(e)}")
    except Exception as e:
        st.error(f"Application error: {str(e)}")