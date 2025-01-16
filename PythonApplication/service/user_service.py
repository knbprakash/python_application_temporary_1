import pymysql.cursors
from flask import jsonify

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

    def signup(self, username, password):
        if not username or not password:
            return jsonify({"error": "Username and password are required."}), 400

        try:
            connection = self.get_db_connection()
            with connection.cursor() as cursor:
                query = "INSERT INTO users (username, password) VALUES (%s, %s)"
                cursor.execute(query, (username, password))
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

