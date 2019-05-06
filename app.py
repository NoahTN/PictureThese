import io
import os
import json
from rectangle_draw import RectangleDraw
from flask import Flask, render_template, request, redirect, jsonify, url_for, make_response
from werkzeug import secure_filename
from google.oauth2 import service_account
from google.cloud import vision
from google.cloud.vision import types
from google.cloud import translate
from google.protobuf.json_format import MessageToJson

# Pycharm local env
# from pathlib import Path
# from dotenv import load_dotenv
# load_dotenv()
# env_path = Path('.') / '.env'
# load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
objects_annotations = []

# Gets credentials
# May have to comment out to get to work locally
credentials_raw = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
service_account_info = json.loads(credentials_raw)
credentials = service_account.Credentials.from_service_account_info(service_account_info)

# Vision client
vision_client = vision.ImageAnnotatorClient(credentials=credentials)
# Translate client
translate_client = translate.Client(credentials=credentials)
languages = translate_client.get_languages()

@app.route('/')
def index():
	return render_template("index.html", languages=languages)

@app.route('/image', methods=['GET', 'POST'])
def vision_api():
	global objects_annotations
	if request.method == 'POST':
		file = request.files['file']
		content = file.read()
		# Reads in image to object
		image = types.Image(content=content)
		# Performs object detection on the image
		objects = vision_client.object_localization(image=image)
		objects_annotations = objects.localized_object_annotations
		return MessageToJson(objects)
	return redirect(url_for("index"))

@app.route('/rectangles', methods=['GET', 'POST'])
def draw_rect():
	global objects_annotations
	if request.method == 'POST':
		file = request.files['file']
		rect_draw = RectangleDraw()
		return rect_draw.draw_rectangles(file, objects_annotations)
	return redirect(url_for("index"))

@app.route('/language', methods=['GET', 'POST'])
def translate_api():
	if request.method == 'POST':
		data = request.get_json()
		language = data["language"]
		ld = data["words"]
		translated_words = list()

		for l in ld:
			translated_words.append(translate_client.translate(l["name"], target_language=language, source_language="en"))

		data["translated"] = translated_words

		return jsonify(status="success", data=data)
	return redirect(url_for("index"))
if __name__ == '__main__':
	app.run()
