# Emotional Support AI 🤖💛

A **Flask-based AI chatbot** that provides **empathetic emotional support** using natural language processing. This application detects user emotions, responds with personalized messages based on selected personality traits, provides coping suggestions, and tracks conversations over time.

---

## 🌟 Features

### Core Features
- **Granular Emotion Detection**: Detects emotions including *happy, sad, anxious, angry, neutral* using keyword matching and TextBlob sentiment analysis
- **Adaptive Response System**: Four distinct AI personalities (empathetic, funny, motivational, calm) for personalized interactions
- **Multi-User Support**: User authentication system with individual conversation history
- **Coping Suggestions**: Provides context-aware tips for managing different emotional state
- **Conversation History**: Persistent chat history with automatic saving (last 100 messages)
- **Statistics Tracking**: Global and per-user statistics for conversations and emotions
- **Crisis Detection**: Automatic detection of crisis keywords with immediate resource referral

### Advanced AI Features
- **Google AI Gemini Integration**: Optional integration with Google Gemini for advanced AI responses
- **Hugging Face Integration**: Optional integration with Hugging Face Inference API for NLP tasks
- **Sentiment Analysis**: TextBlob-powered sentiment analysis with confidence scores

### User Experience
- **Modern Dark Theme**: Beautiful, accessible dark mode UI with smooth animations
- **Real-time Chat Interface**: Instant responses with typing indicators
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Personalized Avatars**: Visual feedback for different emotions and personalities
- **Mandatory Disclaimer**: 60-second wait timer before accessing the application

### Technical Features
- **RESTful API**: Clean API endpoints for all operations
- **User Authentication**: Secure registration and login system with password hashing
- **Session Management**: Secure user sessions with auto-generated secret keys
- **Error Handling**: Graceful error pages and validation
- **Local Storage**: Data stored locally in SQLite and JSON files for privacy
- **API Configuration**: python-dotenv for secure API credential management

---

## 📸 Demo

**Example Conversations:**

| User Input | Detected Emotion | AI Response (Empathetic) |
|------------|------------------|--------------------------|
| "I'm feeling lonely today" | sad | "I'm here for you. It seems like you're going through a difficult time. 🤗 💡 Tip: Take a deep breath" |
| "I got a promotion at work!" | happy | "That's wonderful! I'm so happy for you! 💛" |
| "I'm so stressed about the exam" | anxious | "Take a deep breath. I understand this feels overwhelming. 💛 💡 Tip: Try meditation" |
| "This is so frustrating!" | angry | "It's completely okay to feel angry. Let it out, I'm listening. 😌 💡 Tip: Count to 10" |

---

## 🛠 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Start

1. **Clone the repository:**
```bash
git clone https://github.com/YOUR_USERNAME/Emotional-Support-Model.git
cd Emotional-Support-Model
```

2. **Create and activate virtual environment (recommended):**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure API keys (Optional - for advanced AI features):**
```bash
# Copy the example environment file
copy env\.env.example env\.env

# Edit env/.env and add your API keys:
# HF_TOKEN=your_huggingface_token
# GOOGLE_TOKEN=your_google_ai_key
```

5. **Run the application:**
```bash
python app.py
```

6. **Open in browser:**
Navigate to `http://localhost:5000`

---

## 📁 Project Structure

```
Emotional-Support-Model/
├── app.py                      # Main Flask application
├── auth.py                     # Authentication blueprint (login/register)
├── chatbot.py                  # AI response generation logic
├── emotion_detector.py         # Emotion detection using NLP
├── config.py                   # Application configuration
├── models.py                   # SQLAlchemy database models
├── requirements.txt            # Python dependencies
├── coping_suggestions.json     # Context-aware coping tips
├── training_data.json          # Intent patterns and responses
├── wsgi.py                     # WSGI entry point
│
├── apis/                       # API Integration modules
│   ├── __init__.py            # Package initialization
│   ├── api_config.py          # Configuration management
│   ├── google_ai.py           # Google AI Gemini integration
│   ├── huggingface_api.py     # Hugging Face integration
│   └── demo.py                # API demonstration script
│
├── env/                        # Environment configuration
│   ├── .env.example           # Environment template
│   └── .env                   # Actual environment (not committed)
│
├── templates/                  # HTML templates
│   ├── base.html              # Base template with navigation
│   ├── index.html             # Landing page
│   ├── chat.html              # Chat interface
│   ├── login.html             # Login page
│   ├── register.html          # Registration page
│   ├── disclaimer.html        # Mandatory disclaimer page
│   └── error.html             # Error pages
│
├── static/                    # Static assets
│   ├── css/
│   │   └── style.css          # Main stylesheet
│   └── js/
│       └── main.js            # Client-side JavaScript
│
├── data/                      # Application data
│   ├── app.db                 # SQLite database
│   └── statistics.json        # Usage statistics
│
├── users/                     # User data storage
│   └── {username}.json        # Individual user chat histories
│
└── LICENSE                    # MIT License
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the `env/` directory:

```env
# Required for basic functionality
SECRET_KEY=your-secret-key-here

# Optional - for advanced AI features
HF_TOKEN=your_huggingface_token
GOOGLE_TOKEN=your_google_ai_key
```

### API Configuration

This project supports optional integration with external AI services:

#### Hugging Face API
1. Get your token from: https://huggingface.co/settings/tokens
2. Add to `env/.env`: `HF_TOKEN=your_token_here`

#### Google AI (Gemini)
1. Get your API key from: https://aistudio.google.com/app/apikey
2. Add to `env/.env`: `GOOGLE_TOKEN=your_api_key_here`

### AI Personalities

| Personality | Description | Best For |
|-------------|-------------|----------|
| empathetic | Understanding and patient listener | Venting, seeking validation |
| funny | Light-hearted and humorous | Lifting mood, casual chat |
| motivational | Encouraging and inspiring | Seeking motivation, goals |
| calm | Peaceful and grounding | Anxiety, stress relief |

---

## 📡 API Endpoints

### Web Routes

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Landing page (with disclaimer) |
| `/chat` | GET | Chat interface (requires login) |
| `/login` | GET/POST | User login |
| `/register` | GET/POST | User registration |
| `/logout` | GET | Logout and clear session |
| `/accept-disclaimer` | POST | Accept disclaimer and start timer |
| `/check-disclaimer` | GET | Check disclaimer status |

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/set_user` | POST | Set username and personality |
| `/api/chat` | POST | Send message, get AI response |
| `/api/history` | GET | Get user's chat history |
| `/api/history/clear` | POST | Clear user's chat history |
| `/api/stats` | GET | Get global statistics |
| `/api/user_stats` | GET | Get user's statistics |

### API Examples

**Set User:**
```bash
curl -X POST http://localhost:5000/api/set_user \
  -H "Content-Type: application/json" \
  -d '{"username": "John", "personality": "empathetic"}'
```

**Send Message:**
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I feel sad today"}'
```

**Response:**
```json
{
  "success": true,
  "message": "I'm here for you. It seems like you're going through a difficult time. 🤗\n\n💡 Tip: Take a deep breath",
  "emotion": "sad",
  "timestamp": "2026-03-11T10:00:00.000000"
}
```

---

## 🧠 How It Works

### Emotion Detection
1. **Keyword Matching**: First checks for emotion-specific keywords with intensity modifiers
2. **Negation Handling**: Detects negations like "not happy"
3. **Sentiment Analysis**: Falls back to TextBlob polarity scoring
4. **Classification**: Maps sentiment scores to emotion categories

### Response Generation
1. **Crisis Detection**: First checks for crisis keywords
2. **Intent Matching**: Checks training data for matching patterns
3. **Emotion Detection**: Analyzes user input for emotional content
4. **Personality Selection**: Applies selected personality tone
5. **Context Enhancement**: Adds coping tips for negative emotions
6. **History Saving**: Stores conversation in user history

### Disclaimer System
1. **Initial Visit**: Users see mandatory disclaimer page
2. **Timer**: 60-second countdown prevents immediate access
3. **Acceptance**: Button enabled after timer completes
4. **Session**: Disclaimer status stored in session
5. **Enforcement**: Both landing page and chat enforce disclaimer

### Data Flow
```
User Input → Crisis Check → Emotion Detection → Intent Matching → Personality Response → Add Coping Tips → Save to History → Return Response
```

---

## 🛠️ Technologies Used

### Backend
- **Flask** (3.1.2) - Web framework
- **Flask-Login** - User authentication
- **Flask-SQLAlchemy** - Database ORM
- **TextBlob** (0.19.0) - Natural language processing
- **NLTK** (3.9.3) - Additional NLP capabilities
- **Werkzeug** - Password hashing
- **python-dotenv** - Environment variable management
- **requests** - HTTP client for API calls
- **Python** - Core language

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with CSS variables
- **JavaScript (ES6+)** - Client-side interactivity
- **Font Awesome** - Icon library
- **Google Fonts** - Typography (Poppins)

### External APIs (Optional)
- **Google AI Gemini** - Advanced text generation
- **Hugging Face** - NLP tasks (sentiment, summarization, translation)

---

## 🔒 Privacy & Security

- All conversation data is stored locally on your machine
- User passwords are securely hashed using Werkzeug
- SQLite database for user accounts
- JSON files for chat history (per user)
- Optional API integrations are opt-in only
- Session-based disclaimer tracking

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ⚠️ Disclaimer

> **Important:** This AI companion is designed to provide emotional support and is NOT a substitute for professional mental health care. If you're experiencing a mental health crisis or need immediate help, please contact a qualified mental health professional or crisis hotline in your area.

### Mandatory Disclaimer Page

Upon first visiting the application, users must:
1. Read the mental health disclaimer
2. Read the API usage notice
3. Wait 60 seconds before proceeding
4. Accept the terms to access the application

This is a legal requirement to ensure users understand the limitations of the AI system.

### API Usage Disclaimer

This application integrates with external AI services provided by **Google AI (Gemini)** and **Hugging Face**. By using these features:

1. **Data Transmission**: Your messages may be transmitted to these third-party AI providers for processing. Review their respective privacy policies:
   - [Google AI Privacy Policy](https://policies.google.com/privacy)
   - [Hugging Face Privacy Policy](https://huggingface.co/privacy)

2. **API Costs**: Some features may incur costs based on usage. Users are responsible for managing their own API quotas and billing.

3. **Service Availability**: External API services may experience downtime or rate limiting. The application is not responsible for service interruptions.

4. **Content Moderation**: AI-generated responses are generated by third-party models and may not always be appropriate. Users should exercise judgment and not rely on AI responses for critical decisions.

5. **Terms of Service**: By using this application, you agree to comply with the Terms of Service of both Google AI and Hugging Face.

### Liability

The developers of this project are not liable for:
- Any damages arising from the use of AI-generated responses
- Decisions made based on AI suggestions
- Third-party API service disruptions
- Any breach of data when transmitting to external services

---

## 🙏 Acknowledgments

- TextBlob for sentiment analysis
- NLTK for natural language processing
- Font Awesome for icons
- Google Fonts for typography
- Google AI for Gemini API
- Hugging Face for Inference API

---

**Made with 💛 for mental wellness**
