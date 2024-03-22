import cv2
import cvzone
from cvzone.PoseModule import PoseDetector
import time

# Function to replace shirt in the image
def replace_shirt(img, pose_points, new_shirt_path):
    # Load the new shirt image
    new_shirt = cv2.imread(new_shirt_path, cv2.IMREAD_UNCHANGED)
    if new_shirt is None:
        print(f"Error: Unable to load shirt image from {new_shirt_path}")
        return img

    # Extract pose points for relevant body parts
    left_shoulder = pose_points[11]
    right_shoulder = pose_points[12]
    left_hip = pose_points[23]
    right_hip = pose_points[24]

    # Calculate shirt width and height
    shirt_width = int(abs(right_shoulder[0] - left_shoulder[0]))
    shirt_height = int(abs(right_hip[1] - left_shoulder[1]))

    # Resize new shirt image to match the calculated width and height
    new_shirt_resized = cv2.resize(new_shirt, (shirt_width+30, shirt_height+30))

    # Calculate the position to place the shirt
    shirt_x = int(right_shoulder[0])
    shirt_y = int(right_shoulder[1])
    

    # Overlay the new shirt onto the original image
    img_with_shirt = cvzone.overlayPNG(img, new_shirt_resized, (shirt_x-15, shirt_y-30))

    return img_with_shirt

def run_script():
    detector = PoseDetector()

    # Open the camera
    CAM_WIDTH = 1280
    CAM_HEIGHT = 720
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_HEIGHT)

    # Path to the new shirt images
    new_shirt_path = "1.png"
    shirt_paths = ["1.png","2.png","3.png"]  # Add more paths as needed
    current_shirt_index = 0
    imgButtonRight = cv2.imread("button.png", cv2.IMREAD_UNCHANGED)
    imgButtonLeft = cv2.imread("button.png", cv2.IMREAD_UNCHANGED)

    zoom_scale = 1.0
    shirt_scale = 1.0

    while True:
        # Read frame from camera
        success, img = cap.read()
        if not success:
            print("Failed to read frame from camera.")
            break
        
        #Overlay the button
        img = cvzone.overlayPNG(img, imgButtonRight, (1074, 293))
        img = cvzone.overlayPNG(img, imgButtonLeft, (72, 293))
        
        # Detect pose in the frame
        img = detector.findPose(img,draw=False)
        pose_points = detector.findPosition(img, draw=False)[0]

        # Check if the left hand is raised
        if pose_points[15][1] < pose_points[13][1] and pose_points[15][1] < pose_points[11][1]:
            # Change to the previous shirt
            current_shirt_index = (current_shirt_index + 1) % len(shirt_paths)
            new_shirt_path = shirt_paths[current_shirt_index]
            time.sleep(0.4)

        # Check if the right hand is raised
        if pose_points[16][1] < pose_points[14][1] and pose_points[16][1] < pose_points[12][1]:
            # Change to the next shirt
            current_shirt_index = (current_shirt_index - 1) % len(shirt_paths)
            new_shirt_path = shirt_paths[current_shirt_index]
            time.sleep(0.4)

        # Replace shirt with the new shirt image
        img_with_shirt = replace_shirt(img, pose_points, new_shirt_path)
        
        # Display the result
        cv2.imshow("Image", img_with_shirt)

        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()