from flask import Flask, render_template, redirect, url_for, request, jsonify
from rebuff import Rebuff
import subprocess
import re
import argparse
import base64 
import requests
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger('werkzeug')
log.disabled = False

__header__ = """
Running...

╔╦╗╔═╗╦  ╔═╗┌─┐  ╔╦╗╦    ╔═╗╔╦╗╔═╗  ╔═╗┬ ┬┌─┐┬  ┬  ┌─┐┌┐┌┌─┐┌─┐
 ║║║ ║║  ║ ║└─┐  ║║║║    ║   ║ ╠╣   ║  ├─┤├─┤│  │  ├┤ ││││ ┬├┤ 
═╩╝╚═╝╩═╝╚═╝└─┘  ╩ ╩╩═╝  ╚═╝ ╩ ╚    ╚═╝┴ ┴┴ ┴┴─┘┴─┘└─┘┘└┘└─┘└─┘

Author: Alex Devassy
Access http://127.0.0.1:5012/
Category: Prompt Injection Attack
Description: Flag is at same directory as of flask app, [FLAG].txt.
Press Ctrl+C to quit
"""

print(__header__)

user_input = None

def remove_ansi_escape_codes(input_text):
    # Pattern to match ANSI escape codes
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    # Replace ANSI escape codes except newline characters
    cleaned_result = ansi_escape.sub('', input_text)
    return cleaned_result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    global user_input
    if request.form.get('message'):
        user_input = request.form.get('message')
        try:
            # Encode user input to Base64
            user_input_base64 = base64.b64encode(user_input.encode()).decode()

            # Log the request details
            app.logger.info(f"Sending request to Rebuff AI API with user_input_base64: {user_input_base64}")

            # Prepare the headers and payload
            headers = {
                'Authorization': f'Bearer {REBUFF_API_KEY}',  # Use the API key from command-line arguments
                'Content-Type': 'application/json'
            }
            payload = {
                'userInputBase64': user_input_base64,
                'runHeuristicCheck': True,
                'runVectorCheck': True,
                'runLanguageModelCheck': True,
                'maxHeuristicScore': 0.75,
                'maxModelScore': 0.9,
                'maxVectorScore': 0.9
            }

            # Log the headers and payload
            app.logger.info(f"Headers: {headers}")
            app.logger.info(f"Payload: {payload}")

            # Make the POST request
            response = requests.post(
                'https://www.rebuff.ai/api/detect',
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            result = response.json()

            if result.get('injectionDetected'):
                response_data = {'result': "Possible injection detected."}
            else:
                redirect_url = '/chat'
                response_data = {'response_result': "Verified", 'redirect_url': redirect_url}
        except requests.exceptions.HTTPError as http_err:
            app.logger.error(f"HTTP error occurred: {http_err}")
            response_data = {'result': "HTTP error occurred."}
        except Exception as err:
            app.logger.error(f"Other error occurred: {err}")
            response_data = {'result': "An error occurred."}
        return jsonify({'response': response_data})
    elif request.form.get('value'):
        value = request.form.get('value')
        try:
            command = f"python3 aiexecuter.py --user_input=\"{user_input}\" --api_key=\"{openaiapikey}\""
            # Run the subprocess
            rawresult = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            cleaned_result = remove_ansi_escape_codes(rawresult.stdout)
            result = cleaned_result
            if not rawresult.stdout:
                result = rawresult.stderr
        except Exception as e:
            app.logger.error(f"Subprocess error occurred: {e}")
            result = "An error occurred while executing the command."
        return jsonify({'response': result})

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Flask application")
    parser.add_argument('--rebuffkey', type=str, help='Rebuff API Key')
    parser.add_argument('--openaikey', type=str, help='OpenAI API Key')
    args = parser.parse_args()
    REBUFF_API_KEY = args.rebuffkey
    openaiapikey = args.openaikey
    if REBUFF_API_KEY is not None and openaiapikey is not None:
        rb = Rebuff(api_token=REBUFF_API_KEY, api_url="https://www.rebuff.ai")
        app.run(host="0.0.0.0", port=5012, debug=True)
    else:
        print("Please provide API Keys to proceed")