import io
from base64 import b64encode
from PIL import Image, ImageDraw
from flask import Flask, send_file

class RectangleDraw:
    '''Used to draw bounding rectangles using coordinates from the Google Vision API'''
    def draw_rectangles(self, file, objects):
        image = Image.open(file)
        draw = ImageDraw.Draw(image)
        bounds = []

        # Get rectangle coordinate for each detected object
        for _object in objects:
            for vertex in _object.bounding_poly.normalized_vertices:
                bounds.append((vertex.x * image.width, vertex.y * image.height))
        # Use coordinates to draw on image
        for i in range(0, len(bounds), 4):
            draw.rectangle([(bounds[i][0], bounds[i][1]), (bounds[i+2][0], bounds[i+2][1])], fill=None, outline="blue")
        # Free up memory
        del draw

        # Converts the image to bytes and returns it
        result = io.BytesIO()
        image.save(result, 'JPEG', quality=90)
        result.seek(0, 0)

        return b64encode(result.getvalue())