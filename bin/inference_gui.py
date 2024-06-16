import tkinter as tk
from tkinter import ttk
import numpy as np
from scipy.spatial.transform import Rotation as R
from helpers import shutdown, sendToSteamVR

class InferenceWindow(tk.Frame):
    def __init__(self, root, params, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        
        self.params = params
        params.gui = self       
        self.root = root

        # Image rotation clockwise
        frame5 = tk.Frame(self.root)
        frame5.pack()
        self.change_image_rotation_frame(frame5)

        # recalibrate
        tk.Button(self.root, text='Recalibrate (automatically recalibrates checked values above)', 
                    command=self.autocalibrate).pack()

        # exit
        tk.Button(self.root, text='Press to exit', command=self.params.ready2exit).pack()

        root.protocol("WM_DELETE_WINDOW", self.params.ready2exit) # when press x
    
    def change_image_rotation_frame(self, frame):
        rot_img_var = tk.IntVar(value=self.params.img_rot_dict_rev[self.params.rotate_image])
        tk.Label(frame, text="Image rotation clockwise:", width = 20).grid(row=0, column=0)
        tk.Radiobutton(frame, text="0", variable = rot_img_var, value = 0).grid(row=0, column=1)
        tk.Radiobutton(frame, text="90",  variable = rot_img_var, value = 1).grid(row=0, column=2)
        tk.Radiobutton(frame, text="180",  variable = rot_img_var, value = 2).grid(row=0, column=3)
        tk.Radiobutton(frame, text="270",  variable = rot_img_var, value = 3).grid(row=0, column=4)
        rot_img_var.trace_add('write', callback=lambda var, index, mode: self.params.change_img_rot(rot_img_var.get()))
        img_mirror_var = tk.BooleanVar(value=self.params.mirror)
        img_mirror_check = tk.Checkbutton(frame, text="Mirror", variable=img_mirror_var, command=lambda *args: self.params.change_mirror(bool(img_mirror_var.get())))
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

def make_inference_gui(_params):
    root = tk.Tk()
    InferenceWindow(root, _params).pack(side="top", fill="both", expand=True)
    root.mainloop()

if __name__ == "__main__":
    print("hehe")
