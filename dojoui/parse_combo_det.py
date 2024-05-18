from ultralytics import YOLO
import cv2
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image
from torchvision import datasets, transforms
from torch.autograd import Variable
import torch
from torch import Tensor
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import sys

model = YOLO("best.pt")
model.to('mps')

desired_classes = [0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11]

detections = model.track("/Users/femilamptey/PycharmProjects/dojotest/training/2023-10-12 13-59-01.mp4",
                         classes=desired_classes, save=False, show=True, max_det=1, persist=True, conf=0.8, iou=0.8,
                         device="mps")
window = 15

moves = []

for i in range(window, len(detections)):
    dets = detections[i - window:i]
    conf_sum = [0] * len(dets[0].names)
    conf_count = [0] * len(dets[0].names)
    for det in dets:
        box = det.boxes
        if len(box.cls) != 0:
            cls = int(box.cls[0])
            conf = box.conf[0]
            conf_sum[cls] += conf
            conf_count[cls] += 1
    conf_avg = []
    for x in range(len(conf_sum)):
        if conf_count[x] != 0:
            conf_avg.append(conf_sum[x] / conf_count[x])
        else:
            conf_avg.append(0)
    if (max(conf_avg) != 0) & (max(conf_avg) >= 0.85):
        max_idx = conf_sum.index(max(conf_sum))
        # print("Most likely move is: " + str(dets[0].names[max_idx]))
        moves.append(dets[0].names[max_idx])

print(detections[0].names)

print("moves: " + str(moves))
print(len(moves))
move_tally = 0
combo = []
repeats = 12
for i in range(1, len(moves)):
    if (moves[i] == moves[i - 1]) & (move_tally < repeats):
        move_tally += 1

    if move_tally == repeats:
        if len(combo) != 0:
            if combo[-1] != moves[i]:
                combo.append(moves[i])
                move_tally = 0
        else:
            combo.append(moves[i])
            move_tally = 0

    if moves[i] != moves[i - 1]:
        move_tally = 0

print("combo: " + str(combo))
print(len(combo))

cred = credentials.Certificate("dojo-capstone-firebase-adminsdk-xntkg-a7ee737a7a.json")
# Initialize the app with a service account, granting admin privileges
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred)

db = firestore.client()

# Choose a Firestore collection where you want to store the array
collection_name = "combos"

# Set a document ID (or let Firestore auto-generate one)
document_id = "Combo 2"

doc_ref = db.collection(collection_name).document(document_id)
doc_ref.set({"name": "Combo 2","combo": combo})
print(sys.getsizeof(combo))


