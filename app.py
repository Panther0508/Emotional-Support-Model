# app.py - Flask Backend for Emotional Support AI
import os
import json
import random
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from emotion_detector import detect_emotion, get_emotion_emoji, get_emotion_color
from chatbot import get_response, get_personalities, get_personality_info
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
Config.init_app(app)

# Register custom Jinja2 filters
@app.template_filter('emotion_color')
def emotion_color_filter(emotion):
    """Get color for emotion"""
    return get_emotion_color(emotion)

@app.template_filter('personality_icon')
def personality_icon_filter(personality):
    """Get icon for personality"""
    icons = {
        'empathetic': 'heart',
        'funny': 'laugh-squint',
        'motivational': 'fire',
        'calm': 'spa'
    }
    return icons.get(personality, 'heart')

@app.template_filter('emotion_emoji')
def emotion_emoji_filter(emotion):
    """Get emoji for emotion"""
    return get_emotion_emoji(emotion)

# Ensure data directories exist
os.makedirs(Config.USERS_DIR, exist_ok=True)
os.makedirs(Config.DATA_DIR, exist_ok=True)


def load_statistics():
    """Load usage statistics from file"""
    if os.path.exists(Config.STATISTICS_FILE):
        try:
            with open(Config.STATISTICS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {"total_conversations": 0, "emotions": {}, "users": {}, "daily_stats": {}}
    return {"total_conversations": 0, "emotions": {}, "users": {}, "daily_stats": {}}


def save_statistics(stats):
    """Save usage statistics to file"""
    try:
        with open(Config.STATISTICS_FILE, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=4)
    except IOError:
        pass  # Silently fail if we can't save stats


def update_statistics(username, emotion):
    """Update statistics with new conversation"""
    stats = load_statistics()
    stats["total_conversations"] += 1
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Update daily stats
    if "daily_stats" not in stats:
        stats["daily_stats"] = {}
    if today not in stats["daily_stats"]:
        stats["daily_stats"][today] = {"total": 0, "emotions": {}}
    stats["daily_stats"][today]["total"] += 1
    if emotion not in stats["daily_stats"][today]["emotions"]:
        stats["daily_stats"][today]["emotions"][emotion] = 0
    stats["daily_stats"][today]["emotions"][emotion] += 1
    
    # Update emotion counts
    if emotion not in stats["emotions"]:
        stats["emotions"][emotion] = 0
    stats["emotions"][emotion] += 1
    
    # Update user counts
    if username not in stats["users"]:
        stats["users"][username] = {"total": 0, "emotions": {}, "first_seen": today, "last_seen": today}
    stats["users"][username]["total"] += 1
    stats["users"][username]["last_seen"] = today
    if emotion not in stats["users"][username]["emotions"]:
        stats["users"][username]["emotions"][emotion] = 0
    stats["users"][username]["emotions"][emotion] += 1
    
    save_statistics(stats)


def sanitize_username(username):
    """Sanitize username for security"""
    return ''.join(c for c in username if c.isalnum() or c in ['_', '-'])


def validate_personality(personality):
    """Validate personality selection"""
    return personality if personality in Config.PERSONALITIES else Config.DEFAULT_PERSONALITY


@app.route('/')
def index():
    """Main landing page"""
    stats = load_statistics()
    return render_template('index.html', stats=stats)


@app.route('/about')
def about():
    """About page"""
    return render_template('index.html', stats=load_statistics(), section='about')


@app.route('/features')
def features():
    """Features page"""
    return render_template('index.html', stats=load_statistics(), section='features')


@app.route('/chat')
def chat():
    """Chat interface page"""
    username = session.get('username')
    personality = session.get('personality', Config.DEFAULT_PERSONALITY)
    
    # Load user chat history
    chat_history = []
    if username:
        user_file = os.path.join(Config.USERS_DIR, f"{username}.json")
        if os.path.exists(user_file):
            try:
                with open(user_file, 'r', encoding='utf-8') as f:
                    chat_history = json.load(f)
            except (json.JSONDecodeError, IOError):
                chat_history = []
    
    stats = load_statistics()
    personalities = get_personalities()
    personality_info = get_personality_info()
    
    return render_template('chat.html', 
                         username=username, 
                         personality=personality,
                         chat_history=chat_history,
                         stats=stats,
                         personalities=personalities,
                         personality_info=personality_info)


@app.route('/api/set_user', methods=['POST'])
def set_user():
    """Set user session"""
    data = request.get_json()
    username = data.get('username', '').strip()
    personality = validate_personality(data.get('personality', Config.DEFAULT_PERSONALITY))
    
    if not username:
        return jsonify({'success': False, 'message': 'Please enter a username'})
    
    if len(username) < 2:
        return jsonify({'success': False, 'message': 'Username must be at least 2 characters'})
    
    if len(username) > 30:
        return jsonify({'success': False, 'message': 'Username must be less than 30 characters'})
    
    # Sanitize username
    username = sanitize_username(username)
    
    session['username'] = username
    session['personality'] = personality
    
    return jsonify({
        'success': True, 
        'username': username, 
        'personality': personality,
        'message': f'Welcome, {username}! You are now chatting with the {personality} AI.'
    })


@app.route('/api/change_personality', methods=['POST'])
def change_personality():
    """Change AI personality"""
    if not session.get('username'):
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    data = request.get_json()
    personality = validate_personality(data.get('personality', Config.DEFAULT_PERSONALITY))
    
    session['personality'] = personality
    
    return jsonify({
        'success': True,
        'personality': personality,
        'message': f'AI personality changed to {personality}'
    })


@app.route('/api/chat', methods=['POST'])
def chat_api():
    """Handle chat messages"""
    data = request.get_json()
    user_input = data.get('message', '').strip()
    username = session.get('username')
    personality = session.get('personality', Config.DEFAULT_PERSONALITY)
    
    if not user_input:
        return jsonify({'success': False, 'message': 'Please enter a message'})
    
    if not username:
        return jsonify({'success': False, 'message': 'Please set a username first'})
    
    if len(user_input) > 2000:
        return jsonify({'success': False, 'message': 'Message too long (max 2000 characters)'})
    
    # Get AI response
    reply, emotion = get_response(user_input, personality)
    
    # Create message object
    message_data = {
        "user": user_input,
        "ai": reply,
        "emotion": emotion,
        "timestamp": datetime.now().isoformat()
    }
    
    # Save to user history
    user_file = os.path.join(Config.USERS_DIR, f"{username}.json")
    chat_history = []
    if os.path.exists(user_file):
        try:
            with open(user_file, 'r', encoding='utf-8') as f:
                chat_history = json.load(f)
        except (json.JSONDecodeError, IOError):
            chat_history = []
    
    chat_history.append(message_data)
    
    # Keep only last MAX_HISTORY_MESSAGES
    chat_history = chat_history[-Config.MAX_HISTORY_MESSAGES:]
    
    try:
        with open(user_file, 'w', encoding='utf-8') as f:
            json.dump(chat_history, f, indent=4)
    except IOError:
        pass  # Continue even if save fails
    
    # Update statistics
    update_statistics(username, emotion)
    
    return jsonify({
        'success': True,
        'message': reply,
        'emotion': emotion,
        'timestamp': message_data['timestamp'],
        'emotion_emoji': get_emotion_emoji(emotion)
    })


@app.route('/api/history', methods=['GET'])
def get_history():
    """Get user chat history"""
    username = session.get('username')
    
    if not username:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    user_file = os.path.join(Config.USERS_DIR, f"{username}.json")
    if os.path.exists(user_file):
        try:
            with open(user_file, 'r', encoding='utf-8') as f:
                chat_history = json.load(f)
            return jsonify({'success': True, 'history': chat_history})
        except (json.JSONDecodeError, IOError):
            return jsonify({'success': True, 'history': []})
    
    return jsonify({'success': True, 'history': []})


@app.route('/api/history/clear', methods=['POST'])
def clear_history():
    """Clear user chat history"""
    username = session.get('username')
    
    if not username:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    user_file = os.path.join(Config.USERS_DIR, f"{username}.json")
    if os.path.exists(user_file):
        try:
            os.remove(user_file)
        except OSError:
            return jsonify({'success': False, 'message': 'Could not clear history'})
    
    return jsonify({'success': True, 'message': 'Chat history cleared'})


@app.route('/api/export', methods=['GET'])
def export_history():
    """Export user chat history as JSON"""
    username = session.get('username')
    
    if not username:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    user_file = os.path.join(Config.USERS_DIR, f"{username}.json")
    if os.path.exists(user_file):
        try:
            with open(user_file, 'r', encoding='utf-8') as f:
                chat_history = json.load(f)
            
            export_data = {
                "username": username,
                "export_date": datetime.now().isoformat(),
                "message_count": len(chat_history),
                "messages": chat_history
            }
            
            return jsonify({
                'success': True,
                'data': export_data,
                'filename': f"chat_history_{username}_{datetime.now().strftime('%Y%m%d')}.json"
            })
        except (json.JSONDecodeError, IOError):
            return jsonify({'success': False, 'message': 'Could not export history'})
    
    return jsonify({'success': True, 'messages': []})


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get global statistics"""
    stats = load_statistics()
    return jsonify({'success': True, 'stats': stats})


@app.route('/api/user_stats', methods=['GET'])
def get_user_stats():
    """Get statistics for current user"""
    username = session.get('username')
    
    if not username:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    stats = load_statistics()
    user_stats = stats.get('users', {}).get(username, {})
    
    return jsonify({'success': True, 'stats': user_stats})


@app.route('/api/quick_stats', methods=['GET'])
def get_quick_stats():
    """Get quick statistics summary"""
    stats = load_statistics()
    
    # Calculate percentages for emotions
    emotion_counts = stats.get('emotions', {})
    total = sum(emotion_counts.values())
    
    emotion_percentages = {}
    for emotion, count in emotion_counts.items():
        emotion_percentages[emotion] = round((count / total * 100) if total > 0 else 0, 1)
    
    return jsonify({
        'success': True,
        'total_conversations': stats.get('total_conversations', 0),
        'total_users': len(stats.get('users', {})),
        'emotions': emotion_counts,
        'emotion_percentages': emotion_percentages
    })


@app.route('/logout')
def logout():
    """Log out user"""
    username = session.get('username')
    session.clear()
    return redirect(url_for('index'))


# Error handlers
@app.errorhandler(404)
def not_found(e):
    return render_template('error.html', error_code=404, message="Page not found"), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('error.html', error_code=500, message="Server error"), 500


@app.errorhandler(400)
def bad_request(e):
    return jsonify({'success': False, 'message': 'Bad request'}), 400


@app.errorhandler(403)
def forbidden(e):
    return render_template('error.html', error_code=403, message="Access forbidden"), 403


# Initialize NLTK on startup
def initialize_nltk():
    """Initialize NLTK data on first run"""
    try:
        import nltk
        # Download required NLTK data
        nltk.download('punkt', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
        nltk.download('punkt_tab', quiet=True)
        nltk.download('brown', quiet=True)
        nltk.download('wordnet', quiet=True)
        nltk.download('omw-1.4', quiet=True)
    except Exception as e:
        print(f"NLTK initialization warning: {e}")
        pass  # Continue even if NLTK fails


if __name__ == '__main__':
    initialize_nltk()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
