import pymysql.cursors
from flask import jsonify
import bcrypt

from model.User import User

class UserService:

    # Database connection
    def get_db_connection():
        """Establish and return a database connection."""
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='root',
            database='makeathon_db',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection

    # Hash the password
    def hash_password(plain_password):
        # Generate the salted hash
        hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())
        return hashed_password

    # Verify the password
    def verify_password(plain_password, hashed_password):
        # bcrypt automatically extracts the salt from the hashed_password
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    def signup(self, username, password):
        # Hash password before saving it to the database
        hashed_password = UserService.hash_password(password)
        connection = UserService.get_db_connection()
        try:
            with connection.cursor() as cursor:
                query = "INSERT INTO users (username, password) VALUES (%s, %s)"
                cursor.execute(query, (username, hashed_password))
                connection.commit()

            return jsonify({"message": "User registered successfully."}), 201
        except pymysql.IntegrityError:
            return jsonify({"error": "Username already exists."}), 400
        finally:
            connection.close()

    def getUser(self, username):
        connection = UserService.get_db_connection()
        try:
            user = None
            with connection.cursor() as cursor:
                query = "SELECT * FROM users WHERE username = %s"
                cursor.execute(query, (username))
                result = cursor.fetchone()

                user = User(id=result['username'], password=result['password'])

            return user
        finally:
            connection.close()

