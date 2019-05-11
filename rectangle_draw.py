import io
from base64 import b64encode
from PIL import Image, ImageDraw, ImageFont
from flask import Flask, send_file

class RectangleDraw:

    # Checks both object's top left coordinates to see if they are the same object
    def check_if_same_object(self, _object, compare_object):
        top_left_x = False
        top_left_y = False

        if _object.bounding_poly.normalized_vertices[0].x == compare_object.bounding_poly.normalized_vertices[0].x:
            top_left_x = True
        if _object.bounding_poly.normalized_vertices[0].y == compare_object.bounding_poly.normalized_vertices[0].y:
            top_left_y = True

        if top_left_x == True and top_left_y == True:
            return True
        else:
            return False

    '''Used to draw bounding rectangles using coordinates from the Google Vision API'''
    def draw_rectangles(self, file, objects):
        image = Image.open(file)
        draw = ImageDraw.Draw(image)
        bounds = []
        names = []

        # Sets up font of text drawn on the image and sets the fontsize based off image width
        fnt = ImageFont.truetype('static/fonts/boringboron.ttf', int(image.width * 0.04))

        # Get rectangle coordinate for each detected object
        for _object in objects:
            for vertex in _object.bounding_poly.normalized_vertices:
                bounds.append((vertex.x * image.width, vertex.y * image.height))

            # Adds name to list if list is empty
            if len(names) == 0:
                names.append(_object.name)
            else: # If the API recongizes the same thing as two different objects, it puts their names together
                object_count = 0
                object_found = False
                for compare_object in objects:
                    # Checks if current object is at the same location as any other objects
                    if RectangleDraw().check_if_same_object(_object, compare_object):
                        # Makes sure that the found equal object has already been added to the names list and it's not the same exact object
                        if object_count < len(names) and _object.name != compare_object.name:
                            n_count = 0
                            # Looks for the correct position of the object's name in the names list
                            for name in names:
                                if compare_object.name in name:
                                    name += "/" + _object.name
                                    names[n_count] = name
                                    break

                                n_count += 1
                        object_found = True

                    object_count += 1

                    # Adds the object name if no equal object was found
                    if object_found == False:
                        names.append(_object.name)

        # Use coordinates to draw on image
        name_count = 0
        for i in range(0, len(bounds), 4):
            draw.rectangle([(bounds[i][0], bounds[i][1]), (bounds[i+2][0], bounds[i+2][1])], fill=None, outline="blue")
            if name_count < len(names):
                draw.text((bounds[i][0] + 2, bounds[i][1] - 1), names[name_count], font=fnt, fill=(10,10,10,255))
            name_count += 1
        # Free up memory
        del draw

        # Converts the image to bytes and returns it
        result = io.BytesIO()
        image.save(result, 'PNG', quality=80)
        image.close()
        result.seek(0, 0)
        
        return b64encode(result.getvalue())