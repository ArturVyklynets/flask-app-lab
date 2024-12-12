import unittest
from app import create_app, db, bcrypt
from app.users.models import User
from flask import session
class UserTests(unittest.TestCase):

    def setUp(self):
        """Налаштування перед кожним тестом."""
        self.app = create_app("test")  # Тестова конфігурація
        print(self.app.config["SQLALCHEMY_DATABASE_URI"]) 
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

        # Створення тестового користувача
        hashed_password = bcrypt.generate_password_hash("password123").decode('utf-8')
        self.user = User(username="testuser", email="test@example.com", password=hashed_password)
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        """Очистка після кожного тесту."""
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    # --- Тестування Views ---

    def test_registration_page_loads(self):
        """Перевіряє, чи сторінка реєстрації завантажується успішно."""
        response = self.client.get("/hi/register")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Register", response.data)

    def test_login_page_loads(self):
        """Перевіряє, чи сторінка входу завантажується успішно."""
        response = self.client.get("/hi/login")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login", response.data)

    # --- Тестування реєстрації ---

    def test_user_registration(self):
        """Перевіряє, чи користувач успішно зберігається в базі."""
        response = self.client.post("/hi/register", data={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123",
            "confirm_password": "password123"
        })
        self.assertEqual(response.status_code, 302)

        user = User.query.filter_by(email="newuser@example.com").first()
        self.assertIsNotNone(user)
        self.assertTrue(bcrypt.check_password_hash(user.password, "password123"))

    # --- Тестування входу та виходу ---

    def test_user_login(self):
        """Перевіряє функціональність входу."""
        response = self.client.post("/hi/login", data={
            "email": "test@example.com",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 302) 

        # Перевірка чи сесія створена
        with self.client:
            self.client.get("/")
            self.assertIn("_user_id", session)

    def test_user_logout(self):
        """Перевіряє функціональність виходу."""
        # Спочатку вхід
        self.client.post("/hi/login", data={
            "email": "test@example.com",
            "password": "password123"
        })
        response = self.client.get("/hi/logout")
        self.assertEqual(response.status_code, 302)  # Перенаправлення після виходу

        # Перевірка чи сесія видалена
        with self.client:
            self.client.get("/")
            self.assertNotIn("_user_id", session)
