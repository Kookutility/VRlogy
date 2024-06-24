import os
import sys
import time
import threading
import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from scipy.spatial.transform import Rotation as R
import mediapipe as mp
import pickle
from tkinter import messagebox
sys.path.append(os.getcwd())

from helpers import sendToSteamVR, CameraStream, shutdown, mediapipeTo3dpose, get_rot_mediapipe, get_rot_hands, draw_pose, keypoints_to_original, normalize_screen_coordinates, get_rot
from backends import DummyBackend, SteamVRBackend, VRChatOSCBackend
import webui
import parameters
import vrlogy_authentication
import gui3
from tracking import InferenceWindow  # 추가된 부분

#gui3.py는 steamVR연결 설정 페이지, 이름변경 예정

class InitialWindow(tk.Frame):
    def __init__(self, root, params, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.params = params
        self.root = root
        self.root.wm_iconbitmap(r'C:\VRlogy\Mediapipe-VR-Fullbody-Tracking\bin\assets\icon\VRlogy_icon.ico')
        self.root.title("VRlogy")
        
    def connect_steamvr(self):
        global backend, camera_thread, pose, mp_drawing, mp_pose
        mp_pose = mp.solutions.pose
        mp_drawing = mp.solutions.drawing_utils
        try:
            backends = {0: DummyBackend, 1: SteamVRBackend, 2: VRChatOSCBackend}
            backend = backends[self.params.backend]()
            connection_result = backend.connect(self.params)

            if connection_result == "steamVR과 연결에 실패하였습니다. 재연결 후 다시 시도해주세요":
                messagebox.showerror("Connection Error", connection_result)
                self.root.destroy()
                gui3.make_gui(self.params)
                return
        except Exception as e:
            print(f"ERROR: {e}")
            messagebox.showerror("SteamVR Error", "steamVR과 연결에 실패하였습니다. 재연결 후 다시 시도해주세요")
            self.root.destroy()
            gui3.make_gui(self.params)
            return

        try:
            print("INFO: Opening camera...")
            camera_thread = CameraStream(self.params)

            print("INFO: Starting pose detector...")
            pose = mp_pose.Pose(model_complexity=self.params.model,
                                min_detection_confidence=0.5,
                                min_tracking_confidence=self.params.min_tracking_confidence,
                                smooth_landmarks=self.params.smooth_landmarks,
                                static_image_mode=self.params.static_image)

            self.root.destroy()
            make_inference_gui(self.params, camera_thread, backend, pose, mp_drawing)
        except (ValueError, ConnectionError) as e:
            print(f"ERROR: {e}")
            self.root.destroy()
            main()

    def open_settings(self):
        self.root.destroy()
        root = tk.Tk()
        SettingsWindow(root, self.params).pack(side="top", fill="both", expand=True)
        root.mainloop()

    def go_back(self):
        self.root.destroy()
        main()

class SettingsWindow(tk.Frame):
    def __init__(self, root, params, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.params = params
        self.root = root

        param = pickle.load(open("params.p", "rb"))

        # Camera width
        tk.Label(self, text="Camera width:", width=50).pack()
        self.camwidth = tk.Entry(self, width=20)
        self.camwidth.pack()
        self.camwidth.insert(0, param["camera_width"])

        # Camera height
        tk.Label(self, text="Camera height:", width=50).pack()
        self.camheight = tk.Entry(self, width=20)
        self.camheight.pack()
        self.camheight.insert(0, param["camera_height"])

        # Use hands
        self.varhand = tk.IntVar(value=param["use_hands"])
        self.hand_check = tk.Checkbutton(self, text="Spawn trackers for hands", variable=self.varhand)
        self.hand_check.pack()

        # Save button
        tk.Button(self, text='Save', command=self.save_params).pack()

        tk.Button(self.root, text='뒤로가기', command=self.go_back).pack()

    def save_params(self):
        # Create a dictionary to store the parameters
        updated_params = {
            "camera_width": int(self.camwidth.get()),
            "camera_height": int(self.camheight.get()),
            "use_hands": self.varhand.get()
        }

        # Save parameters
        pickle.dump(updated_params, open("params.p", "wb"))
        self.root.destroy()
        gui3.make_gui(self.params)

    def go_back(self):
        self.root.destroy()
        gui3.make_gui(self.params)

def make_initial_gui(_params):
    root = tk.Tk()
    InitialWindow(root, _params).pack(side="top", fill="both", expand=True)
    root.mainloop()

def make_inference_gui(_params, camera_thread, backend, pose, mp_drawing):
    root = tk.Tk()
    InferenceWindow(root, _params, camera_thread, backend, pose, mp_drawing).pack(side="top", fill="both", expand=True)
    root.mainloop()

def main():
    print("INFO: Reading parameters...")
    params = parameters.Parameters()

    if params.webui:
        webui_thread = threading.Thread(target=webui.start_webui, args=(params,), daemon=True)
        webui_thread.start()
    else:
        print("INFO: WebUI disabled in parameters")

    gui3.make_gui(params)

if __name__ == "__main__": 
    vrlogy_authentication.login()
    main()
