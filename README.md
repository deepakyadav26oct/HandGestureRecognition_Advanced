# Hand Gesture Recognition -- Advanced Project

A Python-based computer-vision project that uses a webcam to detect hand
landmarks and map selected hand gestures to computer actions. The
project is designed for local use on **Windows 10/11** with Python and
VS Code.

> **Note:** Webcam access, real mouse control, and Windows volume
> control must be tested on the local Windows machine. Running this
> project inside a hosted Replit workspace may not provide access to
> your computer's webcam, mouse, or system audio.

## Features

-   Real-time webcam input and hand-landmark detection.
-   Gesture recognition and finger-count mode.
-   Virtual mouse mode for cursor movement and pinch-click, if
    implemented and enabled in the current code.
-   Windows master-volume control using fingertip distance, if supported
    by the current build.
-   Keyboard-based mode selection.
-   Modular Python code for easier maintenance.

## Technology Stack

-   Python
-   OpenCV (`cv2`) for webcam frames and image processing
-   MediaPipe for hand tracking / gesture processing
-   PyAutoGUI for mouse control
-   Pycaw and `comtypes` for Windows volume control
-   NumPy for numerical operations

The exact dependencies and supported versions should be taken from the
project's `requirements.txt`. Keep package versions compatible with one
another, especially NumPy, MediaPipe, and OpenCV.

## Project Structure

The files in your local project may vary. A typical layout is:

``` text
HandGestureRecognition_Advanced/
├── main.py
├── hand_detector.py
├── control.py              # or controls.py, depending on your project
├── gesture_recognition.py  # if included
├── camera.py               # if included
├── dashboard.py            # if included
├── history.py              # if included
├── requirements.txt
├── README.md
└── .gitignore
```

Use the actual filenames in your project folder. Python import names and
filenames must match exactly.

## Requirements

-   Windows 10 or Windows 11
-   A working webcam
-   Python version compatible with the installed MediaPipe/OpenCV
    versions (Python 3.12 is used in the example commands below)
-   Git (optional, for GitHub)

## Setup on Windows

Open PowerShell in the project folder.

### 1. Create a virtual environment

If the project already has a `.venv312` environment, you can skip
creation.

``` powershell
py -3.12 -m venv .venv312
```

### 2. Activate it

``` powershell
.\.venv312\Scripts\Activate.ps1
```

If PowerShell blocks activation for the current terminal session, run:

``` powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv312\Scripts\Activate.ps1
```

### 3. Install dependencies

If the project includes `requirements.txt`:

``` powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If `requirements.txt` is missing, install only the packages required by
your source code and ensure the versions are compatible. Do not install
multiple OpenCV distributions (for example, `opencv-python` and
`opencv-contrib-python`) into the same environment unless the project
specifically requires and supports that setup.

### 4. Select the correct VS Code interpreter

1.  Open the project folder in VS Code.
2.  Press `Ctrl+Shift+P`.
3.  Choose **Python: Select Interpreter**.
4.  Select `.venv312\\Scripts\\python.exe`.
5.  If editor warnings remain, reload VS Code and inspect the Pylance
    output. An editor warning can be different from a runtime error.

### 5. Run the project

``` powershell
python main.py
```

Allow camera access if Windows asks for permission.

## Keyboard Controls

The current startup message reports these controls:

  Key   Mode / action
  ----- --------------------------
  `1`   Gesture recognition mode
  `2`   Mouse mode
  `3`   Volume control mode
  `H`   History
  `Q`   Quit

Verify these shortcuts against the current `main.py`, because they can
change between project versions.

## How to Use

1.  Connect a webcam and place your hand clearly inside the camera view.
2.  Run `python main.py`.
3.  Press `1` to test gesture recognition.
4.  Press `2` to test mouse mode. Start in a safe, uncluttered desktop
    area and ensure you can stop the application quickly.
5.  Press `3` to test volume control, if available.
6.  Press `H` to view history, if implemented.
7.  Press `Q` to exit.

## Troubleshooting

### `ModuleNotFoundError: No module named 'cv2'`

Install OpenCV in the active virtual environment and verify the
interpreter:

``` powershell
python -m pip install opencv-python
python -c "import cv2; print(cv2.__version__)"
```

### `ModuleNotFoundError: No module named 'mediapipe'`

``` powershell
python -m pip install mediapipe
```

If installation or imports fail, check that your Python version is
supported and that VS Code and the terminal use the same virtual
environment.

### NumPy / MediaPipe dependency conflict

Check the installed versions:

``` powershell
python -m pip show numpy mediapipe opencv-python opencv-contrib-python
python -m pip check
```

Use a compatible set of versions based on MediaPipe's requirements and
the project's dependency file. Do not blindly upgrade NumPy to the
latest version.

### Hand landmarks appear, but the mouse cursor does not move

-   Confirm that mouse mode is active (`2`, according to the current
    startup message).
-   Test PyAutoGUI separately:

``` powershell
python -c "import pyautogui; print(pyautogui.size()); pyautogui.moveTo(300,300,duration=1)"
```

-   If that test works, inspect the mouse-controller code: confirm it
    receives valid index-finger coordinates, converts camera coordinates
    to screen coordinates, and calls `pyautogui.moveTo()`.
-   Check whether a mouse-enable flag, pinch state, or exception is
    preventing movement.

### VS Code says `Import "cv2" could not be resolved`

If `python -c "import cv2"` succeeds in the project terminal, the
package is available to that Python environment. In VS Code, select the
same `.venv312` interpreter and restart Pylance. Do not repeatedly
reinstall OpenCV just to clear an editor warning.

### Webcam does not open

-   Close other applications that may be using the camera.
-   Check Windows camera privacy settings.
-   Confirm the camera index used in the source code.
-   Check the terminal for the actual error message.

### Volume control does not work

Windows volume control relies on Windows audio APIs and compatible
Pycaw/`comtypes` versions. Confirm the current implementation and run
the project on Windows.

## Safety Notes

-   Virtual mouse mode can click or interact with real applications.
    Test carefully and keep the quit shortcut available.
-   Do not run untrusted code with elevated administrator privileges.
-   Do not commit virtual environments, private credentials, `.env`
    files, or personal data to GitHub.

## GitHub Upload

Create a repository on GitHub, then run these commands from the project
folder (replace the URL with your repository URL):

``` powershell
git init
git add .
git status
git commit -m "Initial commit: Hand Gesture Recognition System"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/HandGestureRecognition-Advanced.git
git push -u origin main
```

Before `git add .`, ensure `.gitignore` excludes virtual environments
and generated files, for example:

``` gitignore
.venv/
.venv312/
__pycache__/
*.py[cod]
.env
```

If Git is already initialized, do not repeat `git init` unnecessarily.
If a remote already exists, inspect it with `git remote -v` before
adding another.

## Limitations and Future Improvements

Potential improvements include smoother cursor movement, calibration for
different camera positions, more robust gesture classification, better
error handling, automated tests, and packaging for easier installation.
Features should only be described as complete after they have been
verified in the actual running application.

## Acknowledgements

This project uses open-source Python computer-vision and automation
libraries, including OpenCV, MediaPipe, PyAutoGUI, and Pycaw.
