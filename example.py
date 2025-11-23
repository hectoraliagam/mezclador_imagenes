# example.py

import random
from datetime import datetime

imagenes = ['img1.jpg', 'img2.jpg', 'img3.jpg', 'img4.jpg', 'img5.jpg']

random.seed(42)
print(random.sample(imagenes, 3))

random.seed(99)
print(random.sample(imagenes, 3))

semilla = datetime.now().timestamp()
random.seed(semilla)
print(random.sample(imagenes, 3))
