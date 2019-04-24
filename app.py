import io
import os
import json
from flask import Flask, render_template, request
from werkzeug import secure_filename
from google.oauth2 import service_account
from google.cloud import vision
from google.cloud.vision import types

app = Flask(__name__)

# Instantiates a vision client
# May have to comment out to get to work locally
credentials_raw = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
service_account_info = json.loads(credentials_raw)
credentials = service_account.Credentials.from_service_account_info(service_account_info)
client = vision.ImageAnnotatorClient(credentials=credentials)

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/image', methods = ['POST'])
def visionAPI ():

	if request.method == 'POST':
		f = request.files['file']
		content = f.read()

	# Reads in image to object
	image = types.Image(content=content)

	# Performs label detection on the image object
	response = client.label_detection(image=image)
	labels = response.label_annotations

	labelStr = ""
	for label in labels:
		labelStr += label.description

	#return render_template("index.html")
	return labelStr

if __name__=='__main__':
    app.run()