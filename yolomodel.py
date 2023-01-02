import torch
import os

modelpath = os.getcwd()
model = torch.hub.load('ultralytics/yolov5', 'custom', path=modelpath+'/pepsi-model.pt', device="cpu")

