import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl
import sys
import cgi
import base64
import numpy as np
from skimage import io
from io import BytesIO
import requests
import keras
import imghdr

model = keras.models.load_model('./model.h5')
print("Welcome to .....\n")
print("""\
█▀▀ █▀█ █░█ █▀█ ▀█▀ █░█ █▄░█ █▀▀   █▀▄▀█ █░░   █▀▀ ▀█▀ █▀▀   █▀▀ █░█ ▄▀█ █░░ █░░ █▀▀ █▄░█ █▀▀ █▀▀
█▀░ █▄█ █▄█ █▀▄ ░█░ █▄█ █░▀█ ██▄   █░▀░█ █▄▄   █▄▄ ░█░ █▀░   █▄▄ █▀█ █▀█ █▄▄ █▄▄ ██▄ █░▀█ █▄█ ██▄
 """)
print("Created by: Alex Neelankavil Devassy")
print("Access http://127.0.0.1 in host systems's browser")
print("Press Ctrl+C to quit")
with open("templates/AICorp.html","rb") as file:
    STATIC_HTML_PAGE = file.read()

#simple web server
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        forwardedfor = str(self.headers['X-Forwarded-For'])
        print(f"GET {forwardedfor}")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(STATIC_HTML_PAGE)

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        if int(content_length) > 10000000:
            print("File too big")
            self.send_response(500, "File too big")
            return

        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={"REQUEST_METHOD":"POST",
                     "CONTENT_TYPE":self.headers["Content-Type"],
                     })

        filename = str(form['file'].filename)
        forwardedfor = str(self.headers['X-Forwarded-For'])
        print(f"POST {forwardedfor} File: {filename} - ", end = ".")
        data = form["file"].file.read()

        print("Checking image", end = ". ")
        #print(data)
        filetype = imghdr.what(file="", h=data)
        print(filetype)
        if filetype not in ["png","jpeg","gif"]:
             print(f"Unsupported media type:  {filetype}", end = ". ")
             self.send_response(415, "Only png, jpg and gif are supported.")
             return
        image = io.imread(BytesIO(data))
        processedImage = np.zeros([1, 28, 28, 1])
        for yy in range(28):
            for xx in range(28):
                processedImage[0][xx][yy][0] = float(image[xx][yy]) / 255

        shownDigit = np.argmax(model.predict(processedImage))

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        if shownDigit == 4:
            response = '{ "text": " Welcome Mr. ' + str(shownDigit) +'tune {++BackPropogation Magic++}"}'
        else:
            response = '{ "text": "Access Denied"}'
        sys.stdout.flush()
        self.wfile.write(bytes(response,"utf-8"))
httpd = HTTPServer(("", 8080), SimpleHTTPRequestHandler)
httpd.serve_forever()
