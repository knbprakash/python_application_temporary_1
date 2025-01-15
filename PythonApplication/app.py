from flask import Flask, request, jsonify
from service.service import Service
import os
from werkzeug.utils import secure_filename
import pymysql.cursors
from service.text_utils import TextUtils

# Create an instance of the Flask class that is the WSGI application.
# The first argument is the name of the application module or package,
# typically __name__ when using a single module.
app = Flask(__name__)

# Allowed extensions
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

# Database connection
def get_db_connection():
    """Establish and return a database connection."""
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='Pragna@2001',
        database='makethon_db',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/documents/upload', methods = ['POST'])
def upload_documents():
    """Upload a file."""
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request."}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file."}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            if filename.lower().endswith('.docx'):
                text = TextUtils.extract_text_from_docx(filepath)
            elif filename.lower().endswith('.pdf'):
                text = TextUtils.extract_text_from_pdf(filepath)
            else:
                return jsonify({"error": "Unsupported file type."}), 400

            connection = get_db_connection()
            with connection.cursor() as cursor:
                query = "INSERT INTO files (filename, content) VALUES (%s, %s)"
                cursor.execute(query, (filename, text))
                connection.commit()

            response = Service.processDocuments(file)

            return jsonify({"message": "File uploaded and stored successfully.", "filename": filename}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            os.remove(filepath)  # Clean up the uploaded file
            connection.close()
    else:
        return jsonify({"error": "Invalid file type."}), 400

@app.route('/questions/ask', methods=['POST'])
def ask_question():
    """Process a question."""
    data = request.get_json()
    question = data.get('question')

    if not question:
        return jsonify({"error": "A question is required."}), 400

    # Placeholder logic for answering the question
    answer = f"You asked: '{question}'. Here's the answer: This is a sample response."
    return jsonify({"question": question, "answer": answer}), 200

@app.route('/files/<filename>', methods=['GET'])
def get_file_content(filename):
    """Retrieve content of a file."""
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = "SELECT content FROM files WHERE filename = %s"
            cursor.execute(query, (filename,))
            file_data = cursor.fetchone()

        if file_data:
            return jsonify({"filename": filename, "content": file_data['content']}), 200
        else:
            return jsonify({"error": "File not found."}), 404
    finally:
        connection.close()

@app.route('/auth/login', methods=['POST'])
def login():
    """User login."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()

        if user:
            return jsonify({"message": "Login successful."}), 200
        else:
            return jsonify({"error": "Invalid username or password."}), 401
    finally:
        connection.close()

@app.route('/auth/signup', methods=['POST'])
def signup():
    """User signup."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = "INSERT INTO users (username, password) VALUES (%s, %s)"
            cursor.execute(query, (username, password))
            connection.commit()
        return jsonify({"message": "User registered successfully."}), 201
    except pymysql.IntegrityError:
        return jsonify({"error": "Username already exists."}), 400
    finally:
        connection.close()

if __name__ == '__main__':
   # Run the app server on localhost:4449
   app.run('localhost', 4449)