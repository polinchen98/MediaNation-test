import glob
from PIL import Image
import face_recognition
import os
from collections import deque


class PersonImage:
    image = None
    encoding = None


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

persons = glob.glob('Persons/*.jpg')

person_images = deque()

for person in persons:
    image = face_recognition.load_image_file(person)
    person_image = PersonImage()
    person_image.image = image
    face_encoding = face_recognition.face_encodings(image)[0]
    person_image.encoding = face_encoding
    person_images.append(person_image)

groups = []

while person_images:
    current_person_image = person_images.pop()

    have_group = False

    for group in groups:
        group_person_image = group[0]

        distance = face_recognition.face_distance([group_person_image.encoding], current_person_image.encoding)[0]
        if distance <= 0.55:
            group.append(current_person_image)
            have_group = True

    if not have_group:
        groups.append([current_person_image])


for i, group in enumerate(groups):
    if not os.path.exists(f'Persons/group{i+1}'):
        os.mkdir(f'Persons/group{i+1}')

    for j, person in enumerate(group):
        person_image = person.image
        pil_image = Image.fromarray(person_image)
        pil_image.save(f'Persons/group{i+1}/{j}.jpg')

files = glob.glob('Persons/*.jpg')
for file in files:
    os.remove(file)
