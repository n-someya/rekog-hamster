# -*- coding: utf-8 -*-
import cv2
import time
import numpy as np
import boto3
from datetime import datetime as dt
import slack_files

KABOSU_DIR="/mnt/share/kabosu/rekognition/"

def exists_hamster(labels):
    '''
    From amazon rekognition detect label response,
    Detect exisiting hamster
    @return confidencial
    '''
    for label in labels:
        if label['Name'] == 'Hamster':
            return label['Confidence']
    return 0

# OpenCVを利用してWebカメラからのキャプチャ準備
cap = cv2.VideoCapture(0)
# Webカメラから画像読み込み
ret, frame = cap.read()
# なぜか、画像が暗いので、明度を底上げ
frame = frame * 2.0

# Amazon ReKognitionのSDKクライアントを初期化
#   Note:
#     ~/..aws/credentials に以下のようなクレデンシャルを記載しておく
#      [default]
#      aws_access_key_id = 【アクセスキー】
#      aws_secret_access_key = 【アクセスシークレット】
#      region = 【リージョン名: us-west-2とか】
client = boto3.client('rekognition')
# awsに送信するためndarrayとなっている画像をpngのbytearrayに変換
ret, data = cv2.imencode('.png', frame)
byte_data = bytearray(data)
# Amazon rekognitionを呼び出し
response = client.detect_labels(
    Image={
        'Bytes': byte_data
    },
    MaxLabels=123
)
image_filename = KABOSU_DIR + 'hamster' + dt.now().strftime('%Y%m%d%H%M%S')
with open(image_filename + '.resplog', 'w') as respf:
    respf.write(str(response))

if exists_hamster(response['Labels']):
    image_filename += '_ok.jpg'
    cv2.imwrite(image_filename, frame)
    sfm = slack_files.SlackFileManager(channels="kabosu")
    sfm.upload_with_filename(image_filename)
else:
    image_filename += '_ng.jpg'
    cv2.imwrite(image_filename, frame)
