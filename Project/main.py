import subprocess
import pyttsx3

engine = pyttsx3.init()

face_python = r"C:\Users\DELL\Desktop\prmo\face_env\Scripts\python.exe"
sign_python = r"C:\Users\DELL\Desktop\prmo\mp_env\Scripts\python.exe"

face = subprocess.check_output([face_python, "face_system.py"], stderr=subprocess.DEVNULL).decode().strip()
sign = subprocess.check_output([sign_python, "sign_system.py"], stderr=subprocess.DEVNULL).decode().strip()

output = f"{face.replace('_',' ').title()} is in front of you and he is saying {sign}"

print(output)

engine.say(output)
engine.runAndWait()