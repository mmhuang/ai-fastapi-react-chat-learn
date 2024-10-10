import httpx
from backend.main import app
from models.user import fake_users_db

class TestAuthRoutes:
    def test_register_user(self):
        test_user = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword"
        }
        response = httpx.post(
            "http://localhost:8000/users/",
            json=test_user
        )
        assert response.status_code == 200
        assert response.json()["email"] == test_user["email"]
        fake_users_db.pop(test_user["email"], None)  # Clean up the fake database

    def test_register_user_with_existing_email(self):
        test_user = {
            "username": "testuser",
            "email": "existinguser@example.com",
            "password": "testpassword"
        }
        # Add the user to the fake database
        fake_users_db[test_user["email"]] = {
            "username": test_user["username"],
            "email": test_user["email"],
            "hashed_password": "hashed_password"
        }
        response = httpx.post(
            "http://localhost:8000/users/",
            json=test_user
        )
        assert response.status_code == 400
        fake_users_db.pop(test_user["email"], None)  # Clean up the fake database

    def test_login(self):
        test_user = {
            "username": "existinguser",
            "password": "correctpassword"
        }
        # Add the user to the fake database
        fake_users_db[test_user["username"]] = {
            "username": test_user["username"],
            "email": "existinguser@example.com",
            "hashed_password": "correctpassword"
        }
        response = httpx.post(
            "http://localhost:8000/token",
            json=test_user
        )
        assert response.status_code == 200
        fake_users_db.pop(test_user["username"], None)  # Clean up the fake database

    def test_login_with_wrong_password(self):
        test_user = {
            "username": "existinguser",
            "password": "wrongpassword"
        }
        # Add the user to the fake database
        fake_users_db[test_user["username"]] = {
            "username": test_user["username"],
            "email": "existinguser@example.com",
            "hashed_password": "correctpassword"
        }
        response = httpx.post(
            "http://localhost:8000/token",
            json=test_user
        )
        assert response.status_code == 401
        fake_users_db.pop(test_user["username"], None)  # Clean up the fake database

# Run the tests
if __name__ == "__main__":
    import unittest
    unittest.main()
`