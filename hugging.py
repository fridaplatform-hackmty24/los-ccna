from ultralytics import YOLO
import cv2

# Load the YOLO model
model = YOLO(r"C:\Users\sofia\Desktop\hack\hugging\best.pt")

# Define the traffic sign class labels
traffic_light_label = ["no-parking", "no-stopping", "no-stopping-and-parking", "no-parking-and-stopping"]

# Initialize the webcam (0 for default camera)
cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Loop to continuously get frames from the webcam
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Use the model to make predictions on the current frame
    results = model(frame)

    largest_box = None
    largest_area = 0

    # Loop through results and find the largest bounding box
    for result in results:
        boxes = result.boxes
        for box in boxes:
            # Get bounding box coordinates
            x1, y1, x2, y2 = [int(coord) for coord in box.xyxy[0].tolist()]
            label = model.names[int(box.cls)]
            confidence = box.conf.item()

            # Calculate the area of the bounding box
            area = (x2 - x1) * (y2 - y1)

            # Check if this is the largest box so far
            if area > largest_area:
                largest_area = area
                largest_box = (x1, y1, x2, y2)

            # Draw the bounding box and label on the frame
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {confidence:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # If the largest box is found, crop and display it
    if largest_box is not None:
        x1, y1, x2, y2 = largest_box
        cropped_image = frame[y1:y2, x1:x2]
        cv2.imshow("Largest Traffic Sign", cropped_image)

    # Display the frame with bounding boxes
    cv2.imshow("YOLOv8 Webcam Detection", frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
