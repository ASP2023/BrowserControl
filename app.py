from flask import Flask, render_template, request
from test import main # Replace this with the name of your gesture recognition Python file

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start-gesture-recognition', methods=['POST'])
def start_gesture_recognition():
    # Call your gesture recognition function here
    # your_gesture_recognition_module.start_gesture_recognition()  # Replace with the function name that starts your gesture recognition
    main()
    return 'Gesture recognition started'

if __name__ == '__main__':
    app.run(debug=True)
