import os
import random
from flask import Flask, render_template, redirect, url_for, request, jsonify, make_response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import logging
log = logging.getLogger('werkzeug')
log.disabled = True

app = Flask(__name__, static_folder='images')
app.secret_key = 'your_secret_key'

# Initialize Flask-Limiter with the Flask app
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["5 per minute"]  # Set a default rate limit for all routes if needed
)

__header__ = """
Running...

╦  ╦┌─┐┬ ┬┬ ┌┬┐  ╔╦╗╦    ╔═╗╔╦╗╔═╗  ╔═╗┬ ┬┌─┐┬  ┬  ┌─┐┌┐┌┌─┐┌─┐
╚╗╔╝├─┤│ ││  │   ║║║║    ║   ║ ╠╣   ║  ├─┤├─┤│  │  ├┤ ││││ ┬├┤ 
 ╚╝ ┴ ┴└─┘┴─┘┴   ╩ ╩╩═╝  ╚═╝ ╩ ╚    ╚═╝┴ ┴┴ ┴┴─┘┴─┘└─┘┘└┘└─┘└─┘

Author: Alex Devassy
Access http://127.0.0.1:49156/
Category: Model Inversion Attack
Description: Gain access to Vault and fetch Secret (Flag:). 
Press Ctrl+C to quit
"""

print(__header__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/submit', methods=['POST'])
@limiter.limit("3 per minute")
def handle_submit():
    try:
        # Get JSON data from the POST request
        data = request.json

        # Extract selected images from the received data
        dropdown1_image = data.get('dropdown1')
        dropdown2_image = data.get('dropdown2')
        dropdown3_image = data.get('dropdown3')
        dropdown4_image = data.get('dropdown4')
        #print(f"{dropdown1_image}, {dropdown2_image}, {dropdown3_image}, {dropdown4_image}")
        #if dropdown1_image == "12.PNG" and dropdown2_image == "1.PNG" and dropdown3_image =="34.PNG" and dropdown4_image == "23.PNG":
        if dropdown1_image == "Jeff" and dropdown2_image == "Robert" and dropdown3_image =="Frank" and dropdown4_image == "Joshua":
            print("Access Granted")
            #return jsonify({'message': 'Access Granted', 'status': 'success'})
            response = make_response(jsonify({'message': 'Access Granted', 'status': 'success', 'secret':'Flag:M0d3l1nv3rsi0n'}))
            response.headers['X-Tensorflow-Header'] = '2.12.0'
            return response
        else:
            print("No Access")
            #return jsonify({'message': 'Access Denied', 'status': 'success'})
            response = make_response(jsonify({'message': 'Access Denied', 'status': 'failure', 'secret':''}))
            response.headers['X-Tensorflow-Header'] = '2.12.0'
            return response

    except Exception as e:
        print(f'An error occurred: {e}')
        # Return a JSON response indicating an error
        return jsonify({'message': 'An error occurred', 'status': 'error'}), 500

# Rate limit error handler
@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({'message': 'Too many requests, please try again later.', 'status': 'error'}), 429

if __name__ == '__main__':
    
    app.run(host="0.0.0.0", port=49155)
    app.run(debug=True)
    
