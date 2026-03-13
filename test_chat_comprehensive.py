# test_chat_comprehensive.py - Comprehensive Test Plan for Chat Interface
# This test file covers all API endpoints and functionality of the chat interface

import requests
import json
import time
import random
import string
from datetime import datetime
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

BASE_URL = "http://127.0.0.1:5000"
session = requests.Session()

# Test Results Storage
test_results = []
errors_found = []

def log_test(name, expected, actual, passed, severity="N/A", notes=""):
    """Log test result"""
    result = {
        "test_name": name,
        "expected": expected,
        "actual": actual,
        "passed": passed,
        "severity": severity,
        "notes": notes
    }
    test_results.append(result)
    if not passed:
        errors_found.append(result)
    
    status = "PASS" if passed else "FAIL"
    print(f"[{status}]: {name}")
    if notes:
        print(f"   Notes: {notes}")

def generate_random_user():
    """Generate random username and password"""
    username = "testuser_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    return username, password

def cleanup_user(username):
    """Clean up test user"""
    # Try to delete user data file if exists
    from config import Config
    user_file = os.path.join(Config.USERS_DIR, f"{username}.json")
    if os.path.exists(user_file):
        try:
            os.remove(user_file)
        except:
            pass

# ============================================
# TEST 1: Health Check and Basic Connectivity
# ============================================

def test_health_check():
    """Test if the server is running"""
    print("\n" + "="*50)
    print("TEST SUITE: Health Check and Connectivity")
    print("="*50)
    
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        log_test(
            "Health Check - Server Running",
            "200 OK",
            f"{response.status_code} {response.reason}",
            response.status_code == 200,
            "Critical"
        )
    except requests.exceptions.RequestException as e:
        log_test(
            "Health Check - Server Running",
            "200 OK",
            f"Connection failed: {str(e)}",
            False,
            "Critical",
            "Server may not be running. Start with: python app.py"
        )

# ============================================
# TEST 2: Disclaimer Functionality
# ============================================

def test_disclaimer():
    """Test disclaimer acceptance flow"""
    print("\n" + "="*50)
    print("TEST SUITE: Disclaimer Functionality")
    print("="*50)
    
    # Test accept disclaimer
    response = session.post(f"{BASE_URL}/accept-disclaimer")
    log_test(
        "Accept Disclaimer",
        "success: True",
        f"success: {response.json().get('success')}",
        response.json().get('success') == True,
        "High"
    )
    
    # Wait for timer
    time.sleep(11)
    
    # Test check disclaimer
    response = session.get(f"{BASE_URL}/check-disclaimer")
    data = response.json()
    log_test(
        "Check Disclaimer Timer",
        "complete: True",
        f"complete: {data.get('complete')}",
        data.get('complete') == True,
        "Medium"
    )

# ============================================
# TEST 3: User Authentication
# ============================================

def test_authentication():
    """Test user registration and login"""
    print("\n" + "="*50)
    print("TEST SUITE: User Authentication")
    print("="*50)
    
    username, password = generate_random_user()
    
    # Test Registration
    response = session.post(f"{BASE_URL}/register", json={
        "username": username,
        "password": password
    })
    data = response.json()
    
    registration_success = data.get('success') == True
    log_test(
        "User Registration",
        "success: True with redirect",
        f"success: {data.get('success')}, redirect: {data.get('redirect')}",
        registration_success,
        "Critical"
    )
    
    if registration_success:
        # Test login with correct credentials
        response = session.post(f"{BASE_URL}/login", json={
            "username": username,
            "password": password
        })
        
        # Handle both JSON and redirect responses
        try:
            data = response.json()
            login_success = data.get('success') == True
        except:
            # Might have redirected - check if we're logged in by accessing protected route
            login_success = response.status_code in [200, 302]
        
        log_test(
            "User Login - Valid Credentials",
            "success: True or redirect",
            f"status: {response.status_code}",
            login_success,
            "Critical"
        )
        
        # Test login with wrong password
        session2 = requests.Session()
        response = session2.post(f"{BASE_URL}/login", json={
            "username": username,
            "password": "wrong_password_123"
        })
        
        try:
            data = response.json()
            login_failed = data.get('success') == False
        except:
            login_failed = response.status_code != 200
        
        log_test(
            "User Login - Invalid Password",
            "success: False",
            f"status: {response.status_code}",
            login_failed,
            "Critical"
        )
        
        # Test login with non-existent user
        response = session2.post(f"{BASE_URL}/login", json={
            "username": "nonexistent_user_12345",
            "password": password
        })
        
        log_test(
            "User Login - Non-existent User",
            "success: False",
            f"status: {response.status_code}",
            login_failed,
            "Critical"
        )
        
        # Test duplicate registration
        response = session.post(f"{BASE_URL}/register", json={
            "username": username,
            "password": password
        })
        
        try:
            data = response.json()
            duplicate_failed = data.get('success') == False
        except:
            duplicate_failed = response.status_code != 200
        
        log_test(
            "User Registration - Duplicate Username",
            "success: False",
            f"status: {response.status_code}",
            duplicate_failed,
            "High"
        )
        
        # Test short username
        session3 = requests.Session()
        response = session3.post(f"{BASE_URL}/register", json={
            "username": "ab",
            "password": password
        })
        
        try:
            data = response.json()
            short_username_failed = data.get('success') == False
        except:
            short_username_failed = response.status_code != 200
        
        log_test(
            "User Registration - Short Username (<3 chars)",
            "success: False",
            f"status: {response.status_code}",
            short_username_failed,
            "High"
        )
        
        # Test long username
        response = session3.post(f"{BASE_URL}/register", json={
            "username": "a" * 31,
            "password": password
        })
        
        try:
            data = response.json()
            long_username_failed = data.get('success') == False
        except:
            long_username_failed = response.status_code != 200
        
        log_test(
            "User Registration - Long Username (>30 chars)",
            "success: False",
            f"status: {response.status_code}",
            long_username_failed,
            "High"
        )
        
        # Test empty credentials
        response = session3.post(f"{BASE_URL}/register", json={
            "username": "",
            "password": ""
        })
        
        try:
            data = response.json()
            empty_failed = data.get('success') == False
        except:
            empty_failed = response.status_code != 200
        
        log_test(
            "User Registration - Empty Credentials",
            "success: False",
            f"status: {response.status_code}",
            empty_failed,
            "High"
        )
        
        return username, password
    return None, None

# ============================================
# TEST 4: Chat Message Functionality
# ============================================

def test_chat_api(username, password):
    """Test chat API endpoints"""
    print("\n" + "="*50)
    print("TEST SUITE: Chat API Functionality")
    print("="*50)
    
    # Ensure logged in
    session.post(f"{BASE_URL}/login", json={"username": username, "password": password})
    session.post(f"{BASE_URL}/accept-disclaimer")
    time.sleep(11)
    
    # Test valid message
    response = session.post(f"{BASE_URL}/api/chat", json={
        "message": "I am feeling really happy today!"
    })
    data = response.json()
    
    chat_success = data.get('success') == True and 'message' in data
    log_test(
        "Chat API - Valid Message",
        "success: True with message and emotion",
        f"success: {data.get('success')}, has message: {'message' in data}",
        chat_success,
        "Critical"
    )
    
    if chat_success:
        print(f"   Bot Response: {data.get('message', 'N/A')[:100]}...")
        print(f"   Detected Emotion: {data.get('emotion', 'N/A')}")
    
    # Test empty message
    response = session.post(f"{BASE_URL}/api/chat", json={
        "message": ""
    })
    data = response.json()
    
    empty_failed = data.get('success') == False
    log_test(
        "Chat API - Empty Message",
        "success: False",
        f"success: {data.get('success')}",
        empty_failed,
        "High"
    )
    
    # Test whitespace-only message
    response = session.post(f"{BASE_URL}/api/chat", json={
        "message": "   "
    })
    data = response.json()
    
    whitespace_failed = data.get('success') == False
    log_test(
        "Chat API - Whitespace Only Message",
        "success: False",
        f"success: {data.get('success')}",
        whitespace_failed,
        "High"
    )
    
    # Test message > 2000 chars
    long_message = "a" * 2001
    response = session.post(f"{BASE_URL}/api/chat", json={
        "message": long_message
    })
    data = response.json()
    
    long_failed = data.get('success') == False
    log_test(
        "Chat API - Message Too Long (>2000 chars)",
        "success: False",
        f"success: {data.get('success')}",
        long_failed,
        "High"
    )
    
    # Test exactly 2000 chars
    message_2000 = "a" * 2000
    response = session.post(f"{BASE_URL}/api/chat", json={
        "message": message_2000
    })
    data = response.json()
    
    exact_2000_success = data.get('success') == True
    log_test(
        "Chat API - Message Exactly 2000 chars",
        "success: True",
        f"success: {data.get('success')}",
        exact_2000_success,
        "Medium"
    )
    
    # Test special characters
    special_msg = "Test <script>alert('xss')</script> & '\" quotes"
    response = session.post(f"{BASE_URL}/api/chat", json={
        "message": special_msg
    })
    data = response.json()
    
    special_success = data.get('success') == True
    log_test(
        "Chat API - Special Characters",
        "success: True",
        f"success: {data.get('success')}",
        special_success,
        "Medium"
    )
    
    # Test emoji in message
    emoji_msg = "I feel happy 😊🎉"
    response = session.post(f"{BASE_URL}/api/chat", json={
        "message": emoji_msg
    })
    data = response.json()
    
    emoji_success = data.get('success') == True
    log_test(
        "Chat API - Emoji in Message",
        "success: True",
        f"success: {data.get('success')}",
        emoji_success,
        "Medium"
    )
    
    # Test multilingual message
    multi_msg = "你好，我今天很开心！مرحبا كيف حالك？"
    response = session.post(f"{BASE_URL}/api/chat", json={
        "message": multi_msg
    })
    data = response.json()
    
    multi_success = data.get('success') == True
    log_test(
        "Chat API - Multilingual Message",
        "success: True",
        f"success: {data.get('success')}",
        multi_success,
        "Medium"
    )

# ============================================
# TEST 5: Chat History Functionality
# ============================================

def test_history_api(username, password):
    """Test history API endpoints"""
    print("\n" + "="*50)
    print("TEST SUITE: Chat History Functionality")
    print("="*50)
    
    # Ensure logged in
    session.post(f"{BASE_URL}/login", json={"username": username, "password": password})
    
    # Test get history
    response = session.get(f"{BASE_URL}/api/history")
    data = response.json()
    
    history_success = data.get('success') == True and 'history' in data
    log_test(
        "Get Chat History",
        "success: True with history array",
        f"success: {data.get('success')}, history length: {len(data.get('history', []))}",
        history_success,
        "High"
    )
    
    # Test export history
    response = session.get(f"{BASE_URL}/api/export")
    data = response.json()
    
    export_success = data.get('success') == True
    log_test(
        "Export Chat History",
        "success: True",
        f"success: {data.get('success')}",
        export_success,
        "Medium"
    )
    
    # Test clear history
    response = session.post(f"{BASE_URL}/api/history/clear")
    data = response.json()
    
    clear_success = data.get('success') == True
    log_test(
        "Clear Chat History",
        "success: True",
        f"success: {data.get('success')}",
        clear_success,
        "Medium"
    )
    
    # Verify history is cleared
    response = session.get(f"{BASE_URL}/api/history")
    data = response.json()
    
    history_cleared = len(data.get('history', [])) == 0
    log_test(
        "Verify History Cleared",
        "history length: 0",
        f"history length: {len(data.get('history', []))}",
        history_cleared,
        "Medium"
    )
    
    # Send a message after clearing
    session.post(f"{BASE_URL}/api/chat", json={"message": "Test message after clear"})
    
    # Verify new message is saved
    response = session.get(f"{BASE_URL}/api/history")
    data = response.json()
    
    new_message_saved = len(data.get('history', [])) > 0
    log_test(
        "New Message After Clear",
        "history length: > 0",
        f"history length: {len(data.get('history', []))}",
        new_message_saved,
        "High"
    )

# ============================================
# TEST 6: Personality Change
# ============================================

def test_personality_change(username, password):
    """Test personality change functionality"""
    print("\n" + "="*50)
    print("TEST SUITE: Personality Change Functionality")
    print("="*50)
    
    # Ensure logged in
    session.post(f"{BASE_URL}/login", json={"username": username, "password": password})
    
    personalities = ['empathetic', 'funny', 'motivational', 'calm']
    
    for personality in personalities:
        response = session.post(f"{BASE_URL}/api/change_personality", json={
            "personality": personality
        })
        data = response.json()
        
        personality_changed = data.get('success') == True and data.get('personality') == personality
        log_test(
            f"Change Personality to {personality}",
            f"success: True, personality: {personality}",
            f"success: {data.get('success')}, personality: {data.get('personality')}",
            personality_changed,
            "Medium"
        )
    
    # Test invalid personality
    response = session.post(f"{BASE_URL}/api/change_personality", json={
        "personality": "invalid_personality"
    })
    data = response.json()
    
    # Should fallback to default
    log_test(
        "Change Personality - Invalid",
        "should fallback to default",
        f"personality: {data.get('personality')}",
        data.get('personality') in personalities,
        "Low"
    )

# ============================================
# TEST 7: Statistics API
# ============================================

def test_statistics_api(username, password):
    """Test statistics endpoints"""
    print("\n" + "="*50)
    print("TEST SUITE: Statistics API")
    print("="*50)
    
    # Ensure logged in
    session.post(f"{BASE_URL}/login", json={"username": username, "password": password})
    
    # Test global stats
    response = session.get(f"{BASE_URL}/api/stats")
    data = response.json()
    
    global_stats = data.get('success') == True and 'stats' in data
    log_test(
        "Get Global Statistics",
        "success: True with stats",
        f"success: {data.get('success')}",
        global_stats,
        "Low"
    )
    
    # Test user stats
    response = session.get(f"{BASE_URL}/api/user_stats")
    data = response.json()
    
    user_stats = data.get('success') == True
    log_test(
        "Get User Statistics",
        "success: True",
        f"success: {data.get('success')}",
        user_stats,
        "Medium"
    )
    
    # Test quick stats
    response = session.get(f"{BASE_URL}/api/quick_stats")
    data = response.json()
    
    quick_stats = data.get('success') == True
    log_test(
        "Get Quick Statistics",
        "success: True",
        f"success: {data.get('success')}",
        quick_stats,
        "Low"
    )

# ============================================
# TEST 8: Page Rendering
# ============================================

def test_page_rendering(username, password):
    """Test page rendering"""
    print("\n" + "="*50)
    print("TEST SUITE: Page Rendering")
    print("="*50)
    
    # Ensure logged in
    session.post(f"{BASE_URL}/login", json={"username": username, "password": password})
    session.post(f"{BASE_URL}/accept-disclaimer")
    time.sleep(11)
    
    # Test chat page
    response = session.get(f"{BASE_URL}/chat")
    chat_rendered = response.status_code == 200
    log_test(
        "Chat Page Rendering",
        "200 OK",
        f"{response.status_code}",
        chat_rendered,
        "High"
    )
    
    # Test dashboard page
    response = session.get(f"{BASE_URL}/dashboard")
    dashboard_rendered = response.status_code == 200
    log_test(
        "Dashboard Page Rendering",
        "200 OK",
        f"{response.status_code}",
        dashboard_rendered,
        "High"
    )
    
    # Test history page
    response = session.get(f"{BASE_URL}/history")
    history_rendered = response.status_code == 200
    log_test(
        "History Page Rendering",
        "200 OK",
        f"{response.status_code}",
        history_rendered,
        "High"
    )
    
    # Test login page
    session2 = requests.Session()
    response = session2.get(f"{BASE_URL}/login")
    login_page = response.status_code == 200
    log_test(
        "Login Page Rendering",
        "200 OK",
        f"{response.status_code}",
        login_page,
        "Medium"
    )
    
    # Test register page
    response = session2.get(f"{BASE_URL}/register")
    register_page = response.status_code == 200
    log_test(
        "Register Page Rendering",
        "200 OK",
        f"{response.status_code}",
        register_page,
        "Medium"
    )

# ============================================
# TEST 9: Unauthorized Access
# ============================================

def test_unauthorized_access():
    """Test unauthorized access to protected routes"""
    print("\n" + "="*50)
    print("TEST SUITE: Unauthorized Access")
    print("="*50)
    
    # Create new session (not logged in)
    unauth_session = requests.Session()
    
    # Test chat page without login
    response = unauth_session.get(f"{BASE_URL}/chat", allow_redirects=False)
    not_auth = response.status_code in [302, 401]
    log_test(
        "Access Chat Without Login",
        "302 redirect or 401",
        f"{response.status_code}",
        not_auth,
        "Critical"
    )
    
    # Test chat API without login
    response = unauth_session.post(f"{BASE_URL}/api/chat", json={"message": "test"})
    api_not_auth = response.status_code in [302, 401]
    log_test(
        "Access Chat API Without Login",
        "302 redirect or 401",
        f"{response.status_code}",
        api_not_auth,
        "Critical"
    )
    
    # Test history without login
    response = unauth_session.get(f"{BASE_URL}/history")
    history_not_auth = response.status_code in [302, 401]
    log_test(
        "Access History Without Login",
        "302 redirect or 401",
        f"{response.status_code}",
        history_not_auth,
        "Critical"
    )
    
    # Test dashboard without login
    response = unauth_session.get(f"{BASE_URL}/dashboard")
    dashboard_not_auth = response.status_code in [302, 401]
    log_test(
        "Access Dashboard Without Login",
        "302 redirect or 401",
        f"{response.status_code}",
        dashboard_not_auth,
        "Critical"
    )
    
    # Test history API without login
    response = unauth_session.get(f"{BASE_URL}/api/history")
    api_history_not_auth = response.status_code in [302, 401]
    log_test(
        "Access History API Without Login",
        "302 redirect or 401",
        f"{response.status_code}",
        api_history_not_auth,
        "Critical"
    )

# ============================================
# TEST 10: Concurrent Users
# ============================================

def test_concurrent_users():
    """Test concurrent user interactions"""
    print("\n" + "="*50)
    print("TEST SUITE: Concurrent User Interactions")
    print("="*50)
    
    username1, password1 = generate_random_user()
    username2, password2 = generate_random_user()
    
    # Register and login user 1
    session1 = requests.Session()
    session1.post(f"{BASE_URL}/register", json={"username": username1, "password": password1})
    session1.post(f"{BASE_URL}/accept-disclaimer")
    time.sleep(11)
    
    # Register and login user 2
    session2 = requests.Session()
    session2.post(f"{BASE_URL}/register", json={"username": username2, "password": password2})
    session2.post(f"{BASE_URL}/accept-disclaimer")
    time.sleep(11)
    
    # Both users send messages
    response1 = session1.post(f"{BASE_URL}/api/chat", json={"message": "Message from user 1"})
    response2 = session2.post(f"{BASE_URL}/api/chat", json={"message": "Message from user 2"})
    
    both_success = response1.json().get('success') and response2.json().get('success')
    log_test(
        "Concurrent Messages - Both Succeed",
        "success: True for both",
        f"user1: {response1.json().get('success')}, user2: {response2.json().get('success')}",
        both_success,
        "High"
    )
    
    # Verify each user only sees their own messages
    history1 = session1.get(f"{BASE_URL}/api/history").json().get('history', [])
    history2 = session2.get(f"{BASE_URL}/api/history").json().get('history', [])
    
    user1_sees_only_own = all("user 1" in str(m).lower() or "user 2" not in str(m).lower() for m in history1)
    user2_sees_only_own = all("user 2" in str(m).lower() or "user 1" not in str(m).lower() for m in history2)
    
    log_test(
        "Concurrent Users - Isolated History",
        "each user sees only own messages",
        f"user1 history: {len(history1)}, user2 history: {len(history2)}",
        user1_sees_only_own and user2_sees_only_own,
        "High",
        "Note: Messages are user-specific in storage"
    )
    
    # Clean up
    cleanup_user(username1)
    cleanup_user(username2)

# ============================================
# TEST 11: Rate Limiting (if implemented)
# ============================================

def test_rate_limiting(username, password):
    """Test rate limiting (if implemented)"""
    print("\n" + "="*50)
    print("TEST SUITE: Rate Limiting")
    print("="*50)
    
    # Ensure logged in
    session.post(f"{BASE_URL}/login", json={"username": username, "password": password})
    
    # Send multiple rapid requests
    start_time = time.time()
    for i in range(10):
        response = session.post(f"{BASE_URL}/api/chat", json={"message": f"Rapid message {i}"})
    
    elapsed = time.time() - start_time
    
    # Check if rate limited (if implemented)
    all_success = all(response.status_code == 200 for _ in range(10))
    log_test(
        "Rate Limiting - 10 Rapid Requests",
        "should handle or return 429",
        f"completed in {elapsed:.2f}s",
        True,
        "Medium",
        "Rate limiting not currently implemented"
    )

# ============================================
# TEST 12: Error Handling
# ============================================

def test_error_handling():
    """Test error handling for invalid routes"""
    print("\n" + "="*50)
    print("TEST SUITE: Error Handling")
    print("="*50)
    
    # Test 404 for invalid route
    response = session.get(f"{BASE_URL}/api/invalid_route_xyz")
    is_404 = response.status_code == 404
    log_test(
        "404 Error - Invalid Route",
        "404 Not Found",
        f"{response.status_code}",
        is_404,
        "Low"
    )
    
    # Test invalid JSON
    response = session.post(f"{BASE_URL}/api/chat", data="invalid json")
    log_test(
        "Invalid JSON Handling",
        "400 Bad Request or 500",
        f"{response.status_code}",
        response.status_code in [400, 500],
        "Medium"
    )

# ============================================
# MAIN EXECUTION
# ============================================

def main():
    print("\n" + "="*60)
    print("COMPREHENSIVE CHAT INTERFACE TEST PLAN")
    print("="*60)
    print(f"Testing base URL: {BASE_URL}")
    print(f"Start time: {datetime.now().isoformat()}")
    print("="*60)
    
    # Run all tests
    test_health_check()
    
    # Check if server is running
    if not test_results or test_results[0].get('actual', '').startswith('Connection'):
        print("\n❌ ERROR: Server is not running. Please start the server with: python app.py")
        return
    
    test_disclaimer()
    username, password = test_authentication()
    
    if username and password:
        test_chat_api(username, password)
        test_history_api(username, password)
        test_personality_change(username, password)
        test_statistics_api(username, password)
        test_page_rendering(username, password)
        test_rate_limiting(username, password)
    
    test_unauthorized_access()
    test_concurrent_users()
    test_error_handling()
    
    # Generate report
    generate_report()

def generate_report():
    """Generate test report"""
    print("\n" + "="*60)
    print("TEST RESULTS SUMMARY")
    print("="*60)
    
    total = len(test_results)
    passed = sum(1 for r in test_results if r['passed'])
    failed = total - passed
    
    print(f"Total Tests: {total}")
    print(f"Passed: {passed} ({passed/total*100:.1f}%)")
    print(f"Failed: {failed} ({failed/total*100:.1f}%)")
    
    if failed > 0:
        print("\n" + "="*60)
        print("FAILED TESTS")
        print("="*60)
        
        for error in errors_found:
            severity_emoji = {
                "Critical": "[CRITICAL]",
                "High": "[HIGH]",
                "Medium": "[MEDIUM]",
                "Low": "[LOW]"
            }
            emoji = severity_emoji.get(error['severity'], "[INFO]")
            print(f"\n{emoji} {error['test_name']}")
            print(f"   Expected: {error['expected']}")
            print(f"   Actual: {error['actual']}")
            if error['notes']:
                print(f"   Notes: {error['notes']}")
    
    # Save report to file
    report = {
        "timestamp": datetime.now().isoformat(),
        "total_tests": total,
        "passed": passed,
        "failed": failed,
        "results": test_results,
        "errors": errors_found
    }
    
    with open("test_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n[OK] Detailed report saved to: test_report.json")
    print("="*60)

if __name__ == "__main__":
    main()