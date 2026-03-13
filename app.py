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

from flask_login import LoginManager, current_user
from models import db, User
from auth import auth_bp

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register blueprints
app.register_blueprint(auth_bp)

with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(f"Error creating database: {e}")

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


@app.route('/accept-disclaimer', methods=['POST'])
def accept_disclaimer():
    """Accept the disclaimer and start the 10-second timer"""
    import time
    session['disclaimer_accepted'] = True
    session['disclaimer_timestamp'] = time.time()
    return jsonify({'success': True, 'message': 'Disclaimer accepted'})


@app.route('/check-disclaimer', methods=['GET'])
def check_disclaimer():
    """Check if disclaimer timer is complete"""
    import time
    disclaimer_timestamp = session.get('disclaimer_timestamp', 0)
    current_time = time.time()
    time_elapsed = current_time - disclaimer_timestamp if disclaimer_timestamp > 0 else 0
    remaining_time = max(0, 10 - int(time_elapsed))
    
    return jsonify({
        'accepted': session.get('disclaimer_accepted', False),
        'remaining_time': remaining_time,
        'complete': remaining_time == 0
    })


@app.route('/about')
def about():
    """About page"""
    return render_template('index.html', stats=load_statistics(), section='about')


@app.route('/features')
def features():
    """Features page"""
    return render_template('index.html', stats=load_statistics(), section='features')


from flask_login import login_required, current_user

@app.route('/chat')
@login_required
def chat():
    """Chat interface page"""
    username = current_user.username
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


@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard view"""
    username = current_user.username
    stats = load_statistics()
    
    # Get user specific stats
    user_stats = stats.get('users', {}).get(username, {
        "conversations": 0,
        "emotions": {}
    })
    
    # Calculate dominant emotion
    emotions = user_stats.get("emotions", {})
    dominant_emotion = "neutral"
    if emotions:
        dominant_emotion = max(emotions, key=emotions.get)
        
    # Get recent history
    recent_history = []
    user_file = os.path.join(Config.USERS_DIR, f"{username}.json")
    if os.path.exists(user_file):
        try:
            with open(user_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
                recent_history = history[-10:] if history else [] # Last 10 messages
                recent_history.reverse() # Newest first
        except (json.JSONDecodeError, IOError):
            pass
            
    return render_template('dashboard.html',
                         username=username,
                         total_conversations=user_stats.get("conversations", 0),
                         emotions=emotions,
                         dominant_emotion=dominant_emotion,
                         recent_history=recent_history,
                         stats=stats)


@app.route('/history')
@login_required
def history():
    """Full chat history view"""
    username = current_user.username
    stats = load_statistics()
    
    chat_history = []
    user_file = os.path.join(Config.USERS_DIR, f"{username}.json")
    if os.path.exists(user_file):
        try:
            with open(user_file, 'r', encoding='utf-8') as f:
                chat_history = json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
            
    return render_template('history.html',
                         username=username,
                         chat_history=chat_history,
                         stats=stats)


# The `/api/set_user` route has been removed in favor of the new auth blueprint `/login` and `/register`.


@app.route('/api/change_personality', methods=['POST'])
@login_required
def change_personality():
    """Change AI personality"""
    
    data = request.get_json()
    personality = validate_personality(data.get('personality', Config.DEFAULT_PERSONALITY))
    
    session['personality'] = personality
    
    return jsonify({
        'success': True,
        'personality': personality,
        'message': f'AI personality changed to {personality}'
    })


@app.route('/api/chat', methods=['POST'])
@login_required
def chat_api():
    """Handle chat messages"""
    data = request.get_json()
    user_input = data.get('message', '').strip()
    username = current_user.username
    personality = session.get('personality', Config.DEFAULT_PERSONALITY)
    
    if not user_input:
        return jsonify({'success': False, 'message': 'Please enter a message'})
    
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
@login_required
def get_history():
    """Get user chat history"""
    username = current_user.username
    
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
@login_required
def clear_history():
    """Clear user chat history"""
    username = current_user.username
    
    user_file = os.path.join(Config.USERS_DIR, f"{username}.json")
    if os.path.exists(user_file):
        try:
            os.remove(user_file)
        except OSError:
            return jsonify({'success': False, 'message': 'Could not clear history'})
    
    return jsonify({'success': True, 'message': 'Chat history cleared'})


@app.route('/api/export', methods=['GET'])
@login_required
def export_history():
    """Export user chat history as JSON"""
    username = current_user.username
    
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
@login_required
def get_user_stats():
    """Get statistics for current user"""
    username = current_user.username
    
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


# The /logout route is now handled by the auth blueprint.


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


# Initialize NLTK on startup - deferred to avoid blocking deployment
def initialize_nltk():
    """Initialize NLTK data on first run - called lazily"""
    import nltk
    import os
    
    # Set NLTK data path
    nltk_data_path = os.path.join(os.path.expanduser('~'), 'nltk_data')
    nltk.data.path.append(nltk_data_path)
    
    # Download required NLTK data
    try:
        for resource in ['punkt', 'averaged_perceptron_tagger', 'punkt_tab', 'brown', 'wordnet', 'omw-1.4']:
            try:
                nltk.download(resource, quiet=True, download_dir=nltk_data_path)
            except:
                pass
    except Exception as e:
        print(f"NLTK initialization warning: {e}")


# ==================== Confessions Dashboard Routes ====================

@app.route('/confessions')
def confessions():
    """Confessions dashboard - anonymous posts"""
    from models import Confession
    
    # Get all confessions ordered by newest first
    all_confessions = Confession.query.order_by(Confession.created_at.desc()).all()
    
    return render_template('confessions.html', confessions=all_confessions)


@app.route('/api/confessions', methods=['POST'])
def create_confession():
    """Create a new anonymous confession"""
    from models import Confession
    
    data = request.get_json()
    content = data.get('content', '').strip()
    post_type = data.get('post_type', 'confession')
    
    if not content:
        return jsonify({'success': False, 'message': 'Content is required'}), 400
    
    if len(content) > 1000:
        return jsonify({'success': False, 'message': 'Content must be less than 1000 characters'}), 400
    
    # Create new confession
    confession = Confession(content=content, post_type=post_type)
    db.session.add(confession)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Confession posted successfully',
        'confession': {
            'id': confession.id,
            'content': confession.content,
            'post_type': confession.post_type,
            'created_at': confession.created_at.isoformat(),
            'likes': confession.likes
        }
    })


@app.route('/api/confessions/<int:confession_id>/like', methods=['POST'])
def like_confession(confession_id):
    """Like a confession"""
    from models import Confession
    
    confession = Confession.query.get(confession_id)
    if not confession:
        return jsonify({'success': False, 'message': 'Confession not found'}), 404
    
    confession.likes += 1
    db.session.commit()
    
    return jsonify({'success': True, 'likes': confession.likes})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
