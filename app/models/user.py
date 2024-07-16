from app.config.mysqlconnection import connectToMySQL
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password_hash = data['password_hash']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_user_data(first_name, last_name, email, password, password_confirmation):
        errors = []
        if len(first_name) < 2:
            errors.append("First name must be at least 2 characters long.")
        if len(last_name) < 2:
            errors.append("Last name must be at least 2 characters long.")
        if not EMAIL_REGEX.match(email):
            errors.append("Invalid email address.")
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long.")
        if password != password_confirmation:
            errors.append("Passwords do not match.")
        if User.get_by_email(email):
            errors.append("Email already registered.")
        return errors

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO users (first_name, last_name, email, password_hash)
            VALUES (%s, %s, %s, %s)
        """
        data = (
            data['first_name'], data['last_name'], data['email'], data['password_hash']
        )
        return connectToMySQL('spending').query_db(query, data)

    @classmethod
    def get_by_email(cls, email):
        query = "SELECT * FROM users WHERE email = %s"
        result = connectToMySQL('spending').query_db(query, (email,))
        if result:
            return cls(result[0])
        return None

    @classmethod
    def get_by_id(cls, user_id):
        query = "SELECT * FROM users WHERE id = %s"
        result = connectToMySQL('spending').query_db(query, (user_id,))
        if result:
            return cls(result[0])
        return None

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def check_password(password, hashed_password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
