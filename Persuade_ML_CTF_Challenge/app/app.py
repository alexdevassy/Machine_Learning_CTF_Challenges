import torch
import sys
import os
from flask import Flask, request, render_template, flash, redirect, url_for, send_from_directory, send_file
from werkzeug.utils import secure_filename
from transformers import AutoTokenizer
from scipy.special import softmax
import urllib.request
import csv
import numpy as np

import logging
log = logging.getLogger('werkzeug')
log.disabled = True

#cli = sys.modules['flask.cli']
#cli.show_server_banner = lambda *x: None

__header__ = """
Running...

╔═╗┌─┐┬─┐┌─┐┬ ┬┌─┐┌┬┐┌─┐  ╔╦╗╦    ╔═╗╔╦╗╔═╗  ╔═╗┬ ┬┌─┐┬  ┬  ┌─┐┌┐┌┌─┐┌─┐  
╠═╝├┤ ├┬┘└─┐│ │├─┤ ││├┤   ║║║║    ║   ║ ╠╣   ║  ├─┤├─┤│  │  ├┤ ││││ ┬├┤   
╩  └─┘┴└─└─┘└─┘┴ ┴─┴┘└─┘  ╩ ╩╩═╝  ╚═╝ ╩ ╚    ╚═╝┴ ┴┴ ┴┴─┘┴─┘└─┘┘└┘└─┘└─┘ 

Author: Alex Devassy
Access http://127.0.0.1:5000 
Category : Machine Leanrning Model Serialization Attacks 
Description : Flag is at /home/Flag.txt, not on the website. Find it.
Press Ctrl+C to quit
"""
#Access http://127.0.0.1:5000 
#Press Ctrl+C to quit 
print(__header__)
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Configure upload folder and allowed file extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Preprocess text (username and link placeholders)
def preprocess(text):
    new_text = []
    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)
    
def predict_sentiment(user_input: str, model):
    #model = torch.load(file_path)
    task = "sentiment"
    MODEL = f"cardiffnlp/twitter-roberta-base-sentiment"
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    text = preprocess(user_input)
    encoded_input = tokenizer(text, return_tensors='pt')
    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    # download label mapping
    labels=[]
    mapping_link = f"https://raw.githubusercontent.com/cardiffnlp/tweeteval/main/datasets/{task}/mapping.txt"
    with urllib.request.urlopen(mapping_link) as f:
        html = f.read().decode('utf-8').split("\n")
        csvreader = csv.reader(html, delimiter='\t')
    labels = [row[1] for row in csvreader if len(row) > 1]
    ranking = np.argsort(scores)
    ranking = ranking[::-1]
    return (f"The overall sentiment is: {labels[ranking[0]]} with a score of: {np.round(float(scores[ranking[0]])*100, 1)}%")

# Function to check if a filename has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    uploaded_files = os.listdir(app.config['UPLOAD_FOLDER'])
    if request.method == 'POST':
        # Handle file upload
        if 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
                file.save(filename)
                flash('File uploaded successfully')
                uploaded_files.append(secure_filename(file.filename))
            else:
                flash('File format not allowed')
    return render_template('upload.html', uploaded_files=uploaded_files)

@app.route('/analyze', methods=['POST'])
def analyze_input():
    # Handle user input and analysis
    selected_file = request.form.get('model_file')
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads", selected_file)
    user_input = request.form.get('user_input')
    if selected_file and user_input:
        flash(f'Selected file: {selected_file}')
        # Perform your analysis here using the selected_file and user_input   
        sentiment = predict_sentiment(user_input, torch.load(file_path))
        flash(sentiment)
    return render_template('upload.html')

@app.route('/robots.txt', methods=['GET'])
def render_robots():
    return send_file('robots.txt')
    
@app.route('/backend_docs/myfile.txt', methods=['GET'])
def render_file():
    return send_file('backend_docs/myfile.txt')
    
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    #app.secret_key = 'supersecretkey'
    app.run(host="0.0.0.0", port=5000)
