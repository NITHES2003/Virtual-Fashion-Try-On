import cv2
import cvzone
from cvzone.PoseModule import PoseDetector
import math

def overlay_accessory(img, pose_points, accessory_path):
    # Load the accessory image
    accessory = cv2.imread(accessory_path, cv2.IMREAD_UNCHANGED)
    if accessory is None:
        print(f"Error: Unable to load accessory image from {accessory_path}")
        return img

    # Get coordinates for placing the accessory
    left_eye_outer = pose_points[3]
    right_eye_outer = pose_points[6]

    # Calculate the center point between the eyes
    center_x = int((left_eye_outer[0] + right_eye_outer[0]) / 2)
    center_y = int((left_eye_outer[1] + right_eye_outer[1]) / 2)

    # Calculate the distance between the outer eye points
    eye_distance = math.sqrt((right_eye_outer[0] - left_eye_outer[0]) ** 2 + (right_eye_outer[1] - left_eye_outer[1]) ** 2)

    # Resize the accessory based on the eye distance
    accessory_width = int(eye_distance * 1.5)  # Adjust the scaling factor as needed
    accessory_height = int(accessory_width * accessory.shape[0] / accessory.shape[1])
    accessory_resized = cv2.resize(accessory, (accessory_width, accessory_height))

    # Adjust the position of the accessory
    offset_x = int(accessory_resized.shape[1] / 2)
    offset_y = int(accessory_resized.shape[0] / 2)

    # Calculate the position to place the accessory
    accessory_x = center_x - offset_x
    accessory_y = center_y - offset_y

    # Overlay the accessory onto the original image
    img_with_accessory = cvzone.overlayPNG(img, accessory_resized, (accessory_x, accessory_y))

    return img_with_accessory

def run_script():
    # Initialize PoseDetector
    detector = PoseDetector()

    # Open the camera
    CAM_WIDTH = 1280
    CAM_HEIGHT = 720
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_HEIGHT)

    glasses_path = "specs.png"
    # Path to the new shirt images
    '''
    new_shirt_path = "1.png"
    shirt_paths = ["1.png","2.png","3.png"]  # Add more paths as needed
    current_shirt_index = 0
    imgButtonRight = cv2.imread("button.png", cv2.IMREAD_UNCHANGED)
    imgButtonLeft = cv2.imread("button.png", cv2.IMREAD_UNCHANGED)
    '''
    
    while True:
        # Read frame from camera
        success, img = cap.read()
        if not success:
            print("Failed to read frame from camera.")
            break
        
        #Overlay the button
        #img = cvzone.overlayPNG(img, imgButtonRight, (1074, 293))
        #img = cvzone.overlayPNG(img, imgButtonLeft, (72, 293))
        
        # Detect pose in the frame
        img = detector.findPose(img,draw=False)
        pose_points = detector.findPosition(img, draw=False)[0]
        
        # Replace shirt with the new shirt image
        
        img_with_glasses = overlay_accessory(img, pose_points, glasses_path)
        # Display the result
        cv2.imshow("Image", img_with_glasses)

        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()