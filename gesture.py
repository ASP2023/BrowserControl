import cv2
import mediapipe as mp
import time
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from drawing_utils import draw_landmarks
import numpy as np
import pyautogui
import copy
np.set_printoptions(precision=2)



class GestureRecognizer:
    def __init__(self) -> None:
        """
        1. Initialize the gesture recognizer
        2. Set parameters
        3. Open the camera
        """
        base_options = python.BaseOptions(model_asset_path="gesture_recognizer.task")
        options = vision.GestureRecognizerOptions(
            base_options=base_options, num_hands=2
        )
        self.recognizer = vision.GestureRecognizer.create_from_options(options)
        self.direction = None
        self.continous_moving_cnt = 0
        self.MOVING_THRESHOLD = 50
        self.prev_landmarks = None
        self.cap = cv2.VideoCapture(0)
        # category: ["None", "Closed_Fist", "Open_Palm", "Pointing_Up",
        #            "Thumb_Down", "Thumb_Up", "Victory", "ILoveYou"]
        self.gestures = {"dual_hand": None, "hand": None}
        self.freeze = False
        self.freeze_pos = None
        self.factor = 2  # the factor to control the speed of mouse movement
        self.time_stamp = time.time()
        self.time_for_click = time.time()
        self.direction_time_stamp = time.time()
        self.pre_pts = []
        self.cur_pts = []
        self.cur_time = time.time()
        self.pre_time = time.time()
        self.counter = 0
        self.duration_bound = 0.0
        self.mid_fig_direction = []
        self.ring_fig_direction = []
        self.rotation = 0
        self.rotation_cd = False
        self.rotation_last_time = 0

        self.pre_idx_fig_tip = []
        self.cur_idx_fig_tip = []

        self.pre_location = []
        self.cur_location = []
        self.vx = 0
        self.vy = 0

    def clear_gesture_cache(self):
        self.gestures = {"dual_hand": None, "hand": None}

    def location_to_direction(
        self,
    ):
        # only one hand to trigger the gesture
        if self.recog_result.hand_landmarks:
            if self.vx >= 5:
                return "right"
            if self.vx <= -5:
                return "left"
            if self.vy >= 5:
                return "down"
            if self.vy <= -5:
                return "up"

        #    landmark = self.landmark_cvt_to_numpy(self.recog_result.hand_landmarks[0])
        #    if landmark[:, 0].min() < self.w / 10:
        #        return "left"
        #    if landmark[:, 0].max() > self.w * 9 / 10:
        #        return "right"
        #    if landmark[:, 1].min() < self.h / 10:
        #        return "up"
        #    if landmark[:, 1].max() > self.h * 9 / 10:
        #        return "down"
            return None
        #for hand_lanmark in self.recog_result['hand_landmarks']:

    def get_command(self):
        # gesture is saved by string in one of the following 8 strings:
        #       ["None", "Closed_Fist", "Open_Palm", "Pointing_Up",
        #            "Thumb_Down", "Thumb_Up", "Victory", "ILoveYou"]
        if self.direction is not None:
            # map direction to wsad
            # this mapping works at most once per 0.5 seconds
            if time.time() - self.direction_time_stamp > 0.5:
                self.direction_time_stamp = time.time()
                direction_to_wasd = {"left": "a", "right": "d", "up": "w", "down": "s"}
                return direction_to_wasd[self.direction]
        if self.gestures["hand"]:
            return None
        elif self.gestures["dual_hand"]:
            left_gesture = self.gestures["dual_hand"][0]
            right_gesture = self.gestures["dual_hand"][1]

    def take_over_mouse(self, frame):
        # if one hand and closed fist, then start to take over mouse control
        cv2.putText(
            frame,
            "Take Over Mouse Control",
            (10, 300),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2,
            cv2.LINE_AA,
        )
        # show mouse position
        cv2.putText(
            frame,
            "Mouse Position: {}".format(pyautogui.position()),
            (10, 400),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2,
            cv2.LINE_AA,
        )
        # show screen middle position
        screen_width, screen_height = pyautogui.size()
        cv2.putText(
            frame,
            "middle position: {}".format((screen_width / 2, screen_height / 2)),
            (10, 500),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2,
            cv2.LINE_AA,
        )
        # If one hand and open palm, then reset the mouse position
        if (
            len(self.recog_result.handedness) == 1
            and self.recog_result.gestures[0][0].category_name == "Open_Palm"
        ):
            screen_width, screen_height = pyautogui.size()
            pyautogui.moveTo(screen_width // 2, screen_height // 2)
            self.freeze_pos = self.landmark_cvt_to_numpy(self.recog_result.hand_landmarks[0])
            self.start_x = self.freeze_pos[8, 0]
            self.start_y = self.freeze_pos[8, 1]
        elif (
            len(self.recog_result.handedness) == 1
            and self.recog_result.gestures[0][0].category_name == "Pointing_Up"
        ):
            if self.freeze == False:
                self.freeze_pos = self.landmark_cvt_to_numpy(
                    self.recog_result.hand_landmarks[0]
                )
                self.start_x = self.freeze_pos[8, 0]
                self.start_y = self.freeze_pos[8, 1]
                self.mouse_init_pos = pyautogui.position()
                self.freeze = True
            else:
                # use the index finger tip (食指指头) to locate the mouse
                
                cur_pos = self.landmark_cvt_to_numpy(
                    self.recog_result.hand_landmarks[0]
                )
                cur_x = cur_pos[8, 0]
                cur_y = cur_pos[8, 1]
                move_x = (cur_x - self.start_x) * self.factor
                move_y = (cur_y - self.start_y) * self.factor
                pyautogui.moveTo(
                    self.mouse_init_pos[0] + move_x, self.mouse_init_pos[1] + move_y
                )
            # if one hand and closed fist, then start to click mouse, this action takes at most once per 0.5s
        elif (
            len(self.recog_result.handedness) == 1
            and self.recog_result.gestures[0][0].category_name == "Closed_Fist"
        ):
            if time.time() - self.time_stamp >= 0.5:
                pyautogui.click()
                self.time_stamp = time.time()
        return frame

    def run(self, fps=False):
        """
        1. Capture the frame
        2. Recognize the gesture
        3. Visualize the result
        """
        start_time = time.time()
        ret, frame = self.cap.read()
        frame = cv2.flip(frame, 1)
        self.h = frame.shape[0]
        self.w = frame.shape[1]
        if not ret:
            return
        self.recog_result = self.recognize(frame)
        frame = self.visualize(frame, self.recog_result)
        frame = self.update_direction(frame)
        frame = self.take_over_mouse(frame)
        cv2.putText(
            frame,
            "FPS: {:.2f}".format(1 / (time.time() - start_time)),
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2,
            cv2.LINE_AA,
        )
        cv2.imshow("Gesture Recognizer", frame)
        print(self)
        return

    def landmark_cvt_to_numpy(self, landmarks):
        """
        convert landmark to numpy array:
            return: np.array[21x3]
        """
        # landmarks = self.recog_result.hand_landmarks[0]  # only one hand
        # landmarks is a list of 21 landmark_module.NormalizedLandmark
        landmark_np = np.array(
            [[landmark.x * self.w, landmark.y * self.h] for landmark in landmarks]
        )
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
        print(recog_result.handedness)

        for landmark_list in recog_result.hand_landmarks:
            draw_landmarks(frame, landmark_list, mp.solutions.hands.HAND_CONNECTIONS)

        # cur_pts stores the current key points positions
        self.cur_pts = []
        self.cur_time = time.time()
        for idx, landmark in enumerate(landmark_list):
            if False and ((hasattr(landmark, 'visibility') and
                           landmark.visibility < _VISIBILITY_THRESHOLD) or
                          (hasattr(landmark, 'presence') and
                           landmark.presence < _PRESENCE_THRESHOLD)):
                continue
            self.cur_pts.append([landmark.x, landmark.y, landmark.z])
            if idx == 12:
                self.cur_location = np.array([landmark.x, landmark.y, landmark.z])
            if idx == 8:
                self.cur_idx_fig_tip = np.array([landmark.x, landmark.y, landmark.z])

        if len(self.pre_location) != 0:
            d_loc = self.cur_location - self.pre_location
            dt = self.cur_time-self.pre_time
            self.vx, self.vy = d_loc[0]/dt, d_loc[1]/dt

        #update
        self.pre_time = self.cur_time
        self.pre_location = copy.deepcopy(self.cur_location)
        self.pre_idx_fig_tip = copy.deepcopy(self.cur_idx_fig_tip)


        if len(recog_result.handedness) == 2:
            # if two hands are detected
            if recog_result.handedness[0][0].category_name == "Left":
                left_hand_gesture = recog_result.gestures[
                    recog_result.handedness[0][0].index
                ]
                right_hand_gesture = recog_result.gestures[
                    recog_result.handedness[1][0].index
                ]
            else:
                left_hand_gesture = recog_result.gestures[
                    recog_result.handedness[1][0].index
                ]
                right_hand_gesture = recog_result.gestures[
                    recog_result.handedness[0][0].index
                ]
            # flip left and right hand
            left_hand_gesture, right_hand_gesture = (
                right_hand_gesture,
                left_hand_gesture,
            )
            self.gestures["dual_hand"] = [
                left_hand_gesture[0].category_name,
                right_hand_gesture[0].category_name,
            ]
            self.gestures["hand"] = None
            cv2.putText(
                frame,
                left_hand_gesture[0].category_name,
                (10, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2,
                cv2.LINE_AA,
            )
            cv2.putText(
                frame,
                right_hand_gesture[0].category_name,
                (self.w - 240, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2,
                cv2.LINE_AA,
            )
        else:
            self.gestures["dual_hand"] = None
            self.gestures["hand"] = recog_result.gestures[0][0].category_name
            hand_gesture = recog_result.gestures[0]
            cv2.putText(
                frame,
                hand_gesture[0].category_name,
                (10, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2,
                cv2.LINE_AA,
            )
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

    def update_direction(self, frame):
        direction = self.location_to_direction()
        self.direction = direction
        if direction is not None:
            cv2.putText(
                frame,
                direction,
                (10, 190),
                cv2.FONT_HERSHEY_SIMPLEX,
                2,
                (0, 0, 255),
                2,
                cv2.LINE_AA,
            )
        return frame


if __name__ == "__main__":
    gesture_recognizer = GestureRecognizer()
    start_time = time.time()
    frame_count = 0
    while True:
        gesture_recognizer.run()
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    gestures = gesture_recognizer.gestures
