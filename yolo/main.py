from ultralytics import YOLO

# Load a model
model = YOLO("yolov8n.yaml")  # build a new model from scratch

# Train the model
model.train(data="data.yaml", epochs=300, patience=10)  # train the model

# Save the trained model weights
model.export(format="openvino")

# Load the trained model weights
trained_model = YOLO("/home/sofia/Documents/hackmty/yolo/runs/detect/train2/weights")

# Run inference on a new image
results = trained_model("/home/sofia/Documents/hackmty/yolo/test/images/test2020_1008_jpg.rf.4000b10bafa46aa0862f29ba58124dff.jpg")

# Process and display results
for result in results:
    # Access bounding boxes, scores, and class labels
    boxes = result.boxes
    scores = result.scores
    classes = result.classes

    # Optionally, access masks if available
    masks = result.masks if hasattr(result, 'masks') else None

    # Draw bounding boxes on the image
    image = cv2.imread("path/to/new_image.jpg")
    for box, score, cls in zip(boxes, scores, classes):
        x1, y1, x2, y2 = box.xyxy[0].int().tolist()
        label = trained_model.names[int(cls)]
        confidence = score.item()
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, f"{label} {confidence:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Display the image
    cv2.imshow("YOLOv8 Detection", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
