import io
import os
import json
from flask import Flask, render_template, request, redirect, jsonify
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

# Gets credentials
# May have to comment out to get to work locally
credentials_raw = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
service_account_info = json.loads(credentials_raw)
credentials = service_account.Credentials.from_service_account_info(service_account_info)

# Vision client
vision_client = vision.ImageAnnotatorClient(credentials=credentials)
# Translate client
translate_client = translate.Client(credentials=credentials)

@app.route('/')
def index():
	languages = translate_client.get_languages()
	return render_template("index.html", languages=languages)

@app.route('/image', methods=['POST'])
def vision_api():
	if request.method == 'POST':
		f = request.files['file']
		content = f.read()
		# Reads in image to object
		image = types.Image(content=content)
		# Performs object detection on the image
		objects = vision_client.object_localization(image=image)

		return MessageToJson(objects)
	return redirect("/")

@app.route('/language', methods=['POST'])
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
	return redirect("/")
if __name__ == '__main__':
	app.run()
