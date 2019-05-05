'''
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
'''
	print('Labels:')
	for label in labels:
	    print(label.description)
'''
'''
	labelStr = ""
	for label in labels:
		labelStr += label.description

	#return render_template("index.html")
	return labelStr

if __name__=='__main__':
    app.run()
'''
import io
import os
import json
from flask import Flask, render_template, request, redirect, jsonify, send_file
from werkzeug import secure_filename
from google.oauth2 import service_account
from google.cloud import vision
from google.cloud.vision import types

from PIL import Image, ImageDraw
import cv2
import numpy as np

app = Flask(__name__)

#os.makedirs(os.path.join(app.instance_path, 'htmlfi'), exist_ok=True)

# Instantiates a vision client
# May have to comment out to get to work locally
#credentials_raw = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
#service_account_info = json.loads(credentials_raw)
#credentials = service_account.Credentials.from_service_account_info(service_account_info)
vision_client = vision.ImageAnnotatorClient()
# Run this in terminal first: export GOOGLE_APPLICATION_CREDENTIALS="C:\cygwin64\home\claud\dev\cst205\project\credentials.json"

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
		#response = client.label_detection(image=image)
		#labels = response.label_annotations
		# TO IMPLEMENT: return proper json object with keys and values
		#labelStr = ""
		#for label in labels:
		#	labelStr += label.description
		#return jsonify(detected=labelStr)

		objects = vision_client.object_localization(image=image).localized_object_annotations

		#Opens image in pillow
		im = Image.open(f)
		#im.load()
		draw = ImageDraw.Draw(im)

		#Gets Object Coordinates
		bounds = []
		for object_ in objects:
			for vertex in object_.bounding_poly.normalized_vertices:
				#print(' - ({}, {})'.format(vertex.x, vertex.y))
				bounds.append((vertex.x * im.width, vertex.y * im.height))
		
		#Uses coordinates to draw on the image
		for i in range(0, len(bounds), 4):
			draw.rectangle([(bounds[i][0], bounds[i][1]), (bounds[i+2][0], bounds[i+2][1])], fill=None, outline="blue")
		
		del draw
		
		#im.save("test.png")

		#cvIm = np.asarray(im)
		#cv2.imwrite(f, cvIm)

		#f.save(os.path.join(app.instance_path, 'htmlfi', secure_filename(f.filename)))

		'''
		output = io.BytesIO()
		im.convert('RGBA').save(output, format='PNG')
		output.seek(0, 0)

		img = base64.b64encode(im.getvalue())
		
		return send_file(output, mimetype='image/png', as_attachment=False)'''

		#im.show()

		#Converts the image to bytes and sends it to html
		img_io = io.BytesIO()
		im.save(img_io, 'PNG', quality=70)
		img_io.seek(0)
		return send_file(img_io, mimetype='image/png')

		#return render_template('index.html', img=img.decode('ascii'))

		#return MessageToJson(objects)
		#return render_template('index.html')

	return redirect("/")

if __name__=='__main__':
    app.run()