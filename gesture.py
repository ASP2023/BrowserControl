import cv2
import mediapipe as mp
import time
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from drawing_utils import draw_landmarks
import numpy as np


class GestureRecognizer():
    def __init__(self) -> None:
        """
        1. Initialize the gesture recognizer
        2. Set parameters
        3. Open the camera
        """
        base_options = python.BaseOptions(
            model_asset_path='gesture_recognizer.task')
        options = vision.GestureRecognizerOptions(base_options=base_options,num_hands=2)
        self.recognizer = vision.GestureRecognizer.create_from_options(options)
        self.direction = None
        self.continous_moving_cnt = 0
        self.MOVING_THRESHOLD = 50
        self.prev_landmarks = None
        self.cap = cv2.VideoCapture(0)
        # category: ["None", "Closed_Fist", "Open_Palm", "Pointing_Up",
        #            "Thumb_Down", "Thumb_Up", "Victory", "ILoveYou"]
        self.gestures = {'dual_hand': None,'hand':None}

    def clear_gesture_cache(self):
        self.gestures = {'dual_hand': None,'hand':None}
    
    def get_command(self):
        # gesture is saved by string in one of the following 8 strings: 
        #       ["None", "Closed_Fist", "Open_Palm", "Pointing_Up",
        #            "Thumb_Down", "Thumb_Up", "Victory", "ILoveYou"]
        if self.gestures['dual_hand'] is None:
            return None
        else:
            left_gesture  = self.gestures['dual_hand'][0]
            right_gesture = self.gestures['dual_hand'][1]
            # left closed_fist, right thumb_up = quick scroll up
            # left closed_fist, right thumb_down = quick scroll down
            if left_gesture == 'Closed_Fist' and right_gesture == 'Thumb_Up':
                return 'quick_scroll_up'
            elif left_gesture == 'Closed_Fist' and right_gesture == 'Thumb_Down':
                return 'quick_scroll_down'
            # left pointing_up, right thumb_up = scroll up
            # left pointing_up, right thumb_down = scroll down
            if left_gesture == 'Pointing_Up' and right_gesture == 'Thumb_Up':
                return 'scroll_up'
            elif left_gesture == 'Pointing_Up' and right_gesture == 'Thumb_Down':
                return 'scroll_down'
            
            if left_gesture == 'ILoveYou' and right_gesture == 'Thumb_Up':
                return 'slow_scroll_up'
            if left_gesture == 'ILoveYou' and right_gesture == 'Thumb_Down':
                return 'slow_scroll_down'
            
            # if both hands open palm = pause
            if left_gesture == 'Open_Palm' and right_gesture == 'Open_Palm':
                return 'pause'
            if left_gesture == 'Thumb_Up' and right_gesture == 'Thumb_Up':
                return 'play'
            # if both hands pointing up = zoom in
            if left_gesture == 'Pointing_Up' and right_gesture == 'Pointing_Up':
                return 'zoom_in'
            
            # if both hands colsed fist = zoom out
            if left_gesture == 'Closed_Fist' and right_gesture == 'Closed_Fist':
                return 'zoom_out'
            
            
            return None

    def run(self,fps=False):
        """
        1. Capture the frame
        2. Recognize the gesture
        3. Visualize the result
        """
        start_time = time.time()
        ret, frame = self.cap.read()
        self.h = frame.shape[0]
        self.w = frame.shape[1]
        if not ret:
            return
        self.recog_result = self.recognize(frame)
        frame = self.visualize(frame, self.recog_result)
        cv2.putText(frame, 'FPS: {:.2f}'.format(1/(time.time()-start_time)), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.imshow('Gesture Recognizer', frame)
        return

    def landmark_cvt_to_numpy(self, landmarks):
        """
        convert landmark to numpy array: 
            return: np.array[21x3]
        """
        landmarks = self.recog_result.hand_landmarks[0]  # only one hand
        # landmarks is a list of 21 landmark_module.NormalizedLandmark
        landmark_np = np.array(
            [[landmark.x*self.w, landmark.y*self.h] for landmark in landmarks])
        return landmark_np

    def recognize(self, frame):
        # Convert the image to an RGB image
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
        recognition_result = self.recognizer.recognize(mp_image)
        return recognition_result

    def visualize(self, frame, recog_result):
        # Draw the recognized gesture on the frame
        if not recog_result.hand_landmarks:
            return frame
        
        for landmark_list in recog_result.hand_landmarks:
            draw_landmarks(frame, landmark_list,
                    mp.solutions.hands.HAND_CONNECTIONS)
        if len(recog_result.handedness) == 2:
            # if two hands are detected
            if recog_result.handedness[0][0].category_name == 'Left':
                left_hand_gesture = recog_result.gestures[recog_result.handedness[0][0].index]
                right_hand_gesture = recog_result.gestures[recog_result.handedness[1][0].index]
            else:
                left_hand_gesture = recog_result.gestures[recog_result.handedness[1][0].index]
                right_hand_gesture = recog_result.gestures[recog_result.handedness[0][0].index]
            self.gestures['dual_hand'] = [left_hand_gesture[0].category_name, right_hand_gesture[0].category_name]
            self.gestures['hand'] = None
            cv2.putText(frame, left_hand_gesture[0].category_name, (10, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, right_hand_gesture[0].category_name, (self.w - 240, 100),    
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        else:
            self.gestures['dual_hand'] = None
            self.gestures['hand'] = recog_result.gestures[0][0].category_name
            hand_gesture = recog_result.gestures[0]
            cv2.putText(frame, hand_gesture[0].category_name, (10, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        # for ges in recog_result.gestures:
        #     ges_name = ges[0].category_name
        #     if ges_name != 'None':
        #         self.gestures['category'] = ges_name
        #         # put text on cv2 window
        #         cv2.putText(frame, ges_name, (10, 30),
        #                     cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        # self.update_direction(self.landmark_cvt_to_numpy(
        #     recog_result.hand_landmarks))
        # self.prev_landmarks = self.landmark_cvt_to_numpy(
        #     recog_result.hand_landmarks)
        # if self.direction != 'None':
        #     self.gestures['direction'] = self.direction
        #     cv2.putText(frame, self.direction, (10, 60),
        #                 cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        return frame

    def update_direction(self, landmarks):
        if self.prev_landmarks is None:
            self.direction = None
            return
        x_diff = landmarks[0, 0] - self.prev_landmarks[0, 0]
        y_diff = landmarks[0, 1] - self.prev_landmarks[0, 1]
        def diff_to_direction_y(diff):
            if abs(diff) < self.MOVING_THRESHOLD:
                return 'None'
            if diff > 0:
                return 'DOWN'
            else:
                return 'UP'
        def diff_to_direction_x(diff):
            if abs(diff) < self.MOVING_THRESHOLD:
                return 'None'
            if diff > 0:
                return 'LEFT'
            else:
                return 'RIGHT'
        # print(x_diff, y_diff)
        if abs(x_diff) > abs(y_diff):
            self.direction = diff_to_direction_x(x_diff)
        else:
            self.direction = diff_to_direction_y(y_diff)
        # self.direction = None


if __name__ == '__main__':
    gesture_recognizer = GestureRecognizer()
    start_time = time.time()
    frame_count = 0
    while True:
        gesture_recognizer.run()            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
                    
    gestures = gesture_recognizer.gestures
    print(gestures)
