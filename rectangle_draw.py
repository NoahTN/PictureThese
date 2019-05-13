import io
from base64 import b64encode
from PIL import Image, ImageDraw, ImageFont
from flask import Flask, send_file
import sys


class RectangleDraw:
    '''Used to draw bounding rectangles using coordinates from the Google Vision API'''
    def draw_rectangles(self, file, objects):
        image = Image.open(file)
        # resize image for consistency
        if image.width < 1200:
            image = image.resize((1200, int(image.height * 1200 / image.width)), Image.BILINEAR)
        draw = ImageDraw.Draw(image)
        bounds = []
        names = {}

        # Sets up font of text drawn on the image and sets the fontsize based off image width
        fnt = ImageFont.truetype('static/fonts/boringboron.ttf', int(image.width * 0.045))

        # Get rectangle coordinate for each detected object
        for _object in objects:
            for vertex in _object.bounding_poly.normalized_vertices:
                bounds.append((round(vertex.x * image.width), round(vertex.y * image.height)))
        # Combine names with overlapping corners
        for _object in objects:
            top_left_vertex = (round(_object.bounding_poly.normalized_vertices[0].x * image.width), round(_object.bounding_poly.normalized_vertices[0].y * image.height))
            # if already exists and not a duplicate name
            if top_left_vertex in names:
                if names[top_left_vertex] != _object.name:
                    names[top_left_vertex] += "/" + _object.name
            else:
                names[top_left_vertex] = _object.name

        for i in range(0, len(bounds), 4):
            # draw rectangle thrice for thickness
            draw.rectangle([(bounds[i][0], bounds[i][1]), (bounds[i+2][0], bounds[i+2][1])], fill=None, outline="#6879D3")
            draw.rectangle([(bounds[i][0]-1, bounds[i][1]+1), (bounds[i+2][0]+1, bounds[i+2][1]+1)], fill=None, outline="#6879D3")
            draw.rectangle([(bounds[i][0]-2, bounds[i][1]+2), (bounds[i+2][0]+2, bounds[i+2][1]+2)], fill=None, outline="#6879D3")
            # draw text
            top_left_vertex = (bounds[i][0], bounds[i][1])
            # shadow
            draw.text((bounds[i][0] + 1, bounds[i][1] - 1), names[top_left_vertex], font=fnt, fill="white")
            draw.text((bounds[i][0] + 3, bounds[i][1] - 1), names[top_left_vertex], font=fnt, fill="white")
            draw.text((bounds[i][0] + 2, bounds[i][1] - 2), names[top_left_vertex], font=fnt, fill="white")
            draw.text((bounds[i][0] + 2, bounds[i][1]), names[top_left_vertex], font=fnt, fill="white")
            draw.text((bounds[i][0] + 1, bounds[i][1] - 2), names[top_left_vertex], font=fnt, fill="white")
            draw.text((bounds[i][0] + 3, bounds[i][1] - 2), names[top_left_vertex], font=fnt, fill="white")
            draw.text((bounds[i][0] + 1, bounds[i][1]), names[top_left_vertex], font=fnt, fill="white")
            draw.text((bounds[i][0] + 3, bounds[i][1]), names[top_left_vertex], font=fnt, fill="white")
            # actual text
            draw.text((bounds[i][0] + 2, bounds[i][1] - 1), names[top_left_vertex], font=fnt, fill="#6879D3")
           
        # Free up memory
        del draw

        # Converts the image to bytes and returns it
        result = io.BytesIO()
        image.save(result, 'PNG', quality=80)
        image.close()
        result.seek(0, 0)
        
        return b64encode(result.getvalue())