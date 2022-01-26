from PIL import Image
import face_recognition
import os


if not os.path.exists('Persons'):
    os.mkdir('Persons')

photos = os.listdir('photos')

for i, photo in enumerate(photos):
    image = face_recognition.load_image_file(f'fotos/{photo}')
    face_locations = face_recognition.face_locations(image)
    print(face_locations)

    print("I found {} face(s) in this photograph.".format(len(face_locations)))

    for j, face_location in enumerate(face_locations):
        top, right, bottom, left = face_location

        face_image = image[top:bottom, left:right]
        pil_image = Image.fromarray(face_image)
        pil_image.save(f'Persons/{i}_{j}.jpg')

