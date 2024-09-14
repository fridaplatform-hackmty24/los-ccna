from ultralytics import YOLO

# Load a model
model = YOLO("yolov8n.yaml")  # build a new model from scratch

# Use the model
model.train(data="Supermarket Empty Shelf Detector.v4i.yolov8/data.yaml", epochs=3)  # train the model


