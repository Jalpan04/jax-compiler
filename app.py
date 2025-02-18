import subprocess
import sys
import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__, template_folder=os.getcwd())
CORS(app)  # Enable CORS to allow cross-origin requests

@app.route('/')
def index():
    return render_template('index.html')  # Serve the frontend

@app.route('/run', methods=['POST'])
def run_code():
    if request.method == 'POST':
        code = request.form.get('code')

        if not code:
            return render_template('index.html', error="No code provided!", code=code)

        # Secure filename
        filename = "temp_code.py"
        safe_filename = secure_filename(filename)

        try:
            # Save code in a temporary file
            with open(safe_filename, 'w') as file:
                file.write(code)

            # Execute the code safely with a timeout
            result = subprocess.run(
                [sys.executable, safe_filename],
                capture_output=True, text=True, timeout=5
            )

            output = result.stdout if result.returncode == 0 else None
            error = result.stderr if result.returncode != 0 else None

        except subprocess.TimeoutExpired:
            output = None
            error = "Error: Timeout exceeded while executing the code."
        except Exception as e:
            output = None
            error = f"An unexpected error occurred: {str(e)}"
        finally:
            # Remove the temporary file after execution
            if os.path.exists(safe_filename):
                os.remove(safe_filename)

        return render_template('index.html', code=code, output=output, error=error)

if __name__ == '__main__':
    app.run(debug=True)
