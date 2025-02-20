import django
import os
import requests
from django.contrib.auth import get_user_model
from rest_framework import status

# Django 환경 설정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from users.serializers import RegisterSerializer, LoginSerializer

# API 기본 URL
BASE_URL = "http://localhost:8000/api/users"

# 세션 생성 (쿠키 기반 인증 유지)
session = requests.Session()

# Django User Model 가져오기
User = get_user_model()

# ✅ 로그 출력용 함수
def log_result(test_name, success, details=""):
    icon = "✅" if success else "❌"
    print(f"{icon} {test_name}: {details}")

# ✅ 테스트 전 기존 사용자 삭제
def reset_users():
    User.objects.filter(email="test@example.com").delete()
    User.objects.filter(email="admin@example.com").delete()

# ✅ 회원가입 테스트 (성공)
def test_register_user():
    """Test successful user registration"""
    reset_users()
    data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpassword",
        "role": "restaurant_owner"
    }
    response = session.post(f"{BASE_URL}/register/", json=data)

    if response.status_code == status.HTTP_201_CREATED:
        log_result("Register User", True, response.json())
    else:
        log_result("Register User", False, response.text)

# ✅ 회원가입 테스트 (이메일 형식 오류)
def test_register_invalid_email():
    """Test registration with an invalid email"""
    data = {
        "name": "Invalid Email User",
        "email": "invalid-email",
        "password": "testpassword",
        "role": "restaurant_owner"
    }
    response = session.post(f"{BASE_URL}/register/", json=data)

    if response.status_code == status.HTTP_400_BAD_REQUEST:
        log_result("Register Invalid Email", True, response.json())
    else:
        log_result("Register Invalid Email", False, response.text)

# ✅ 회원가입 테스트 (비밀번호 너무 짧음)
def test_register_short_password():
    """Test registration with a short password"""
    data = {
        "name": "Short Password User",
        "email": "shortpass@example.com",
        "password": "123",
        "role": "restaurant_owner"
    }
    response = session.post(f"{BASE_URL}/register/", json=data)

    if response.status_code == status.HTTP_400_BAD_REQUEST:
        log_result("Register Short Password", True, response.json())
    else:
        log_result("Register Short Password", False, response.text)

# ✅ 로그인 테스트 (성공)
def test_login_user():
    """Test successful user login (JWT stored in HttpOnly Cookie)"""
    data = {
        "email": "test@example.com",
        "password": "testpassword"
    }
    response = session.post(f"{BASE_URL}/login/", json=data)

    # ✅ 응답 헤더 및 쿠키 정보 출력
    print("\n🔍 Response Headers:", response.headers)
    print("🔍 Response JSON:", response.text)
    print("🔍 Response Cookies (Direct):", response.cookies.get_dict())
    print("🔍 Session Cookies (Stored):", session.cookies.get_dict())

    # ✅ Set-Cookie 확인
    set_cookie_header = response.headers.get("Set-Cookie")

    if response.status_code == status.HTTP_200_OK and set_cookie_header:
        log_result("Login User", True, "JWT stored in HttpOnly Cookie")
    else:
        log_result("Login User", False, response.text)

        # 🚨 Set-Cookie 헤더가 없으면 에러 로그 출력
        if not set_cookie_header:
            print("❌ ERROR: `Set-Cookie` header is missing! JWT is not stored in cookies.")
            print("❌ Possible Issues:")
            print("   - `response.set_cookie()` not executed in LoginView?")
            print("   - `AUTH_COOKIE_HTTP_ONLY` or `CORS_ALLOW_CREDENTIALS` misconfigured?")
            print("   - Django Middleware missing `CsrfViewMiddleware`?")

# ✅ 로그인 테스트 (존재하지 않는 이메일)
def test_login_invalid_email():
    """Test login with a non-existent email"""
    data = {
        "email": "wrong@example.com",
        "password": "testpassword"
    }
    response = session.post(f"{BASE_URL}/login/", json=data)

    if response.status_code == status.HTTP_400_BAD_REQUEST:
        log_result("Login Invalid Email", True, response.json())
    else:
        log_result("Login Invalid Email", False, response.text)

# ✅ 로그인 테스트 (틀린 비밀번호)
def test_login_invalid_password():
    """Test login with an incorrect password"""
    data = {
        "email": "test@example.com",
        "password": "wrongpassword"
    }
    response = session.post(f"{BASE_URL}/login/", json=data)

    if response.status_code == status.HTTP_400_BAD_REQUEST:
        log_result("Login Invalid Password", True, response.json())
    else:
        log_result("Login Invalid Password", False, response.text)

# ✅ 프로필 조회 (성공)
def test_user_profile():
    """Test fetching user profile using stored JWT cookie"""
    test_login_user()  # 로그인 선행
    response = session.get(f"{BASE_URL}/me/")  # 세션 쿠키 기반 인증

    if response.status_code == status.HTTP_200_OK:
        log_result("User Profile", True, response.json())
    else:
        log_result("User Profile", False, response.text)

# 🛑 프로필 조회 (인증 없음)
def test_user_profile_unauthorized():
    """Test fetching user profile without authentication"""
    new_session = requests.Session()  # 인증되지 않은 새 세션 사용
    response = new_session.get(f"{BASE_URL}/me/")

    if response.status_code == status.HTTP_401_UNAUTHORIZED:
        log_result("User Profile Unauthorized", True, response.json())
    else:
        log_result("User Profile Unauthorized", False, response.text)

# ✅ JWT 리프레시 테스트
def test_refresh_token():
    """Test refreshing JWT access token using stored cookie"""
    test_login_user()  # 로그인 후 실행
    response = session.post(f"{BASE_URL}/refresh/")

    if response.status_code == status.HTTP_200_OK:
        log_result("Refresh Token", True, response.json())
    else:
        log_result("Refresh Token", False, response.text)

# ✅ 로그아웃 테스트
def test_logout():
    """Test user logout (clearing JWT cookies)"""
    test_login_user()  # 로그인 후 실행
    response = session.post(f"{BASE_URL}/logout/")

    if response.status_code == status.HTTP_200_OK:
        log_result("Logout", True, "User logged out, cookies cleared")
    else:
        log_result("Logout", False, response.text)

# ✅ 전체 테스트 실행
if __name__ == "__main__":
    print("\n🚀 Running API Tests...\n")

    # test_register_user()
    # test_register_invalid_email()
    # test_register_short_password()
    #
    # test_login_user()
    # test_login_invalid_email()
    # test_login_invalid_password()

    test_user_profile()
    # test_user_profile_unauthorized()
    #
    # test_refresh_token()
    # test_logout()

    print("\n✅ All Tests Completed!\n")