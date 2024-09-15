from ultralytics import YOLO
import cv2
import time
from main import get_rack_number
from gtts import gTTS
import pygame

# Function to adjust brightness and contrast
def adjust_brightness_contrast(image, alpha=0, beta=-150):
    adjusted = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return adjusted
def emitirMensaje(mensaje):
    language = "es"
    gtts_object = gTTS(text=mensaje, lang=language, slow=False)
    gtts_object.save("gtts.mp3")

    pygame.mixer.init()
    pygame.mixer.music.load('gtts.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
# Function to prompt the user for their next action
def ask_for_next_action():
    return get_rack_number_from_main()

#esta funcion cicla lo de la traduccion del query
def get_rack_number_from_main():
    emitirMensaje("Puede preguntar sobre un producto")
    rack_number = get_rack_number()
    if rack_number is not None:
        print(f"Rack number obtained: {rack_number}")
        return rack_number
    else:
        print("No rack number found. Please try again.")
        return None

# Load the YOLO model
model = YOLO(r"/home/dzl/Downloads/finalopen1/chico_openvino_model  ")

# Initialize the webcam (0 for default camera)
cap = cv2.VideoCapture(0)

# Set the resolution to 640x480
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Check if the webcam is opened correctly
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Initialize variables for sign detection
sign_detected = False
previous_state = False
current_sign = 0  # Start at position 0
max_signs = 3     # Limit the system to 3 signs
rack_map = {
    1: {"left": 1, "right": 2},
    2: {"left": 3, "right": 4},
    3: {"left": 5, "right": 6}
}
no_sign_frames = 20
entered_rack = False

target_rack = ask_for_next_action()
going_backwards = False

emitirMensaje(f"empezando en la posicion {current_sign}")
print(f"Starting at position {current_sign}")

# Function to provide walking instructions
def provide_walking_instructions(current_sign, target_rack):
    if current_sign in rack_map:
        if rack_map[current_sign]["left"] == target_rack:
            return f"Gira a la derecha al para ir al rack {target_rack}. Detente"
        else:
            return "N"
    else:
        return "No valid sign detected. Continue walking."



# Function to check if user is going backwards
def check_if_going_backwards(current_sign, target_sign):
    return current_sign > target_sign

# Main detection loop
while True:
    if entered_rack:  # After entering the target rack, ask the user what to do next
        pygame.mixer.music.load('pitido.mp3')
        pygame.mixer.music.play()
        emitirMensaje("has llegado a tu destino")
        print(f"Arrived at {target_rack}. You can now stop walking.")
        target_rack = ask_for_next_action()  # Ask for the next action

        if target_rack == 0:
            print("Returning to the start position.")
             # Reset to start
        else:
            target_sign = next((sign for sign, racks in rack_map.items() if target_rack in racks.values()), None)
            if target_sign is None:
                print("Error: Invalid rack choice.")
                continue  # Ask for a valid choice again
            going_backwards = check_if_going_backwards(current_sign, target_sign)
            if going_backwards:
                print(f"Turn around to go back to Sign {target_sign}.")
                emitirMensaje(f"da la vuelta al signo {target_sign}")
            else:
                emitirMensaje(f"avanzando hacia rack {target_rack}")
                print(f"Heading forward to {target_rack}.")
        entered_rack = False  # Reset flag to start looking for signs again
        print(f"Heading to {target_rack}")

    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Adjust brightness and contrast of the current frame
    processed_frame = adjust_brightness_contrast(frame, alpha=1.5, beta=-50)

    # Use the model to make predictions on the processed frame
    results = model(processed_frame, imgsz=640, verbose=False)

    # Reset sign detection for this frame
    sign_detected = False

    # Loop through results to check for sign detection
    for result in results:
        boxes = result.boxes
        for box in boxes:
            # Get bounding box coordinates and label
            x1, y1, x2, y2 = [int(coord) for coord in box.xyxy[0].tolist()]
            label = model.names[int(box.cls)]
            confidence = box.conf.item()

            # Check if the detected object is the sign
            if label == "no-parking-and-stopping":  # Replace with your sign's label
                sign_detected = True
                no_sign_frames = 0  # Reset the no-sign frame counter

                # Draw the bounding box and label on the frame
                cv2.rectangle(processed_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Handle transitions between detecting and not detecting the sign
    if not sign_detected:
        no_sign_frames += 1  # Increment the no-sign counter

    # If the sign is not detected for more than a threshold (e.g., 10 frames)
    if no_sign_frames > 10:
        previous_state = False

    # If the sign is detected after being lost for a few frames (a transition)
    if sign_detected and not previous_state:
        if going_backwards:
            current_sign -= 1  # Decrement the sign counter if going backwards
        else:
            current_sign += 1  # Increment the sign counter if going forward

        # Ensure the sign count does not exceed 3
        if current_sign > max_signs:
            current_sign = 1

        print(f"Detected new sign: Sign {current_sign}")

        result=provide_walking_instructions(current_sign, target_rack)
        if result!="":
            emitirMensaje(result)

        

        # Check if we've reached the target sign and are ready to enter the rack
        if rack_map.get(current_sign, {}).get("left") == target_rack or rack_map.get(current_sign, {}).get("right") == target_rack:
            entered_rack = True  # Assume the user enters the rack
            print(f"Arrived at {target_rack}. Entering the rack...")

        # Update the previous state to reflect the new detection
        previous_state = True

    # Constantly print walking instructions if no specific action has been instructed
    if not sign_detected and no_sign_frames > 10:
        print("Continue walking...")
    

    # Display the preprocessed frame (adjusted brightness and contrast)
    cv2.imshow("Preprocessed Frame (Brightness & Contrast Adjusted)", processed_frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
