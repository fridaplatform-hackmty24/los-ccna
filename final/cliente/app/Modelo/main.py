from ultralytics import YOLO
import cv2
import requests

# Load the OpenVINO model
ov_model = YOLO(r"D:\leemo\Documents\Documentos personales\Repositorios\HackMty_CCNA\Modelo\best.pt")

# Initialize webcam capture
cap = cv2.VideoCapture(0)  # 0 is the default camera, change to 1 or other index if needed

# Define colors for left and right boxes
left_color = (0, 255, 0)  # Green for left
right_color = (0, 0, 255)  # Red for right

# Loop to process each frame from the webcam
while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Failed to capture image")
        break

    image_height, image_width = frame.shape[:2]
    midpoint = image_width // 2

    # Run inference on the frame
    results = ov_model(frame)

    # Initialize counts
    left_count = 0
    right_count = 0

    # Process results
    for result in results:
        # Access bounding boxes
        boxes = result.boxes

        # Draw bounding boxes on the image
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0].int().tolist()
            label = ov_model.names[int(box.cls)]
            confidence = box.conf.item()

            # Check if the box is in the left or right half
            box_midpoint = (x1 + x2) // 2
            if box_midpoint < midpoint:
                position = "left"
                color = left_color
                left_count += 1
            else:
                position = "right"
                color = right_color
                right_count += 1

            # Draw the bounding box and label on the image
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, f"{label} {confidence:.2f} ({position})", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    # Send counts to Flask endpoint
    data = {
        "left_count": left_count,
        "right_count": right_count
    }

    # Update the URLs to send requests to localhost using HTTP
    request_1 = f"http://localhost:5000/racks/rack_1/{left_count}"
    request_2 = f"http://localhost:5000/racks/rack_2/{right_count}"
    
    print(request_1)

    try:
        # Send POST request to the HTTP endpoint (no SSL)
        response_1 = requests.post(request_1, json=data)  # Send request to localhost
        response_1.raise_for_status()  # Raise an HTTPError for bad responses
        print(response_1.json())

        response_2 = requests.post(request_2, json=data)
        response_2.raise_for_status()  # Raise an HTTPError for bad responses
        print(response_2.json())

    except requests.exceptions.RequestException as e:
        print(f"Error sending data to server: {e}")

    # Display the frame with bounding boxes
    cv2.imshow("YOLOv8 Detection", frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close OpenCV windows
cap.release()
cv2.destroyAllWindows()