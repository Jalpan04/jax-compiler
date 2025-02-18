import subprocess
import sys
import os
from flask import Flask, render_template, request

# Set template folder to the current working directory
app = Flask(__name__, template_folder=os.getcwd())

@app.route('/')
def index():
    return render_template('index.html')  # Flask will now look for 'index.html' in the root folder

@app.route('/run', methods=['POST'])
def run_code():
    if request.method == 'POST':
        code = request.form.get('code')

        if not code:
            return render_template('index.html', error="No code provided!")

        # Save the code in a temporary Python file
        with open('temp_code.py', 'w') as file:
            file.write(code)

        # Run the Python file and capture output
        try:
            result = subprocess.run([sys.executable, 'temp_code.py'], capture_output=True, text=True, timeout=5)

            # Check if there is output or error
            output = result.stdout
            error = result.stderr

            if result.returncode != 0:
                error = f"Error: {error if error else 'Unknown error occurred'}"
                output = None

        except subprocess.TimeoutExpired:
            output = None
            error = 'Error: Timeout exceeded while executing the code.'
        except Exception as e:
            output = None
            error = f"An unexpected error occurred: {str(e)}"

        # Clean up by removing the temporary file
        os.remove('temp_code.py')

        return render_template('index.html', code=code, output=output, error=error)

if __name__ == '__main__':
    app.run(debug=True)
