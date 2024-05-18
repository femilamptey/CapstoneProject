from ultralytics import YOLO
import cv2
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image
from torchvision import datasets, transforms
from torch.autograd import Variable
import torch
from torch import Tensor
import utils

model = YOLO("best.pt")
model.to("mps")

src = "/Users/femilamptey/PycharmProjects/dojotest/training/2023-10-12 13-59-01.mp4"
img_size=384

cmap = plt.get_cmap('tab20b')
colors = [cmap(i)[:3] for i in np.linspace(0, 1, 20)]

videoPath = '/Users/femilamptey/PycharmProjects/dojotest/training/2023-10-12 13-59-01.mp4'
vid = cv2.VideoCapture(videoPath)
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
out = cv2.VideoWriter("output2.mp4", fourcc, 30, (1280, 720))

conf_thres=0.7
nms_thres=0.4

def detect_image(img):
    # scale and pad image
    ratio = min(img_size/img.size[0], img_size/img.size[1])
    imw = round(img.size[0] * ratio)
    imh = round(img.size[1] * ratio)
    img_transforms=transforms.Compose([transforms.Resize((imh,imw)),
         transforms.Pad((max(int((imh-imw)/2),0),
              max(int((imw-imh)/2),0), max(int((imh-imw)/2),0),
              max(int((imw-imh)/2),0)), (128,128,128)),
         transforms.ToTensor(),
         ])
    # convert image to Tensor
    image_tensor = img_transforms(img).float()
    image_tensor = image_tensor.unsqueeze_(0)
    input_img = Variable(image_tensor.type(Tensor))
    # run inference on the model and get detections
    with torch.no_grad():
        detections = model(input_img, conf=conf_thres, iou=0.8, max_det=1)
        #detections = utils.non_max_suppression(detections, 12, conf_thres, nms_thres)

    return detections[0]


while vid.isOpened():
    ret, frame = vid.read()
    if not ret:
        break
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    pilimg = Image.fromarray(frame)
    results = model.predict(frame, conf=conf_thres, iou=0.8, max_det=1)
    detections = detect_image(pilimg)
    img = np.array(pilimg)
    pad_x = max(img.shape[0] - img.shape[1], 0) * (img_size / max(img.shape))
    pad_y = max(img.shape[1] - img.shape[0], 0) * (img_size / max(img.shape))
    unpad_h = img_size - pad_y
    unpad_w = img_size - pad_x
    annotated_frame = results[0].plot()
    if detections is not None:
        for i in range(len(detections)):
            box = detections[i, :].boxes
            cls = box.cls

            if box.conf > conf_thres:
                x1, y1, x2, y2 = box.xyxy[0]
                c = box.cls
                label = model.names[int(c)]
                box_h = int(((y2 - y1) / unpad_h) * img.shape[0])
                box_w = int(((x2 - x1) / unpad_w) * img.shape[1])
                y1 = int(((y1 - pad_y // 2) / unpad_h) * img.shape[0])
                x1 = int(((x1 - pad_x // 2) / unpad_w) * img.shape[1])
                color = colors[int(c) % len(colors)]
                color = [i * 255 for i in color]
                cv2.rectangle(frame, (x1, y1), (x1 + box_w, y1 + box_h), color,  4)
                cv2.rectangle(frame, (x1, y1 - 35), (x1 + len(label) * 19 + 60,
                                                     y1), color, -1)
                cv2.putText(frame, label,
                            (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (255, 255, 255), 3)
        cv2.imshow("YOLOv8 Tracking", annotated_frame)
        cv2.waitKey(1)
        out.write(frame)

vid.release()
out.release()

