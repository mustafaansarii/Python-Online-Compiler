from flask import Flask, render_template, request, send_file, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_code():
    code = request.form.get('code')
    file_path = 'temp_code.py'
    with open(file_path, 'w') as file:
        file.write(code)
    
    try:
        result = subprocess.run(['python', file_path], capture_output=True, text=True, timeout=10)
        output = result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        output = 'Error: Code execution timed out.'
    except Exception as e:
        output = f'Error: {str(e)}'
    finally:
        os.remove(file_path)
    
    return jsonify({'output': output})

@app.route('/download', methods=['POST'])
def download():
    code = request.form.get('code')
    file_path = 'app.py'
    with open(file_path, 'w') as file:
        file.write(code)
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
