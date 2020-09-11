import os, io
from google.cloud import vision
from google.cloud.vision import types
import time
from PIL import Image, ImageDraw, ImageFont


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'api_vision_key.json'
client=vision.ImageAnnotatorClient()

def localize_objects(path):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """
    
    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content) # pylint: disable=no-member

    objects = client.object_localization(image=image).localized_object_annotations # pylint: disable=no-member
    print("OBJECTS",objects)
    print('Number of objects found: {}'.format(len(objects)))
    
    image = Image.open('images/living2.jpg')
    dibujar = ImageDraw.Draw(image)
    for object_ in objects:
        print('\n{} (confidence: {})'.format(object_.name, object_.score))
        print('Normalized bounding polygon vertices: ')
        for vertex in object_.bounding_poly.normalized_vertices:
            print(' - ({}, {})'.format(vertex.x, vertex.y))

        ancho, alto = image.size
        dibujar.polygon([object_.bounding_poly.normalized_vertices[0].x * ancho,
                         object_.bounding_poly.normalized_vertices[0].y * alto,
                         object_.bounding_poly.normalized_vertices[1].x * ancho,
                         object_.bounding_poly.normalized_vertices[1].y * alto,
                         object_.bounding_poly.normalized_vertices[2].x * ancho,
                         object_.bounding_poly.normalized_vertices[2].y * alto,
                         object_.bounding_poly.normalized_vertices[3].x * ancho,
                         object_.bounding_poly.normalized_vertices[3].y * alto])
        dibujar.text((object_.bounding_poly.normalized_vertices[0].x * ancho, object_.bounding_poly.normalized_vertices[0].y* alto - 10),object_.name, fill="Black")
    image.show()

localize_objects('images/living2.jpg')