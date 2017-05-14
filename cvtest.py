import cv2
import time
import numpy as np
import boto3

def exists_hamster(labels):
    for label in labels:
        if label['Name'] == 'Hamster':
            return label['Confidence']
    return 0


def adjust_gamma(image, gamma=1.0):
    table = np.array([
        ((i / 255.0) ** (1.0 / gamma) ) * 255 for i in np.arange(0, 256)
        ]).astype("uint8")
    return cv2.LUT(image, table)

def adjust_hsv(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    hsv[:, :, 1] = hsv[:, :, 1] * 1.5
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)


cap = cv2.VideoCapture(0)

ret, frame = cap.read()
frame = frame * 2.5

client = boto3.client('rekognition')

ret, data = cv2.imencode('.png', frame)
byte_data = bytearray(data)

response = client.detect_labels(
    Image={
        'Bytes': byte_data
    },
    MaxLabels=123
)
print(response)
if exists_hamster(response['Labels']):
    print("kabo!")

cv2.imwrite('test.jpg', frame)
exit(0)
