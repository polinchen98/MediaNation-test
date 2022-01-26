from PIL import Image
import face_recognition
import os


if not os.path.exists('Persons'):
    os.mkdir('Persons')

photos = os.listdir('photos')

for i, photo in enumerate(photos):
    image = face_recognition.load_image_file(f'photos/{photo}')
    face_locations = face_recognition.face_locations(image)

    print("I found {} face(s) in this photograph.".format(len(face_locations)))

    for j, face_location in enumerate(face_locations):
        top, right, bottom, left = face_location

        face_image = image[top:bottom, left:right]
        pil_image = Image.fromarray(face_image)
        pil_image.save(f'Persons/{i}_{j}.jpg')

persons = os.listdir('Persons')

persons_encoding = []
for person in persons:
    image = face_recognition.load_image_file(f'Persons/{person}')
    face_encoding = face_recognition.face_encodings(image)[0]
    persons_encoding.append(face_encoding)

for person in persons:
    image = face_recognition.load_image_file(f'Persons/{person}')
    face_encoding = face_recognition.face_encodings(image)[0]
    distances = face_recognition.face_distance(persons_encoding, face_encoding)
    for distance in distances:
        if distance <= 0.6 and distance != 0:
            print('match!')

