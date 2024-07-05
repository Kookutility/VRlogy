import os
import cv2
import numpy as np
import tkinter as tk
from tkinter import Canvas, PhotoImage
from PIL import Image, ImageTk
from scipy.spatial.transform import Rotation as R
import mediapipe as mp
from pathlib import Path
import launch_setting_gui
from helpers import sendToSteamVR, shutdown, mediapipeTo3dpose, get_rot_mediapipe, get_rot_hands, get_rot
import os
import pickle
# 현재 스크립트의 디렉토리 경로를 가져옴
script_dir = os.path.dirname(os.path.abspath(__file__))

# 아이콘 파일의 상대 경로 설정
icon_path = os.path.join(script_dir, 'assets', 'icon', 'VRlogy_icon.ico')

# 상대 경로 설정
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets/frame4")

class InferenceWindow(tk.Frame):
    def __init__(self, root, params, camera_thread, backend, pose, mp_drawing, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)

        self.params = params
        self.camera_thread = camera_thread
        self.backend = backend
        self.pose = pose
        self.mp_drawing = mp_drawing
        params.gui = self       
        self.root = root
        
        self.root.wm_iconbitmap(icon_path)
        self.root.title("VRlogy")
        self.setup_gui()
        self.update_video_feed()
        self.schedule_autocalibrate()

    def setup_gui(self):
        def relative_to_assets(path: str) -> Path:
            return ASSETS_PATH / Path(path)

        def on_button_click(button_id):
            if button_id == 1:
                self.root.destroy()
                launch_setting_gui.make_gui(self.params)
            elif button_id == 3:
                self.params.change_mirror(not self.params.mirror)
            elif button_id == 4:
                self.params.img_rot_dict_rev[1]
                

        self.root.geometry("530x661+100+100")
        self.root.configure(bg="#FFFFFF")

        self.canvas = Canvas(
            self.root,
            bg="#FFFFFF",
            height=1000,
            width=1000,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
        self.canvas.create_image(265.0, 380.0, image=self.image_image_1)

        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        
        self.button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
        self.button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))

        button_1 = self.canvas.create_image(265, 611, image=self.button_image_1, anchor="center")
        self.canvas.tag_bind(button_1, "<Button-1>", lambda e: on_button_click(1))

        button_4 = self.canvas.create_image(68, 588, image=self.button_image_4, anchor="center")
        self.canvas.tag_bind(button_4, "<Button-1>", lambda e: on_button_click(4))

        button_3 = self.canvas.create_image(68, 548, image=self.button_image_3, anchor="center")
        self.canvas.tag_bind(button_3, "<Button-1>", lambda e: on_button_click(3))


        self.canvas_video = self.canvas.create_image(265.0, 280.0)

    def set_rotation(self, value):
        self.params.rotate_image = self.params.img_rot_dict_rev[value]
        self.params.change_img_rot(value)

    def schedule_autocalibrate(self):
        self.autocalibrate()
        self.root.after(1000, self.schedule_autocalibrate)  # 1초마다 자동 재추적

    def autocalibrate(self):
        use_steamvr = True if self.params.backend == 1 else False

        if use_steamvr:
            array = sendToSteamVR("getdevicepose 0")

            if array is None or len(array) < 10:
                shutdown(self.params)

            headsetpos = [float(array[3]), float(array[4]), float(array[5])]
            headsetrot = R.from_quat([float(array[7]), float(array[8]), float(array[9]), float(array[6])])

            neckoffset = headsetrot.apply(self.params.hmd_to_neck_offset)
        if self.params.calib_tilt:
            try:
                feet_middle = (self.params.pose3d_og[0] + self.params.pose3d_og[5]) / 2
            except:
                print("INFO: No pose detected, try to autocalibrate again.")
                return

            #print(feet_middle)
            value = np.arctan2(feet_middle[0], -feet_middle[1]) * 57.295779513
            #print("INFO: Precalib z angle: ", value)
            self.params.rot_change_z(-value + 180)
            for j in range(self.params.pose3d_og.shape[0]):
                self.params.pose3d_og[j] = self.params.global_rot_z.apply(self.params.pose3d_og[j])
            feet_middle = (self.params.pose3d_og[0] + self.params.pose3d_og[5]) / 2
            value = np.arctan2(feet_middle[0], -feet_middle[1]) * 57.295779513
            #print("INFO: Postcalib z angle: ", value)
            value = np.arctan2(feet_middle[2], -feet_middle[1]) * 57.295779513
            #print("INFO: Precalib x angle: ", value)
            self.params.rot_change_x(value + 90)
            for j in range(self.params.pose3d_og.shape[0]):
                self.params.pose3d_og[j] = self.params.global_rot_x.apply(self.params.pose3d_og[j])
            feet_middle = (self.params.pose3d_og[0] + self.params.pose3d_og[5]) / 2
            value = np.arctan2(feet_middle[2], -feet_middle[1]) * 57.295779513
            #print("INFO: Postcalib x angle: ", value)
        if use_steamvr and self.params.calib_rot:
            feet_rot = self.params.pose3d_og[0] - self.params.pose3d_og[5]
            value = np.arctan2(feet_rot[0], feet_rot[2])
            value_hmd = np.arctan2(headsetrot.as_matrix()[0][0], headsetrot.as_matrix()[2][0])
            #print("INFO: Precalib y value: ", value * 57.295779513)
            #print("INFO: hmd y value: ", value_hmd * 57.295779513)
            value = value - value_hmd
            value = -value
            #print("INFO: Calibrate to value:", value * 57.295779513)
            self.params.rot_change_y(value * 57.295779513)

            for j in range(self.params.pose3d_og.shape[0]):
                self.params.pose3d_og[j] = self.params.global_rot_y.apply(self.params.pose3d_og[j])

            feet_rot = self.params.pose3d_og[0] - self.params.pose3d_og[5]
            value = np.arctan2(feet_rot[0], feet_rot[2])

            #print("INFO: Postcalib y value: ", value * 57.295779513)

        if use_steamvr and self.params.calib_scale:
            skelSize = np.max(self.params.pose3d_og, axis=0) - np.min(self.params.pose3d_og, axis=0)
            self.params.posescale = headsetpos[1] / skelSize[1]

        self.params.recalibrate = False

    def update_video_feed(self):
        if not self.camera_thread.image_ready:
            self.root.after(10, self.update_video_feed)
            return

        img = self.camera_thread.image_from_thread.copy()
        param = pickle.load(open("params.p", "rb"))
        param_width = param.get("camera_width")
        param_height = param.get("camera_height")
        
        # 이미지의 width와 height를 param에서 가져온 값으로 리사이즈
        img = cv2.resize(img, (param_width, param_height))

        self.camera_thread.image_ready = False
        if self.params.rotate_image is not None:
            img = cv2.rotate(img, self.params.rotate_image)

        if self.params.mirror:
            img = cv2.flip(img, 1)
        
        if max(img.shape) > self.params.maximgsize:
            ratio = max(img.shape) / self.params.maximgsize
            img = cv2.resize(img, (int(img.shape[1] / ratio), int(img.shape[0] / ratio)))

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.pose.process(img_rgb)

        if results.pose_world_landmarks:
            pose3d = mediapipeTo3dpose(results.pose_world_landmarks.landmark)
            pose3d[:, 0] = -pose3d[:, 0]
            pose3d[:, 1] = -pose3d[:, 1]
            self.params.pose3d_og = pose3d.copy()

            for j in range(pose3d.shape[0]):
                pose3d[j] = self.params.global_rot_z.apply(pose3d[j])
                pose3d[j] = self.params.global_rot_x.apply(pose3d[j])
                pose3d[j] = self.params.global_rot_y.apply(pose3d[j])

            if not self.params.feet_rotation:
                rots = get_rot(pose3d)
            else:
                rots = get_rot_mediapipe(pose3d)

            if self.params.use_hands:
                hand_rots = get_rot_hands(pose3d)
            else:
                hand_rots = None

            self.backend.updatepose(self.params, pose3d, rots, hand_rots)

        self.mp_drawing.draw_landmarks(img_rgb, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)

        imgtk = ImageTk.PhotoImage(image=Image.fromarray(img_rgb))
        self.canvas.itemconfig(self.canvas_video, image=imgtk)
        self.canvas.image = imgtk  # GC로 인한 이미지 손실 방지

        self.root.after(10, self.update_video_feed)


    def exit_program(self):
        self.params.ready2exit()
        self.root.quit()
        self.root.destroy()
