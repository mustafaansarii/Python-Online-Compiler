from flask import Flask, render_template, request, send_file, jsonify
import subprocess
import os
import tempfile
import sys

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_code():
    code = request.form.get('code')
    
    # Create a temporary file to save the code
    with tempfile.NamedTemporaryFile(delete=False, suffix='.py') as temp_file:
        file_path = temp_file.name
        temp_file.write(code.encode('utf-8'))
    
    try:
        # Use the correct Python executable (either 'python' or 'python3')
        python_executable = sys.executable
        result = subprocess.run([python_executable, file_path], capture_output=True, text=True, timeout=10)
        output = result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        output = 'Error: Code execution timed out.'
    except Exception as e:
        output = f'Error: {str(e)}'
    finally:
        # Clean up the temporary file after execution
        os.remove(file_path)
    
    return jsonify({'output': output})

@app.route('/download', methods=['POST'])
def download():
    code = request.form.get('code')
    
    # Create a temporary file to save the code
    with tempfile.NamedTemporaryFile(delete=False, suffix='.py') as temp_file:
        file_path = temp_file.name
        temp_file.write(code.encode('utf-8'))
    
    # Return the code file as a download
    return send_file(file_path, as_attachment=True, download_name='main.py')

if __name__ == '__main__':
    app.run(debug=True)