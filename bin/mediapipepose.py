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

sys.path.append(os.getcwd())  # 임베더블 파이썬이 로컬 모듈을 찾지 못하기 때문에 이 줄이 필요합니다.

from helpers import sendToSteamVR,CameraStream, shutdown, mediapipeTo3dpose, get_rot_mediapipe, get_rot_hands, draw_pose, keypoints_to_original, normalize_screen_coordinates, get_rot
from backends import DummyBackend, SteamVRBackend, VRChatOSCBackend
import webui
import parameters

class InferenceWindow(tk.Frame):
    def __init__(self, root, params, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        
        self.params = params
        params.gui = self       
        self.root = root

        # 이미지 회전 설정
        frame5 = tk.Frame(self.root)
        frame5.pack()
        self.change_image_rotation_frame(frame5)

        # 재조정
        tk.Button(self.root, text='재조정 (위 설정값을 자동으로 재조정)', 
                    command=self.autocalibrate).pack()

        # 종료 버튼
        tk.Button(self.root, text='종료', command=self.params.ready2exit).pack()

        # 비디오 피드
        self.video_label = tk.Label(self.root)
        self.video_label.pack()

        root.protocol("WM_DELETE_WINDOW", self.params.ready2exit) # X 버튼을 눌렀을 때

        # 비디오 업데이트 루프 시작
        self.update_video_feed()

    def change_image_rotation_frame(self, frame):
        rot_img_var = tk.IntVar(value=self.params.img_rot_dict_rev[self.params.rotate_image])
        tk.Label(frame, text="이미지 회전 시계방향:", width = 20).grid(row=0, column=0)
        tk.Radiobutton(frame, text="0", variable = rot_img_var, value = 0).grid(row=0, column=1)
        tk.Radiobutton(frame, text="90",  variable = rot_img_var, value = 1).grid(row=0, column=2)
        tk.Radiobutton(frame, text="180",  variable = rot_img_var, value = 2).grid(row=0, column=3)
        tk.Radiobutton(frame, text="270",  variable = rot_img_var, value = 3).grid(row=0, column=4)
        rot_img_var.trace_add('write', callback=lambda var, index, mode: self.params.change_img_rot(rot_img_var.get()))
        img_mirror_var = tk.BooleanVar(value=self.params.mirror)
        img_mirror_check = tk.Checkbutton(frame, text="미러", variable=img_mirror_var, command=lambda *args: self.params.change_mirror(bool(img_mirror_var.get())))
        img_mirror_check.grid(row=0, column=5)

    def autocalibrate(self):
        use_steamvr = True if self.params.backend == 1 else False

        if use_steamvr:
            array = sendToSteamVR("getdevicepose 0")       

            if array is None or len(array) < 10:
                shutdown(self.params)

            headsetpos = [float(array[3]),float(array[4]),float(array[5])]
            headsetrot = R.from_quat([float(array[7]),float(array[8]),float(array[9]),float(array[6])])
            
            neckoffset = headsetrot.apply(self.params.hmd_to_neck_offset)   
        if self.params.calib_tilt:
            try:
                feet_middle = (self.params.pose3d_og[0] + self.params.pose3d_og[5])/2
            except:
                print("INFO: No pose detected, try to autocalibrate again.")
                return
        
            print(feet_middle)
            value = np.arctan2(feet_middle[0],-feet_middle[1]) * 57.295779513
            print("INFO: Precalib z angle: ", value)
            self.params.rot_change_z(-value+180)
            for j in range(self.params.pose3d_og.shape[0]):
                self.params.pose3d_og[j] = self.params.global_rot_z.apply(self.params.pose3d_og[j])
            feet_middle = (self.params.pose3d_og[0] + self.params.pose3d_og[5])/2
            value = np.arctan2(feet_middle[0],-feet_middle[1]) * 57.295779513
            print("INFO: Postcalib z angle: ", value)
            value = np.arctan2(feet_middle[2],-feet_middle[1]) * 57.295779513
            print("INFO: Precalib x angle: ", value)
            self.params.rot_change_x(value+90)
            for j in range(self.params.pose3d_og.shape[0]):
                self.params.pose3d_og[j] = self.params.global_rot_x.apply(self.params.pose3d_og[j])
            feet_middle = (self.params.pose3d_og[0] + self.params.pose3d_og[5])/2
            value = np.arctan2(feet_middle[2],-feet_middle[1]) * 57.295779513
            print("INFO: Postcalib x angle: ", value)
        if use_steamvr and self.params.calib_rot:
            feet_rot = self.params.pose3d_og[0] - self.params.pose3d_og[5]
            value = np.arctan2(feet_rot[0],feet_rot[2])
            value_hmd = np.arctan2(headsetrot.as_matrix()[0][0],headsetrot.as_matrix()[2][0])
            print("INFO: Precalib y value: ", value * 57.295779513)
            print("INFO: hmd y value: ", value_hmd * 57.295779513)  
            value = value - value_hmd
            value = -value
            print("INFO: Calibrate to value:", value * 57.295779513)   
            self.params.rot_change_y(value * 57.295779513)

            for j in range(self.params.pose3d_og.shape[0]):
                self.params.pose3d_og[j] = self.params.global_rot_y.apply(self.params.pose3d_og[j])
            
            feet_rot = self.params.pose3d_og[0] - self.params.pose3d_og[5]
            value = np.arctan2(feet_rot[0],feet_rot[2])
            
            print("INFO: Postcalib y value: ", value * 57.295779513)

        if use_steamvr and self.params.calib_scale:
            skelSize = np.max(self.params.pose3d_og, axis=0)-np.min(self.params.pose3d_og, axis=0)
            self.params.posescale = headsetpos[1]/skelSize[1]

        self.params.recalibrate = False

    def update_video_feed(self):
        # 카메라 스레드가 다른 이미지를 캡처할 때까지 대기
        if not camera_thread.image_ready:     
            self.root.after(10, self.update_video_feed)
            return

        # 최신 프레임 가져오기
        img = camera_thread.image_from_thread.copy()
        camera_thread.image_ready = False
        
        # 필요한 경우 이미지 회전 및 미러
        if self.params.rotate_image is not None:       
            img = cv2.rotate(img, self.params.rotate_image)
            
        if self.params.mirror:
            img = cv2.flip(img,1)

        # 이미지가 최대 크기를 초과하면 크기 조정
        if max(img.shape) > self.params.maximgsize:        
            ratio = max(img.shape)/self.params.maximgsize
            img = cv2.resize(img, (int(img.shape[1]/ratio),int(img.shape[0]/ratio)))

        # Mediapipe로 이미지를 RGB로 변환 및 처리
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(img_rgb)
        
        if results.pose_world_landmarks:
            pose3d = mediapipeTo3dpose(results.pose_world_landmarks.landmark)
            pose3d[:,0] = -pose3d[:,0]
            pose3d[:,1] = -pose3d[:,1]
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

            backend.updatepose(self.params, pose3d, rots, hand_rots)

        # 포즈 랜드마크를 이미지에 그리기
        mp_drawing.draw_landmarks(img_rgb, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # PIL 이미지를 Tkinter로 변환하여 표시
        imgtk = ImageTk.PhotoImage(image=Image.fromarray(img_rgb))
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)

        self.root.after(10, self.update_video_feed)

def make_inference_gui(_params):
    root = tk.Tk()
    InferenceWindow(root, _params).pack(side="top", fill="both", expand=True)
    root.mainloop()

def main():
    global camera_thread, pose, mp_drawing, mp_pose, backend

    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    print("INFO: Reading parameters...")
    params = parameters.Parameters()

    if params.webui:
        webui_thread = threading.Thread(target=webui.start_webui, args=(params,), daemon=True)
        webui_thread.start()
    else:
        print("INFO: WebUI disabled in parameters")

    backends = { 0: DummyBackend, 1: SteamVRBackend, 2: VRChatOSCBackend }
    backend = backends[params.backend]()
    backend.connect(params)

    if params.exit_ready:
        sys.exit("INFO: Exiting... You can close the window after 10 seconds.")

    print("INFO: Opening camera...")
    camera_thread = CameraStream(params)

    print("INFO: Starting pose detector...")
    pose = mp_pose.Pose(model_complexity=params.model, 
                        min_detection_confidence=0.5, 
                        min_tracking_confidence=params.min_tracking_confidence, 
                        smooth_landmarks=params.smooth_landmarks, 
                        static_image_mode=params.static_image)

    make_inference_gui(params)

if __name__ == "__main__":
    main()
