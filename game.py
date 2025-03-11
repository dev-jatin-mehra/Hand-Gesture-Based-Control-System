import cv2
from hand_tracker import HandTracker
from key_controller import press_key, release_keys
from key_mappings import KEY_MAP

# Initialize Hand Tracker
hand_tracker = HandTracker()
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip frame for a mirror effect
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # Process hand tracking
    results = hand_tracker.process_frame(frame)
    active_keys = set()

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            hand_tracker.draw_landmarks(frame, [hand_landmarks])
            landmarks = hand_landmarks.landmark
            
            # Y-coordinates of fingertips (normalized 0 to 1)
            index_tip = landmarks[8].y
            middle_tip = landmarks[12].y
            pinky_tip = landmarks[20].y
            thumb_tip = landmarks[4].y

            # Y-coordinates of base joints (to check if a finger is raised)
            index_base = landmarks[5].y
            middle_base = landmarks[9].y
            pinky_base = landmarks[17].y
            thumb_base = landmarks[2].y

            # Define raised finger conditions
            index_raised = index_tip < index_base - 0.05
            middle_raised = middle_tip < middle_base - 0.05
            pinky_raised = pinky_tip < pinky_base - 0.05
            thumb_raised = thumb_tip < thumb_base - 0.05

            # Movement Conditions
            if index_raised and not (middle_raised or pinky_raised):
                active_keys.add(KEY_MAP["forward"])  # Move forward (W)
            elif pinky_raised and not (index_raised or middle_raised):
                active_keys.add(KEY_MAP["backward"])  # Move backward (S)
            elif index_raised and pinky_raised and not middle_raised:
                active_keys.add(KEY_MAP["jump"])  # Jump (Space)
            elif index_raised and middle_raised and not pinky_raised:
                active_keys.add(KEY_MAP["left"])  # Move left (A)
            elif middle_raised and pinky_raised and not index_raised:
                active_keys.add(KEY_MAP["right"])  # Move right (D)
            elif middle_raised and not (index_raised or thumb_raised or pinky_raised):
                active_keys.add(KEY_MAP["sprint"])  # Sprint (Shift)

    # Simulate key presses
    for key in active_keys:
        press_key(key)

    release_keys(set(KEY_MAP.values()) - active_keys)
    cv2.imshow("Hand Tracking - Game Control", frame)

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
