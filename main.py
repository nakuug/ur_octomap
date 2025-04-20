from ultralytics import YOLO
import numpy as np
import time

# Load a pretrained YOLO11n model
model = YOLO("yolov8n.pt",verbose=True)
# path = pre_model.export(format="engine")
# model = path

# Train the model on the COCO8 dataset for 100 epochs

# Perform object detection on an image
#results = model("https://www.youtube.com/watch?v=uWBv-8c1_3U&pp=ygUS5Lq66YCa44KK44CA5YuV55S7", stream=False)  # Predict on an image
#for r in results:
#    print(r.speed)
# results[0].show()  # Display results

# Export the model to ONNX format for deployment
#path = model.export(format="onnx")  # Returns the path to the exported model

import cv2

#image = None
#FILEPATH = "./sample.jpg" # 動画ファイルの相対パス
#img = cv2.imread(FILEPATH)
#results = model(image, stream=False)

FILEPATH = "./sample.mp4" # 動画ファイルの相対パス

# # 動画ファイルを読み込む
video = cv2.VideoCapture(FILEPATH)

# 動画情報の取得
frameAll = int(video.get(cv2.CAP_PROP_FRAME_COUNT)) # 動画の総フレームを取得
framerate = int(video.get(cv2.CAP_PROP_FPS)) # 動画フレームレートを取得(当サンプルでは[60]を返す)

# ファイル出力用のインデックス初期化
idx = 0

# 動画1秒単位でのループ処理(※1)
pretime = 10
for i in range(0, frameAll, framerate):
    nowtime = time.time()
    fps = 1 / (nowtime - pretime)
    pretime = nowtime
    # print("fps" + str(fps))


    # 動画指定秒数での動画読み込み
    video.set(cv2.CAP_PROP_POS_FRAMES, i)
    ret, image = video.read() # [ret]はread()の処理結果、[image]は処理画像が格納される

    # read()が正常終了した場合に画像ファイル出力を実行
    if ret == True:
        befor = time.time()
        results = model(image,stream=False)  # Predict on an image
        # print("predicttime:" + str(time.time()-befor))
        # print(dir(results[0]))
        # cv2.imshow("result", np.ndarray(results[0].orig_img))
        # # 画像ファイルとして保存(※2)
        # cv2.imwrite('{}{}{}'.format('./ret/image_', idx, '.jpg'), image[390:590, 590:1320]) 

        # # ファイル出力用のインデックスをインクリメント
        # idx += 1
    else:
        break
