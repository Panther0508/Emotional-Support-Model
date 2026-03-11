# Emotional Support AI 🤖💛

A **Flask-based AI chatbot** that provides **empathetic emotional support** using natural language processing. This application detects user emotions, responds with personalized messages based on selected personality traits, provides coping suggestions, and tracks conversations over time.

---

## 🌟 Features

### Core Features
- **Granular Emotion Detection**: Detects emotions including *happy, sad, anxious, angry, neutral* using keyword matching and TextBlob sentiment analysis
- **Adaptive Response System**: Four distinct AI personalities (empathetic, funny, motivational, calm) for personalized interactions
- **Multi-User Support**: Each user has their own conversation history stored locally in JSON format
- **Coping Suggestions**: Provides context-aware tips for managing different emotional states
- **Conversation History**: Persistent chat history with automatic saving (last 100 messages)
- **Statistics Tracking**: Global and per-user statistics for conversations and emotions

### User Experience
- **Modern Dark Theme**: Beautiful, accessible dark mode UI with smooth animations
- **Real-time Chat Interface**: Instant responses with typing indicators
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Personalized Avatars**: Visual feedback for different emotions and personalities

### Technical Features
- **RESTful API**: Clean API endpoints for all operations
- **Session Management**: Secure user sessions with auto-generated secret keys
- **Error Handling**: Graceful error pages and validation
- **Local Storage**: All data stored locally for privacy (no cloud dependency)

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

4. **Run the application:**
```bash
python app.py
```

5. **Open in browser:**
Navigate to `http://localhost:5000`

---

## 📁 Project Structure

```
Emotional-Support-Model/
├── app.py                      # Main Flask application
├── chatbot.py                  # AI response generation logic
├── emotion_detector.py         # Emotion detection using NLP
├── requirements.txt            # Python dependencies
├── coping_suggestions.json     # Context-aware coping tips
├── training_data.json          # Intent patterns and responses
│
├── templates/                  # HTML templates
│   ├── base.html              # Base template with navigation
│   ├── index.html             # Landing page
│   ├── chat.html              # Chat interface
│   └── error.html             # Error pages
│
├── static/                    # Static assets
│   ├── css/
│   │   └── style.css          # Main stylesheet
│   └── js/
│       └── main.js            # Client-side JavaScript
│
├── data/                      # Application data
│   └── statistics.json        # Usage statistics
│
├── users/                     # User data storage
│   └── {username}.json        # Individual user chat histories
│
└── LICENSE                    # MIT License
```

---

## ⚙️ Configuration

### Environment Variables (Optional)

Create a `.env` file in the project root:

```env
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000
HOST=0.0.0.0
SECRET_KEY=your-secret-key-here
```

### AI Personalities

| Personality | Description | Best For |
|------------|-------------|----------|
| empathetic | Understanding and patient listener | Venting, seeking validation |
| funny | Light-hearted and humorous | Lifting mood, casual chat |
| motivational | Encouraging and inspiring | Seeking motivation, goals |
| calm | Peaceful and grounding | Anxiety, stress relief |

---

## 📡 API Endpoints

### Web Routes

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Landing page |
| `/chat` | GET | Chat interface |
| `/logout` | GET | Logout and clear session |

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
1. **Keyword Matching**: First checks for emotion-specific keywords
2. **Sentiment Analysis**: Falls back to TextBlob polarity scoring
3. **Classification**: Maps sentiment scores to emotion categories

### Response Generation
1. **Intent Matching**: Checks training data for matching patterns
2. **Personality Selection**: Applies selected personality tone
3. **Context Enhancement**: Adds coping tips for negative emotions

### Data Flow
```
User Input → Emotion Detection → Intent Matching → Personality Response → Add Coping Tips → Save to History → Return Response
```

---

## 🛠️ Technologies Used

### Backend
- **Flask** (3.1.2) - Web framework
- **TextBlob** (0.19.0) - Natural language processing
- **NLTK** (3.9.3) - Additional NLP capabilities
- **Python** - Core language

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with CSS variables
- **JavaScript (ES6+)** - Client-side interactivity
- **Font Awesome** - Icon library
- **Google Fonts** - Typography (Poppins)

---

## 🔒 Privacy & Security

- All conversation data is stored locally on your machine
- No data is sent to external servers (except NLTK data downloads)
- Usernames are sanitized to prevent path traversal
- Session keys are auto-generated for each session
- No analytics or tracking implemented

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

---

## 🙏 Acknowledgments

- TextBlob for sentiment analysis
- NLTK for natural language processing
- Font Awesome for icons
- Google Fonts for typography

---

**Made with 💛 for mental wellness**

