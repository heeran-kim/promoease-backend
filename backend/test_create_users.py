import os
import django
import requests
from bs4 import BeautifulSoup  # CSRF 토큰 추출용

# Django 환경 설정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from users.models import User

# API 기본 URL
BASE_URL = "http://localhost:8000/api/users"
ADMIN_URL = "http://localhost:8000/admin"

# 세션 생성 (API 요청 간 인증 유지)
session = requests.Session()

def create_user():
    """Create a test user directly in the database"""
    try:
        user = User.objects.create_user(email="test@example.com", name="Test User", password="testpassword")
        print(f"✅ User Created: {user.email} | is_admin: {user.is_admin()}")
    except Exception as e:
        print(f"❌ User Creation Failed: {e}")

def create_superuser():
    """Create a superuser directly in the database"""
    try:
        admin = User.objects.create_superuser(email="admin@example.com", name="Admin User", password="adminpassword")
        print(f"✅ Admin Created: {admin.email} | is_admin: {admin.is_admin()}")
    except Exception as e:
        print(f"❌ Admin Creation Failed: {e}")

def register_user():
    """Test user registration via API"""
    url = f"{BASE_URL}/register/"
    data = {
        "email": "test@example.com",
        "name": "Test User",
        "password": "testpassword"
    }
    response = session.post(url, json=data)

    if response.status_code == 201:
        print(f"✅ API: User registered successfully: {response.json()}")
    else:
        print(f"❌ API: Registration failed: {response.status_code} | {response.text}")

def login_user():
    """Test user login via API"""
    url = f"{BASE_URL}/login/"
    data = {
        "email": "test@example.com",
        "password": "testpassword"
    }

    print(f"🔍 Sending login request to {url} with data: {data}")
    response = session.post(url, json=data)

    print(f"🔍 Response Status: {response.status_code}")
    print(f"🔍 Response Text: {response.text}")

    if response.status_code == 200:
        data = response.json()
        access_token = data.get("access")
        print(f"✅ API: Login successful: {data}")

        # 세션에 Authorization 헤더 추가
        session.headers.update({"Authorization": f"Bearer {access_token}"})
        return access_token
    else:
        print(f"❌ API: Login failed: {response.status_code} | {response.text}")
        return None

def get_csrf_token():
    """Retrieve CSRF token from Django Admin login page"""
    response = session.get(f"{ADMIN_URL}/login/")
    if response.status_code != 200:
        print(f"❌ Failed to get CSRF token: {response.status_code}")
        return None

    # HTML 파싱하여 CSRF 토큰 추출
    soup = BeautifulSoup(response.text, "html.parser")
    csrf_token = soup.find("input", {"name": "csrfmiddlewaretoken"})

    if csrf_token:
        return csrf_token["value"]
    print("❌ CSRF token not found.")
    return None

def admin_login():
    """Test Django Admin login with CSRF token"""
    csrf_token = get_csrf_token()
    if not csrf_token:
        print("❌ Admin login failed: No CSRF token")
        return

    login_data = {
        "csrfmiddlewaretoken": csrf_token,
        "username": "admin@example.com",
        "password": "adminpassword",
        "next": "/admin/"  # 로그인 후 이동할 페이지
    }

    headers = {
        "Referer": f"{ADMIN_URL}/login/"  # CSRF 보호를 위해 Referer 설정
    }

    response = session.post(f"{ADMIN_URL}/login/", data=login_data, headers=headers)

    if response.status_code == 200 or response.status_code == 302:  # 302면 리다이렉트 성공
        print("✅ Django Admin login successful!")
    else:
        print(f"❌ Django Admin login failed: {response.status_code} | {response.text}")

def test_admin_access():
    """Test if the admin user has access to Django admin panel"""
    response = session.get(f"{ADMIN_URL}/")

    if response.status_code == 200:
        print("✅ Django Admin panel access confirmed!")
    else:
        print(f"❌ Django Admin access denied: {response.status_code} | {response.text}")

if __name__ == "__main__":
    print("🚀 Running authentication tests...\n")

    # 기존 사용자 삭제 (테스트 초기화)
    User.objects.filter(email="test@example.com").delete()
    User.objects.filter(email="admin@example.com").delete()

    # Step 1: 사용자 & 관리자 계정 생성 (Django ORM)
    create_user()
    create_superuser()

    # Step 2: 사용자 계정 삭제 후 API 등록 & 로그인 테스트
    User.objects.filter(email="test@example.com").delete()
    register_user()
    user_token = login_user()

    # Step 3: 관리자 로그인 및 Django Admin 접근 테스트
    admin_login()
    test_admin_access()