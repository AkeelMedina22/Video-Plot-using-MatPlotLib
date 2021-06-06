import cv2
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig = plt.figure()

frames = []

# Change the video name here:
cap = cv2.VideoCapture('input.mp4')
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        frames.append(frame)
    else:
        break
cap.release()
cv2.destroyAllWindows()

line = plt.scatter([0], [0], s=0.1, c='black')


def animate(i):
    im = frames[i]
    gray_img = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    
    # For black background videos, lower the threshold near 75.
    # For white background videos, increase to max 255, near 200
    _, img = cv2.threshold(gray_img, 150, 150, cv2.THRESH_BINARY_INV)
    img = cv2.medianBlur(img, 1)

    contours, hierarchy = cv2.findContours(
        img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    hierarchy = hierarchy[0]

    lst = []
    for component in zip(contours, hierarchy):
        currentContour = component[0].tolist()
        currentHierarchy = component[1].tolist()
        # Un-Comment this line if the borders are being detected
        #if currentHierarchy[0] >= 5:
        for i in currentContour:
            for j in i:
                lst.append(j)
    arrx = [i[0] for i in lst]
    arry = [-i[1] for i in lst]
    arr = [(x, y) for x, y in zip(arrx, arry)]

    line.set_offsets(arr)


plt.ylim(-720, 0)
plt.xlim(0, 1280)

anim = FuncAnimation(fig, animate,
                     frames=len(frames), interval=0.1, blit=False)

# Change the output name here:
anim.save('output.gif')
