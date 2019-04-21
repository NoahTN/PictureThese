# Run this in terminal first: export GOOGLE_APPLICATION_CREDENTIALS="C:\cygwin64\home\claud\dev\cst205\project\credentials.json"

import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
'''
file_name = os.path.join(
    os.path.dirname(__file__),
    'scoobydoo.png')

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()
'''

#image = types.Image(content=content)

#These 2 lines allow to look at image from url
image = types.Image()
image.source.image_uri = "blob:https://image-translator.herokuapp.com/7860c885-035e-4e29-8d90-8f7281e6752a"

# Performs label detection on the image file
response = client.label_detection(image=image)
labels = response.label_annotations

print('Labels:')
for label in labels:
    print(label.description)


'''
# https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/vision/cloud-client/web/web_detect.py

import argparse
import io

from google.cloud import vision
from google.cloud.vision import types
# [END vision_web_detection_tutorial_imports]


def annotate(path):
    """Returns web annotations given the path to an image."""
    # [START vision_web_detection_tutorial_annotate]
    client = vision.ImageAnnotatorClient()

    if path.startswith('http') or path.startswith('gs:'):
        image = types.Image()
        image.source.image_uri = path

    else:
        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = types.Image(content=content)

    web_detection = client.web_detection(image=image).web_detection
    # [END vision_web_detection_tutorial_annotate]

    return web_detection


def report(annotations):
    """Prints detected features in the provided web annotations."""
    # [START vision_web_detection_tutorial_print_annotations]
    if annotations.pages_with_matching_images:
        print('\n{} Pages with matching images retrieved'.format(
            len(annotations.pages_with_matching_images)))

        for page in annotations.pages_with_matching_images:
            print('Url   : {}'.format(page.url))

    if annotations.full_matching_images:
        print('\n{} Full Matches found: '.format(
              len(annotations.full_matching_images)))

        for image in annotations.full_matching_images:
            print('Url  : {}'.format(image.url))

    if annotations.partial_matching_images:
        print('\n{} Partial Matches found: '.format(
              len(annotations.partial_matching_images)))

        for image in annotations.partial_matching_images:
            print('Url  : {}'.format(image.url))

    if annotations.web_entities:
        print('\n{} Web entities found: '.format(
              len(annotations.web_entities)))

        for entity in annotations.web_entities:
            print('Score      : {}'.format(entity.score))
            print('Description: {}'.format(entity.description))
    # [END vision_web_detection_tutorial_print_annotations]


if __name__ == '__main__':
    # [START vision_web_detection_tutorial_run_application]
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    path_help = str('The image to detect, can be web URI, '
                    'Google Cloud Storage, or path to local file.')
    parser.add_argument('image_url', help=path_help)
    args = parser.parse_args()

    report(annotate(args.image_url))
'''