import django
import os
import requests
from rest_framework.exceptions import ValidationError

# Django 환경 설정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from users.serializers import RegisterSerializer, LoginSerializer
from users.models import User

# API 기본 URL
BASE_URL = "http://localhost:8000/api/users"

# 세션 생성 (API 요청 간 인증 유지)
session = requests.Session()


def test_valid_registration():
    """Test valid user registration"""
    data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpassword",
        "role": "restaurant_owner"
    }

    # 기존 사용자 삭제
    User.objects.filter(email=data["email"]).delete()

    serializer = RegisterSerializer(data=data)
    assert serializer.is_valid(), f"❌ Validation failed: {serializer.errors}"

    user = serializer.save()
    assert user.role == "restaurant_owner", f"❌ Role mismatch: Expected 'restaurant_owner', got {user.role}"

    print(f"✅ Registration Successful: {user.email}, Role: {user.role}")

def test_without_role_registration():
    """Test user registration without specifying a role"""
    data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpassword"
    }

    # 기존 사용자 삭제
    User.objects.filter(email=data["email"]).delete()

    serializer = RegisterSerializer(data=data)
    assert serializer.is_valid(), f"❌ Validation failed: {serializer.errors}"

    user = serializer.save()
    assert user.role == "restaurant_owner", f"❌ Role mismatch: Expected 'restaurant_owner', got {user.role}"

    print(f"✅ Registration Successful (No Role Provided): {user.email}, Role: {user.role}")


def test_invalid_role():
    """Test user registration with an invalid role"""
    data = {
        "name": "Invalid Role User",
        "email": "invalidrole@example.com",
        "password": "testpassword",
        "role": "invalid_role"
    }

    serializer = RegisterSerializer(data=data)
    try:
        serializer.is_valid(raise_exception=True)
    except ValidationError as e:
        error_detail = e.detail.get("role", [""])[0]  # role 필드에서 첫 번째 오류 메시지 가져오기
        assert "is not a valid choice." in error_detail, f"❌ Unexpected error: {e.detail}"
        print(f"✅ Invalid Role Test Passed: {error_detail}")


def test_login_user():
    """Test correct user login via serializer"""
    data = {
        "email": "test@example.com",
        "password": "testpassword"
    }
    serializer = LoginSerializer(data=data)
    assert serializer.is_valid(), f"❌ Login failed: {serializer.errors}"

    tokens = serializer.validated_data
    assert "access" in tokens, "❌ Missing access token"
    assert "refresh" in tokens, "❌ Missing refresh token"

    print(f"✅ Serializer: Login successful: {tokens}")

def test_login_invalid_password():
    """Test login failure with incorrect password"""
    data = {
        "email": "test@example.com",
        "password": "wrongpassword"
    }
    serializer = LoginSerializer(data=data)
    assert not serializer.is_valid(), "❌ Login should have failed, but it succeeded"
    print(f"✅ Serializer: Expected login failure: {serializer.errors}")

def test_login_invalid_email():
    """Test login failure with incorrect email"""
    data = {
        "email": "wrong@example.com",
        "password": "testpassword"
    }
    serializer = LoginSerializer(data=data)
    assert not serializer.is_valid(), "❌ Login should have failed, but it succeeded"
    print(f"✅ Serializer: Expected login failure: {serializer.errors}")

if __name__ == "__main__":
    print("🚀 Running serializer tests...\n")

    # Step 1: 유저 등록 테스트
    test_valid_registration()
    test_without_role_registration()
    test_invalid_role()

    # Step 2: 로그인 테스트 (정상 + 실패 케이스)
    test_login_user()
    test_login_invalid_password()
    test_login_invalid_email()
