# TripMateAI
🌍 Travel & Entertainment Chatbot
A sophisticated AI-powered chatbot that helps users discover travel destinations, find local events, and create personalized itineraries. Built with Streamlit and powered by Ollama LLM, it features user authentication, persistent conversation history, and intelligent travel recommendations.

✨ Features
🤖 AI-Powered Conversations: Ollama LLM integration for intelligent responses

🔐 User Authentication: Secure login/registration system

💾 Persistent Memory: Database-backed conversation history

🎭 Event Discovery: Ticketmaster API integration

🗺️ Travel Planning: Itinerary generation and recommendations

🎨 Modern UI: Beautiful Streamlit interface with custom CSS

🚀 Setup

Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh
ollama serve &

Pull a Model
ollama pull gemma:2b

Install Dependencies
pip install streamlit bcrypt requests python-dotenv


Configure Environment

Create a .env file:
TICKETMASTER_API_KEY=your_api_key_here
DATABASE_URL=sqlite:///travel_bot.db
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=gemma:2b

Run the Application
streamlit run app.py

🎯 Usage
Register/Login: Create an account or login to access the chatbot

Start Chatting: Ask about travel destinations, events, or request itineraries

View History: Access your previous conversations from the sidebar

Get Recommendations: Receive personalized travel and event suggestions

Example Queries:
"Find concerts in New York this weekend"

"Plan a 3-day trip to Paris"

"Best restaurants in Tokyo"

"What events are happening in London next month?"

🗄️ Database Schema
The application uses SQLite with two main tables:

users: User authentication information

 username, email, mobile number, password

chats: Conversation history with message data

username, title, messages, created_at

🔒 Security Features
Password hashing with bcrypt

SQL injection prevention through parameterized queries

Input validation and sanitization

Session-based authentication

Email format validation


📁 Project Structure

travel-chatbot/
├── app.py                 # Main application
├── bot_logic.py          # AI chatbot logic
├── api_handlers.py       # External API handlers
├── database.py           # Database operations
├── config.py             # Configuration settings
├── css_loader.py         # CSS management
└── styles/               # CSS styles directory

📌 Notes
Requires Ollama running locally with a supported model

Ticketmaster API key is optional but enhances event discovery

Conversations are persisted in SQLite database

User authentication ensures private chat histories
