# -*- coding: utf-8 -*-
"""Практическая работа №4 Классификация и детекция объектов на изображении с использованием библиотеки ImageAI.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vsxGB_kUrhkD6AEW14u9ylBisB65WteH
"""

from google.colab import drive
drive.mount('/content/drive')

!pip install imageai # установка библиотеки ImageAI

"""# Добавляем в проект исходное изображение:"""

import numpy as np
import cv2
from google.colab.patches import cv2_imshow
from urllib.request import urlopen
req = urlopen('https://img.youscreen.ru/wall/14977257054998/14977257054998_1920x1200.jpg') # используя метод urlopen, получаем объект запроса по ссылке (изображение)
                                                                                      # и сохраняем его в виде потокового набора данных в переменную "req"

image_2 = np.asarray(bytearray(req.read()), dtype=np.uint8) # преобразуем потоковый набор данных в массив numpy
image_2 = cv2.imdecode(image_2, -1) # декодируем изображение в привычный для отображения формат

cv2_imshow(image_2) # Выводим изображение, используя метод cv2_imshow()

"""# Пример №1. Детекция

[Техническая документация](https://imageai.readthedocs.io/en/latest/detection/index.html)
"""

from imageai.Detection import ObjectDetection # Импортируем из библиотеки imageai класс ObjectDetection для поиска объектов
import os # Импортируем библиотеку os для взаимодействия с ОС

exec_path = os.getcwd()# Объявляем переменную exec_path и помещаем в неё функцию os.getcwd()для указания пути к данному проекту (для удобства работы с файлами, находящимися в корневой папке проекта)

detector = ObjectDetection() # создаем объект класса ObjectDetection
detector.setModelTypeAsRetinaNet() # обращаемся к методу setModelTypeAsRetinaNet, тем самым устанавливая для использования в проекте модель RetinaNet для распознавания объектов
detector.setModelPath("/content/drive/MyDrive/retinanet.pth") # указываем путь к модели (предварительно модель необходимо скачать с официального сайта ImageAI и поместить в корневую папку проекта)
detector.loadModel() # загружаем модель

list = detector.detectObjectsFromImage( # используем метод detectObjectsFromImage для обнаружения объектов на изображении
    input_image=image_2, # указываем путь к исходному изображению, либо имя переменной, которая уже содержит изображение
    output_image_path=os.path.join(exec_path, "new_objects.jpg"), # указываем имя и путь для сохранения распознанного изображения
    minimum_percentage_probability=60, # дополнительная характеристика, отвечающая за процент точности распознавания объекта. В данном случае, если точность объекта будет меньше, чем 60%, то в конечной выборке он присутствовать не будет
    display_percentage_probability=True, # отображение процента точности в конечном изображении
    display_object_name=True # отображение класса объекта в конечном изображении
)

print(list)
output_image = cv2.imread("/content/new_objects.jpg")
cv2_imshow(output_image)

"""# Пример №2. Классификация

[Техническая документация](https://imageai.readthedocs.io/en/latest/prediction/index.html)
"""

from imageai.Classification import ImageClassification
import os

execution_path = "/content/drive/MyDrive/resnet50.pth"

prediction = ImageClassification()
prediction.setModelTypeAsResNet50()
prediction.setModelPath("/content/drive/MyDrive/resnet50.pth")
prediction.loadModel()

predictions, probabilities = prediction.classifyImage((image_2), result_count=10)
for eachPrediction, eachProbability in zip(predictions, probabilities):
    print(eachPrediction , " : " , eachProbability)

"""# Задание №1. Детекция объектов на изображении

#### 1.1. Загрузка готовой модели для детекции объектов на изображении, отличной от той, что представлена в примере
"""

from imageai.Detection import ObjectDetection # Импортируем из библиотеки imageai класс ObjectDetection для поиска объектов
import os # Импортируем библиотеку os для взаимодействия с ОС

exec_path = os.getcwd()# Объявляем переменную exec_path и помещаем в неё функцию os.getcwd()для указания пути к данному проекту (для удобства работы с файлами, находящимися в корневой папке проекта)
detector = ObjectDetection() # создаем объект класса ObjectDetection
detector.setModelTypeAsYOLOv3() # обращаемся к методу setModelTypeAsYOLOv3, тем самым устанавливая для использования в проекте модель YOLOv3 для распознавания объектов
detector.setModelPath("/content/drive/MyDrive/yolov3.pt") # указываем путь к модели (предварительно модель необходимо скачать с официального сайта ImageAI и поместить в корневую папку проекта)
detector.loadModel()

"""#### 1.2. Используя данную модель, обработал 5 изображений с больши набором объектов, которые относятся к разным классам"""

import numpy as np
import cv2
from urllib.request import urlopen
urls = ['https://kartinkin.net/uploads/posts/2022-03/1647874931_44-kartinkin-net-p-tolpa-kartinki-60.jpg',
        'https://www.sbs.com.au/news/sites/sbs.com.au.news/files/Syd%20pedestrians%20-%20Getty.jpg',
        'https://www.sat7uk.org/wp-content/uploads/2021/07/Crowded-Istiklal-Avenue-Istanbul.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/7/74/Running_for_the_bus%2C_Spring_St%2C_Seattle_WA%2C_2009.jpg',
        'https://i.pinimg.com/originals/6d/06/ae/6d06ae9a9a9c561917cbe821997df39e.jpg']
exec_path = os.getcwd()
for i in range(len(urls)):
    req = urlopen(urls[i])
    image = np.asarray(bytearray(req.read()), dtype=np.uint8)
    image = cv2.imdecode(image, -1)
    list = detector.detectObjectsFromImage( # используем метод detectObjectsFromImage для обнаружения объектов на изображении
        input_image=image, # указываем путь к исходному изображению, либо имя переменной, которая уже содержит изображение
        output_image_path=os.path.join(exec_path, f"output{i}.jpg"), # указываем имя и путь для сохранения распознанного изображения
        minimum_percentage_probability=60, # дополнительная характеристика, отвечающая за процент точности распознавания объекта. В данном случае, если точность объекта будет меньше, чем 60%, то в конечной выборке он присутствовать не будет
        display_percentage_probability=True, # отображение процента точности в конечном изображении
        display_object_name=True # отображение класса объекта в конечном изображении
    )
    print(list)
    output_image = cv2.imread(f"/content/output{i}.jpg")
    cv2_imshow(output_image)

"""#### 1.4. Визуализируйте полученные результаты"""

import matplotlib.pyplot as plt
for image in os.listdir(exec_path):
    if (image.endswith(".jpg")):
        img = cv2.imread(os.path.join(exec_path, image))
        fig = plt.figure()
        plt.imshow(img)

"""# Задание №2. Классификация изображений

#### 2.1. Загрузка готовой модели для классификации изображений, отличной от той, что представлена в примере
"""

from imageai.Classification import ImageClassification
import os

prediction = ImageClassification()
prediction.setModelTypeAsInceptionV3()
prediction.setModelPath("/content/drive/MyDrive/inception.pth")
prediction.loadModel()

"""#### 2.2. Используя данную модель, обработал 5 изображений, которые относятся к разным классам и сохранил полученные предсказания используемой модели"""

import numpy as np
import cv2
from urllib.request import urlopen

urls = ['https://sc02.alicdn.com/kf/H1b52e2ed434f42be9223bcda1c3ddf88d/232031428/H1b52e2ed434f42be9223bcda1c3ddf88d.jpg',
        'https://i.pinimg.com/originals/06/bd/82/06bd82a32fd9a0ec6e5151dfadd7538a.jpg',
        'https://mobimg.b-cdn.net/v3/fetch/74/749a8e93ee92cfd039a1a0f2b25e3956.jpeg',
        'https://img4.goodfon.ru/original/2048x1365/6/7f/puma-malyshi-detenyshi.jpg',
        'https://64.media.tumblr.com/5fc9a38df4ffcb59ca160731863dbc2e/tumblr_onkh2lL42x1roirddo1_1280.jpg']

for i in range(len(urls)):
    req = urlopen(urls[i]) 
    image_2 = np.asarray(bytearray(req.read()), dtype=np.uint8) # преобразуем потоковый набор данных в массив numpy
    image_2 = cv2.imdecode(image_2, -1)
    predictions, probabilities = prediction.classifyImage((image_2), result_count=10)

    with open("output2.txt", "a") as file:
        file.write(f"{urls[i]}\n")

    for eachPrediction, eachProbability in zip(predictions, probabilities):
        with open("output2.txt", "a") as file:
            file.write(f"{eachPrediction} : {eachProbability}\n")
        #print(eachPrediction , " : " , eachProbability)

    with open("output2.txt", "a") as file:
        file.write("\n")

"""Результат задания №2 по классификацией изображения в Excel файле

# Задание №3. Детекция и трекинг объектов на видеопотоке

#### 3.1. Загрузил готовую модель для детекции объектов
"""

from imageai.Detection import VideoObjectDetection
import os
exec_path = os.getcwd()

detector = VideoObjectDetection()
detector.setModelTypeAsTinyYOLOv3()
detector.setModelPath(os.path.join(exec_path , "/content/drive/MyDrive/tiny-yolov3.pt"))
detector.loadModel()

"""#### 3.2. Используя данную модель, обрабатываю 5 видеофайлов, и сохраняю полученные видеофайлы

"""

exec_path_video = os.path.join(exec_path, '/content/drive/MyDrive/work 4/videos')

video_path = detector.detectObjectsFromVideo(
input_file_path=os.path.join(execution_path, "/content/drive/MyDrive/work 4/videos/video4.mp4"),
output_file_path=os.path.join(execution_path, "/content/drive/MyDrive/work 4/videos/video4_output"), 
frames_per_second=20, 
log_progress=True)

"""Можно посмотреть результаты  5 видеофайлов по данной ссылке: https://drive.google.com/drive/folders/1lcuISkHHbW2yj6jLH1jGA0Ytw-kzwpfw"""