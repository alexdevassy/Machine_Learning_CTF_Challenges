from flask import Flask, render_template, redirect, url_for, request, jsonify
from rebuff import RebuffSdk
import subprocess
import re
import argparse
import base64
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
Access http://127.0.0.1:5000/
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
            # Log the request details
            app.logger.info(f"Sending request to Rebuff SDK with user_input: {user_input}")

            # Using the correct method `detect_injection` from RebuffSdk
            result = rb.detect_injection(user_input)

            if result.injection_detected:
                response_data = {'result': "Possible injection detected."}
            else:
                redirect_url = '/chat'
                response_data = {'response_result': "Verified", 'redirect_url': redirect_url}
        except Exception as err:
            app.logger.error(f"Error occurred: {err}")
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
    parser.add_argument('--pineconekey', type=str, help='Pinecone API Key')
    parser.add_argument('--pineconeenv', type=str, help='Pinecone Environment', default="Default")  # Default value
    parser.add_argument('--pineconeindex', type=str, help='Pinecone Index')
    args = parser.parse_args()

    # Initialize the Rebuff SDK with the correct parameters
    rb = RebuffSdk(
        args.openaikey,
        args.pineconekey,
        args.pineconeenv,  # This will now use 'Default' if no value is provided
        args.pineconeindex
    )
    
    app.run(host="0.0.0.0", port=5000, debug=True)