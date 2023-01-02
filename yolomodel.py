import torch
import os

model = torch.hub.load('ultralytics/yolov5', 'custom', path='pepsi-model.pt', device="cpu")

