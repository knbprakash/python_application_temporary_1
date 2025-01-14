from flask import Flask, request, jsonify
from service.service import Service

# Create an instance of the Flask class that is the WSGI application.
# The first argument is the name of the application module or package,
# typically __name__ when using a single module.
app = Flask(__name__)

# Flask route decorators map / and /hello to the hello function.
# To add other resources, create functions that generate the page contents
# and add decorators to define the appropriate resource locators for them.

# Allowed extensions
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/hello')
def hello():
   # Render the page
   return "Hello Python!"

@app.route('/documents/upload', methods = ['POST'])
def upload_documents():

    if 'files' not in request.files:
        return jsonify({"error": "No files part in the request"}), 400

    files = request.files.getlist('files')
    if not files:
        return jsonify({"error": "No files provided"}), 400

    response = Service.processDocuments()

    return jsonify(response), 200

if __name__ == '__main__':
   # Run the app server on localhost:4449
   app.run('localhost', 4449)