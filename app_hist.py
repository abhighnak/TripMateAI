# app.py
import streamlit as st
from config import Config
from bot_logic import get_travel_bot
import json
import os
from datetime import datetime

class TravelApp:
    def __init__(self):
        self.bot = get_travel_bot()
        self.setup_page()
        self.setup_styles()
        self.chat_history_file = "chat_history.json"
        
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
            background-color: #f5f5f5;
            padding-bottom: 100px;
        }}
        
        /* Sidebar styles */
        .sidebar .sidebar-content {{
            background-color: #ffffff;
        }}
        
        /* Chat history buttons */
        .chat-history-btn {{
            text-align: left;
            padding: 8px 12px;
            margin: 4px 0;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
            background: white;
            width: 100%;
            cursor: pointer;
        }}
        .chat-history-btn:hover {{
            background: #f8fafc;
        }}

        /* Sidebar text color */
        .sidebar .sidebar-content {{
            color: #000000 !important;
        }}
        
        /* Chat history items */
        .chat-history-item {{
            color: #000000 !important;
            padding: 8px;
            margin: 4px 0;
            border-radius: 8px;
            cursor: pointer;
            transition: background-color 0.2s;
        }}
        .chat-history-item:hover {{
            background-color: #f0f0f0;
        }}
        
        /* Timestamp styling */
        .chat-timestamp {{
            font-size: 0.8em;
            color: #666666 !important;
        }}
                        
        /* Delete button */
        .delete-btn {{
            color: #e53e3e;
            background: none;
            border: none;
            cursor: pointer;
            padding: 8px;
        }}
                
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
        
        /* Rest of your existing styles... */
        </style>
        """, unsafe_allow_html=True)

    def load_chat_history(self):
        """Load chat history from file with better error handling"""
        try:
            if os.path.exists(self.chat_history_file):
                with open(self.chat_history_file, 'r') as f:
                    return json.load(f)
            return []
        except json.JSONDecodeError:
            st.error("Error reading chat history - file may be corrupted")
            return []
        except Exception as e:
            st.error(f"Error loading chat history: {str(e)}")
            return []
        
    def save_chat_history(self, history):
        """Save chat history to file with atomic write"""
        try:
            # Write to temporary file first
            temp_file = self.chat_history_file + ".tmp"
            with open(temp_file, 'w') as f:
                json.dump(history, f, indent=2)
            
            # Replace original file
            if os.path.exists(temp_file):
                if os.path.exists(self.chat_history_file):
                    os.remove(self.chat_history_file)
                os.rename(temp_file, self.chat_history_file)
        except Exception as e:
            st.error(f"Error saving chat history: {str(e)}")
        
    def get_chat_title(self, messages):
        """Generate a descriptive title based on conversation content"""
        if len(messages) < 2:
            return "New chat"
        
        # Get the first substantial user message
        for content, is_user in messages[1:]:
            if is_user and len(content.strip()) > 3:
                # Clean the content
                clean_content = content.replace('\n', ' ').strip()
                
                # Extract key information
                location = ""
                purpose = ""
                
                # Check for travel-related queries
                travel_keywords = ["trip", "travel", "visit", "go to", "flight", "itinerary"]
                if any(word in clean_content.lower() for word in travel_keywords):
                    purpose = "Trip"
                
                # Check for event-related queries
                event_keywords = ["event", "concert", "show", "ticket"]
                if any(word in clean_content.lower() for word in event_keywords):
                    purpose = "Event"
                
                # Try to extract location
                location_markers = [" in ", " at ", " to ", " from "]
                for marker in location_markers:
                    if marker in clean_content.lower():
                        parts = clean_content.lower().split(marker)
                        if len(parts) > 1:
                            location = parts[-1].split('.')[0].split('?')[0].strip().title()
                            break
                
                # Format the title
                if purpose and location:
                    return f"{purpose}: {location}"
                elif purpose:
                    return purpose
                elif location:
                    return f"Chat: {location}"
                
                # Fallback to first few words
                return clean_content[:30].strip() + ("..." if len(clean_content) > 30 else "")
        
        return "New chat"

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
        # Initialize session state
        if "messages" not in st.session_state:
            st.session_state.messages = [
                (f"Hi! I'm {Config.BOT_NAME}. {Config.TAGLINE} How can I help you today?", False)
            ]
            st.session_state.current_chat_id = None
            st.session_state.chat_start_time = datetime.now().strftime("%b %d, %H:%M")
        
        # Load chat history
        chat_history = self.load_chat_history()
        
        # Handle chat selection from URL parameters
        query_params = st.query_params
        if "chat" in query_params:
            try:
                chat_id = int(query_params["chat"][0])
                if 0 <= chat_id < len(chat_history):
                    st.session_state.messages = chat_history[chat_id]["messages"]
                    st.session_state.current_chat_id = chat_id
                    st.session_state.chat_start_time = chat_history[chat_id]["timestamp"]
            except (ValueError, IndexError):
                pass
        
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
            
            # Chat history section
            st.header("Chat History")
            
            # New Chat button
            if st.button("➕ New Chat", use_container_width=True):
                st.session_state.messages = [
                    (f"Hi! I'm {Config.BOT_NAME}. {Config.TAGLINE} How can I help you today?", False)
                ]
                st.session_state.current_chat_id = None
                st.session_state.chat_start_time = datetime.now().strftime("%b %d, %H:%M")
                st.query_params.clear()
                st.rerun()
            
            # Clear history button
            if st.button("Clear All History", use_container_width=True):
                try:
                    if os.path.exists(self.chat_history_file):
                        os.remove(self.chat_history_file)
                    st.session_state.messages = [
                        (f"Hi! I'm {Config.BOT_NAME}. {Config.TAGLINE} How can I help you today?", False)
                    ]
                    st.session_state.current_chat_id = None
                    st.query_params.clear()
                    st.rerun()
                except Exception as e:
                    st.error(f"Error clearing history: {str(e)}")
            
            # Display chat history items
            if chat_history:
                for i, chat in enumerate(reversed(chat_history)):
                    chat_id = len(chat_history) - 1 - i  # Maintain correct index after reverse
                    is_active = st.session_state.get("current_chat_id") == chat_id
                    
                    # Create columns for chat item and delete button
                    col1, col2 = st.columns([0.85, 0.15])
                    
                    with col1:
                        # Chat history button
                        if st.button(
                            f"{chat['title']} - {chat['timestamp']}",
                            key=f"history_{chat_id}",
                            use_container_width=True,
                            type="primary" if is_active else "secondary"
                        ):
                            st.session_state.messages = chat["messages"]
                            st.session_state.current_chat_id = chat_id
                            st.session_state.chat_start_time = chat["timestamp"]
                            st.query_params["chat"] = str(chat_id)
                            st.rerun()
                    
                    with col2:
                        # Delete button
                        if st.button("🗑️", key=f"delete_{chat_id}"):
                            try:
                                chat_history.pop(chat_id)
                                self.save_chat_history(chat_history)
                                if st.session_state.get("current_chat_id") == chat_id:
                                    st.session_state.messages = [
                                        (f"Hi! I'm {Config.BOT_NAME}. {Config.TAGLINE} How can I help you today?", False)
                                    ]
                                    st.session_state.current_chat_id = None
                                    st.query_params.clear()
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error deleting chat: {str(e)}")
            else:
                st.info("No previous chats found")
        
        # Main chat interface
        st.markdown(f"""
        <div class='main-container'>
            <div class='header'>
                <h2>{Config.BOT_EMOJI} {Config.BOT_NAME}</h2>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display messages
        st.markdown("<div class='main-container'>", unsafe_allow_html=True)
        for content, is_user in st.session_state.messages:
            self.render_message(content, is_user)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # User input
        user_input = st.chat_input("Ask about places, events, or say 'plan my trip'...")
        if user_input:
            # If this is the first user message, set the chat start time
            if len(st.session_state.messages) == 1:
                st.session_state.chat_start_time = datetime.now().strftime("%b %d, %H:%M")
            
            st.session_state.messages.append((user_input, True))
            try:
                response = self.bot.process_message(user_input)
                st.session_state.messages.append((response, False))
                
                # Create/update chat history
                current_chat = {
                    "timestamp": st.session_state.chat_start_time,
                    "title": self.get_chat_title(st.session_state.messages),
                    "messages": st.session_state.messages
                }
                
                # Update chat history
                chat_history = self.load_chat_history()
                
                # If we're continuing an existing chat
                if st.session_state.current_chat_id is not None:
                    chat_history[st.session_state.current_chat_id] = current_chat
                else:
                    # Add new chat
                    chat_history.append(current_chat)
                    st.session_state.current_chat_id = len(chat_history) - 1
                
                # Limit history size
                if len(chat_history) > 20:
                    chat_history = chat_history[-20:]
                    if st.session_state.current_chat_id is not None:
                        st.session_state.current_chat_id = chat_history.index(current_chat)
                
                self.save_chat_history(chat_history)
                
                st.rerun()
            except Exception as e:
                st.error(f"Error processing message: {str(e)}")
        
    

if __name__ == "__main__":
    try:
        Config.validate_keys()
        app = TravelApp()
        app.run()
    except ValueError as e:
        st.error(f"Configuration error: {str(e)}")
    except Exception as e:
        st.error(f"Application error: {str(e)}")