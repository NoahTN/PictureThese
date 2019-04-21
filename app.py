from flask import Flask, render_template, request
from werkzeug import secure_filename

app = Flask(__name__)

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/image', methods = ['GET', 'POST'])
def visionAPI ():

	if request.method == 'POST':
		f = request.files['file']
		#sfname = 'static/images/'+str(secure_filename(f.filename))
		#f.save(sfname)
		content = f.read()
	

	# Run this in terminal first: export GOOGLE_APPLICATION_CREDENTIALS="C:\cygwin64\home\claud\dev\cst205\project\credentials.json"
	import io
	import os

	# Imports the Google Cloud client library
	from google.cloud import vision
	from google.cloud.vision import types

	# Instantiates a client
	client = vision.ImageAnnotatorClient()

	# The name of the image file to annotate
	#file_name = os.path.join(
	#    os.path.dirname(__file__), 'static/images/'+ str(f.filename))

	# Loads the image into memory
	#with io.open(file_name, 'rb') as image_file:
	#    content = image_file.read()
	
	image = types.Image(content=content)

	#These 2 lines allow to look at image from url
	#image = types.Image()
	#image.source.image_uri = image_link

	# Performs label detection on the image file
	response = client.label_detection(image=image)
	labels = response.label_annotations
	'''
	print('Labels:')
	for label in labels:
	    print(label.description)
	'''
	labelStr = ""
	for label in labels:
		labelStr += label.description

	#return render_template("index.html")
	return labelStr

if __name__=='__main__':
    app.run()