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

Here, gestures is a dictionary as: `{'category': 'Pointing_Up', 'direction': 'LEFT'}`

`category` has 8 possible values: `["None",
      "Closed_Fist", "Open_Palm", "Pointing_Up", "Thumb_Down", "Thumb_Up",
      "Victory", "ILoveYou"]`.

`direction` has 5 possible values: `["None","LEFT","RIGHT","DOWN","UP"]`.


## Demo

```
python gesture.py
```
