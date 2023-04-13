import cv2
from matplotlib import pyplot as plt

bgr = cv2.imread("./images/test.jpg")

rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

f = plt.figure()

f.add_subplot(1, 2, 1)
plt.xticks([])
plt.yticks([])
plt.imshow(rgb)

f.add_subplot(1, 2, 2)
plt.xticks([])
plt.yticks([])
plt.imshow(gray)

plt.show(block=True)
