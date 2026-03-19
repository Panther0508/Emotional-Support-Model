# Emotional Support AI 🌿

<p align="center">
  <a href="https://emotional-support-model-1.onrender.com/">
    <img src="https://img.shields.io/badge/Live_Demo-00b894?style=for-the-badge&logo=render&logoColor=white" alt="Live Demo">
  </a>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  </a>
  <a href="https://flask.palletsprojects.com/">
    <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  </a>
  <a href="https://creativecommons.org/licenses/MIT/">
    <img src="https://img.shields.io/badge/License-MIT-00b894?style=for-the-badge" alt="License">
  </a>
</p>

> A Flask-based AI chatbot that provides empathetic emotional support using natural language processing. This application detects user emotions, responds with personalized messages based on selected personality traits, provides coping suggestions, and tracks conversations over time.

---

## 🚀 Live Demo

**Try it now**: [https://emotional-support-model-1.onrender.com/](https://emotional-support-model-1.onrender.com/)

![Landing Page](Screenshot%202026-03-19%20110427.png)

---

## 📋 Table of Contents

1. [Features](#-features)
2. [Screenshots](#-application-screenshots)
3. [Tech Stack](#-tech-stack)
4. [Installation](#-installation)
5. [Configuration](#-configuration)
6. [Usage](#-usage)
7. [API Endpoints](#-api-endpoints)
8. [Project Structure](#-project-structure)
9. [How It Works](#-how-it-works)
10. [Contributing](#-contributing)
11. [License](#-license)
12. [Disclaimer](#-disclaimer)

---

## ✨ Features

### Core Features

#### 🤖 Intelligent Emotion Detection

- **Multi-emotion recognition**: Detects happy, sad, anxious, angry, neutral, calm, and excited states
- **Hybrid approach**: Combines keyword matching with TextBlob sentiment analysis
- **Context awareness**: Handles negations and intensity modifiers for accurate detection
- **Confidence scoring**: Provides sentiment polarity scores for each message

#### 🎭 Adaptive AI Personalities

Choose from four distinct interaction styles:

| Personality      | Icon | Description                        | Best For                    |
| ---------------- | ---- | ---------------------------------- | --------------------------- |
| **Empathetic**   | 🤗   | Understanding and patient listener | Venting, seeking validation |
| **Funny**        | 😄   | Light-hearted and humorous         | Lifting mood, casual chat   |
| **Motivational** | 💪   | Encouraging and inspiring          | Seeking motivation, goals   |
| **Calm**         | 🧘   | Peaceful and grounding             | Anxiety, stress relief      |

#### 💬 Real-time Chat Experience

- Instant AI responses with typing indicators
- Glassmorphism UI with smooth animations
- Persistent conversation history (last 100 messages per user)
- Emotion badges showing detected feelings
- Message timestamps and metadata

#### 📊 Personal Analytics

- Track your emotional journey over time
- View message counts and active days
- Monitor emotion distribution with visual charts
- Export conversation history in JSON format

#### 🔒 Security & Privacy

- User authentication with secure password hashing
- Session-based disclaimer tracking
- Local data storage (no cloud dependency)
- Optional API integrations (opt-in)

### Advanced AI Features

- **Google AI Gemini Integration**: Optional integration with Google Gemini for advanced AI responses
- **Hugging Face Integration**: Optional integration with Hugging Face Inference API for NLP tasks
- **Sentiment Analysis**: TextBlob-powered sentiment analysis with confidence scores
- **Crisis Detection**: Automatic detection of crisis keywords with immediate resource referral

### User Experience Features

- **Modern Dark/Light Theme**: Beautiful, accessible UI with smooth theme transitions
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Mandatory Disclaimer**: 60-second wait timer before accessing the application
- **Accessibility**: Keyboard navigation, focus states, and screen reader friendly

---

## 🖥️ Application Screenshots

### Landing Page

![Landing Page](Screenshot%202026-03-19%20110427.png)

### Features Section

![Features](Screenshot%202026-03-19%20110530.png)

### Chat Interface

![Chat Interface](Screenshot%202026-03-19%20110649.png)

---

## 🛠️ Tech Stack

### Backend Technologies

| Technology       | Version | Purpose                     |
| ---------------- | ------- | --------------------------- |
| Python           | 3.8+    | Core programming language   |
| Flask            | 3.1.x   | Web framework               |
| Flask-Login      | Latest  | User authentication         |
| Flask-SQLAlchemy | Latest  | Database ORM                |
| TextBlob         | 0.19.0  | Sentiment analysis          |
| NLTK             | 3.9.x   | Natural language processing |
| Werkzeug         | Latest  | Password hashing            |
| python-dotenv    | Latest  | Environment variables       |
| requests         | Latest  | HTTP client for APIs        |

### Frontend Technologies

| Technology      | Purpose                    |
| --------------- | -------------------------- |
| HTML5           | Semantic markup            |
| CSS3 (Modern)   | Styling with CSS variables |
| JavaScript ES6+ | Client-side interactivity  |
| Font Awesome 6  | Icon library               |
| Google Fonts    | Poppins typography         |

### External APIs (Optional)

- **Google AI Gemini** - Advanced text generation
- **Hugging Face** - NLP tasks (sentiment, summarization)

---

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- (Optional) Git for version control

### Quick Start

#### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/Emotional-Support-Model.git
cd Emotional-Support-Model
```

#### 2. Create Virtual Environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**

```bash
python -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Run the Application

```bash
python app.py
```

#### 5. Open in Browser

Navigate to: `http://localhost:5000`

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the `env/` directory:

```env
# Required for basic functionality
SECRET_KEY=your-secret-key-here-change-in-production

# Optional - for advanced AI features
HF_TOKEN=your_huggingface_token
GOOGLE_TOKEN=your_google_ai_key
```

### API Configuration

#### Getting Hugging Face Token

1. Visit: https://huggingface.co/settings/tokens
2. Create a new token with "Read" permissions
3. Add to `.env`: `HF_TOKEN=your_token_here`

#### Getting Google AI (Gemini) Key

1. Visit: https://aistudio.google.com/app/apikey
2. Create a new API key
3. Add to `.env`: `GOOGLE_TOKEN=your_api_key_here`

---

## 📖 Usage

### First-Time Setup

1. **Accept Disclaimer**: Read and accept the mandatory disclaimer (60-second timer)
2. **Register**: Create an account with username and password
3. **Login**: Use your credentials to access the chat
4. **Choose Personality**: Select your preferred AI personality style

### Using the Chat

#### Sending Messages

- Type your message in the input field
- Press Enter or click the send button
- Receive empathetic AI responses
- View detected emotion badges

#### Changing Personality

1. Click "Change" in the sidebar
2. Select from 4 personality options
3. Apply changes instantly

#### Viewing Statistics

1. Check sidebar for quick stats
2. Use "View Stats" for detailed analytics
3. Export history for external analysis

### Example Conversations

| User Input                       | Detected Emotion | AI Response (Empathetic)                                                                               |
| -------------------------------- | ---------------- | ------------------------------------------------------------------------------------------------------ |
| "I'm feeling lonely today"       | sad              | "I'm here for you. It seems like you're going through a difficult time. 🤗 💡 Tip: Take a deep breath" |
| "I got a promotion at work!"     | happy            | "That's wonderful news! I'm so proud of you! 🎉"                                                       |
| "I'm so stressed about the exam" | anxious          | "Take a deep breath. I understand this feels overwhelming. 💛 💡 Tip: Try meditation"                  |
| "This is so frustrating!"        | angry            | "It's completely okay to feel angry. Let it out, I'm listening. 😌 💡 Tip: Count to 10"                |

---

## 📡 API Endpoints

### Web Routes

| Endpoint             | Methods   | Description                  | Auth Required |
| -------------------- | --------- | ---------------------------- | ------------- |
| `/`                  | GET       | Landing page with disclaimer | No            |
| `/chat`              | GET       | Main chat interface          | Yes           |
| `/login`             | GET, POST | User login                   | No            |
| `/register`          | GET, POST | User registration            | No            |
| `/logout`            | GET       | Logout and clear session     | Yes           |
| `/dashboard`         | GET       | User dashboard               | Yes           |
| `/history`           | GET       | Conversation history         | Yes           |
| `/confessions`       | GET       | Anonymous confessions        | No            |
| `/accept-disclaimer` | POST      | Accept disclaimer            | No            |
| `/check-disclaimer`  | GET       | Check disclaimer status      | No            |

### REST API Endpoints

#### Public Endpoints

| Endpoint                     | Method | Description             |
| ---------------------------- | ------ | ----------------------- |
| `/api/stats`                 | GET    | Get global statistics   |
| `/api/quick_stats`           | GET    | Get quick stats summary |
| `/api/confessions`           | GET    | List all confessions    |
| `/api/confessions`           | POST   | Create new confession   |
| `/api/confessions/<id>/like` | POST   | Like a confession       |

#### Protected Endpoints (Authentication Required)

| Endpoint                  | Method | Description                   |
| ------------------------- | ------ | ----------------------------- |
| `/api/chat`               | POST   | Send message, get AI response |
| `/api/history`            | GET    | Get user's chat history       |
| `/api/history/clear`      | POST   | Clear user's chat history     |
| `/api/user_stats`         | GET    | Get user's statistics         |
| `/api/export`             | GET    | Export chat history as JSON   |
| `/api/change_personality` | POST   | Change AI personality         |

### API Request/Response Examples

#### Send Chat Message

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
  "emotion_emoji": "😢",
  "timestamp": "2026-03-19T10:00:00.000000"
}
```

#### Get User Statistics

```bash
curl -X GET http://localhost:5000/api/user_stats \
  -H "Authorization: Bearer <token>"
```

**Response:**

```json
{
  "success": true,
  "stats": {
    "total_messages": 42,
    "emotions": {
      "happy": 15,
      "sad": 12,
      "anxious": 8,
      "neutral": 7
    }
  }
}
```

---

## 📁 Project Structure

```
Emotional-Support-Model/
├── app.py                      # Main Flask application entry point
├── auth.py                     # Authentication blueprint (login/register/logout)
├── chatbot.py                  # AI response generation logic
├── emotion_detector.py         # Emotion detection using NLP
├── config.py                   # Application configuration settings
├── models.py                   # SQLAlchemy database models
├── coping_suggestions.json     # Context-aware coping tips data
├── training_data.json          # Intent patterns and responses
├── requirements.txt            # Python dependencies
├── wsgi.py                     # WSGI entry point for deployment
│
├── apis/                       # External API integrations
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
├── templates/                  # HTML/Jinja2 templates
│   ├── base.html              # Base template with navigation
│   ├── index.html             # Landing page
│   ├── chat.html              # Chat interface
│   ├── login.html             # Login page
│   ├── register.html          # Registration page
│   ├── dashboard.html         # User dashboard
│   ├── history.html           # Conversation history
│   ├── confessions.html       # Anonymous confessions
│   ├── disclaimer.html        # Mandatory disclaimer page
│   └── error.html             # Error pages
│
├── static/                    # Static assets
│   ├── css/
│   │   ├── imports.css       # Main modular CSS (imports all)
│   │   ├── base/            # Base styles (variables, reset)
│   │   ├── components/       # Reusable UI components
│   │   ├── layouts/          # Layout styles
│   │   ├── pages/            # Page-specific styles
│   │   └── utilities/        # Utility classes
│   └── js/
│       ├── main.js           # Core functionality
│       └── chat.js           # Chat interface logic
│
├── data/                      # Application data
│   ├── app.db               # SQLite database
│   └── statistics.json      # Global usage statistics
│
├── users/                     # User data storage
│   └── {username}.json      # Individual user chat histories
│
└── LICENSE                   # MIT License
```

---

## 🧠 How It Works

### Emotion Detection Pipeline

1. **Keyword Matching**: First checks for emotion-specific keywords with intensity modifiers
2. **Negation Handling**: Detects negations like "not happy" or "doesn't make me sad"
3. **Sentiment Analysis**: Falls back to TextBlob polarity scoring (-1 to +1)
4. **Classification**: Maps sentiment scores to emotion categories
5. **Confidence Scoring**: Returns confidence based on keyword matches and sentiment

### Response Generation Flow

```
User Input
    ↓
Crisis Detection (Check for urgent keywords)
    ↓
Intent Matching (Check training data patterns)
    ↓
Emotion Detection (Analyze emotional content)
    ↓
Personality Selection (Apply selected tone)
    ↓
Context Enhancement (Add coping tips if negative)
    ↓
History Saving (Store in user JSON file)
    ↓
Return Response
```

### Disclaimer System

1. **Initial Visit**: Users see mandatory disclaimer page
2. **Timer**: 60-second countdown prevents immediate access
3. **Acceptance**: Button enabled after timer completes
4. **Session**: Disclaimer status stored in session
5. **Enforcement**: Both landing page and chat enforce disclaimer

### Data Storage

- **User Accounts**: SQLite database (`data/app.db`)
- **Chat History**: JSON files per user (`users/{username}.json`)
- **Statistics**: JSON file (`data/statistics.json`)
- **Confessions**: SQLite table in app.db

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

### Step 1: Fork the Repository

Click the "Fork" button on GitHub.

### Step 2: Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/Emotional-Support-Model.git
cd Emotional-Support-Model
```

### Step 3: Create a Feature Branch

```bash
git checkout -b feature/amazing-feature
```

### Step 4: Make Changes

Implement your feature or bug fix.

### Step 5: Commit Changes

```bash
git add .
git commit -m 'Add amazing feature'
```

### Step 6: Push to GitHub

```bash
git push origin feature/amazing-feature
```

### Step 7: Open a Pull Request

Go to the original repository and click "New Pull Request"

### Coding Standards

- Follow PEP 8 style guide for Python
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Test your changes before submitting

---

## 📝 License

This project is licensed under the MIT License.

Copyright (c) 2026 Emotional Support AI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

See the [LICENSE](LICENSE) file for details.

---

## ⚠️ Disclaimer

### Important Notice

> **This AI companion is designed to provide emotional support and is NOT a substitute for professional mental health care.**

If you're experiencing a mental health crisis or need immediate help, please contact:

- **National Suicide Prevention Lifeline**: 988 (US)
- **Crisis Text Line**: Text HOME to 741741
- **International Association for Suicide Prevention**: https://findahelpline.com/

### Mandatory Disclaimer Page

Upon first visiting the application, users must:

1. Read the mental health disclaimer
2. Read the API usage notice
3. Wait 60 seconds before proceeding
4. Accept the terms to access the application

This is a legal requirement to ensure users understand the limitations of the AI system.

### API Usage Disclaimer

This application integrates with external AI services provided by **Google AI (Gemini)** and **Hugging Face**. By using these features:

1. **Data Transmission**: Your messages may be transmitted to these third-party AI providers for processing.
   - [Google AI Privacy Policy](https://policies.google.com/privacy)
   - [Hugging Face Privacy Policy](https://huggingface.co/privacy)

2. **API Costs**: Some features may incur costs based on usage.

3. **Service Availability**: External API services may experience downtime or rate limiting.

4. **Content Moderation**: AI-generated responses are generated by third-party models and may not always be appropriate.

### Liability

The developers of this project are not liable for:

- Any damages arising from the use of AI-generated responses
- Decisions made based on AI suggestions
- Third-party API service disruptions
- Any breach of data when transmitting to external services

---

## 🙏 Acknowledgments

- [TextBlob](https://textblob.readthedocs.io/) for sentiment analysis
- [NLTK](https://www.nltk.org/) for natural language processing
- [Font Awesome](https://fontawesome.com/) for icons
- [Google Fonts](https://fonts.google.com/) for Poppins typography
- [Google AI](https://ai.google/) for Gemini API
- [Hugging Face](https://huggingface.co/) for Inference API
- [Flask](https://flask.palletsprojects.com/) community for the amazing framework

---

## 📊 Stats

![GitHub stars](https://img.shields.io/github/stars/yourusername/Emotional-Support-Model?style=flat)
![GitHub forks](https://img.shields.io/github/forks/yourusername/Emotional-Support-Model?style=flat)
![GitHub issues](https://img.shields.io/github/issues/yourusername/Emotional-Support-Model?style=flat)

---

**Made with 🌿 for mental wellness**
