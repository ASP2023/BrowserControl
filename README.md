# BrowserControl

## User Guide for GestureRecognizer
Install [mediapipe](https://developers.google.com/mediapipe/solutions/vision/gesture_recognizer/python):
```
pip install mediapipe
```

Please be aware that MediaPipe currently does not fully support Windows (see issue: https://github.com/google/mediapipe/issues/4272)

1. Create a GestureRecognizer object:

```
gesture_recognizer = GestureRecognizer()
```

2. Process a single frame:

```
gesture_recognizer.run()
```

3. Get recognized result:

```
gestures = gesture_recognizer.gestures
```

If both hands are detected， the dual-hand gestures are represented as `gestures["dual_hand"] = [LEFT_HAND_GESTURE, RIGHT_HAND_GESTURE]`.

If only single hand are detected, the single-hand gesture is represented as `gestures["hand"] = [GESTURE]`

Here, gestures has 8 possible string values: `["None",
      "Closed_Fist", "Open_Palm", "Pointing_Up", "Thumb_Down", "Thumb_Up",
      "Victory", "ILoveYou"]`.

You can modify the function 
```
def get_command(self):
    # your code
```

to transfer the gesture strings to selenium command.

## Demo
For guesture recognition demo:
```
python gesture.py
```
For browser control demo:

```
python test.py
```

or

```
python PDFdemo.py
```

## Acknowledgement

[MediaPipe](https://github.com/google/mediapipe)
