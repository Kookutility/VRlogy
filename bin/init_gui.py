import tkinter as tk
import sys
import pickle
from sys import platform

def set_advanced(window, param):
    param["switch_advanced"] = True
    window.quit()

def getparams():
    try:
        param = pickle.load(open("params.p", "rb"))
        if not isinstance(param, dict):
            raise ValueError("Loaded parameter is not a dictionary.")
    except (FileNotFoundError, ValueError):
        param = {}

    param_defaults = {
        "camid" : "0",
        "imgsize": 640,
        "neckoffset": [0.0, -0.2, 0.1],
        "prevskel": False,
        "waithmd": False,
        "rotateclock": False,
        "rotatecclock": False,
        "rotate": None,
        "camlatency": 0.05,
        "smooth": 0.5,
        "feetrot": False,
        "calib_scale": True,
        "calib_tilt": True,
        "calib_rot": True,
        "use_hands": False,
        "ignore_hip": False,
        "camera_settings": False,
        "camera_width": 640,
        "camera_height": 480,
        "model_complexity": 1,
        "smooth_landmarks": True,
        "min_tracking_confidence": 0.5,
        "static_image": False,
        "backend": 1,
        "backend_ip": "127.0.0.1",
        "backend_port": 9000,
        "advanced": False,
        "webui": False
    }

    for key, value in param_defaults.items():
        if key not in param:
            param[key] = value

    window = tk.Tk()

    def on_close():
        window.destroy()
        sys.exit("INFO: Exiting... You can close the window after 10 seconds.")

    window.protocol("WM_DELETE_WINDOW", on_close)

    tk.Label(text="User ID:", width=50).pack()
    user_id = tk.Entry(width=50)
    user_id.pack()

    tk.Label(text="Password:", width=50).pack()
    user_password = tk.Entry(width=50, show="*")
    user_password.pack()
    
    def on_button_click():
        open_camera_selection()
        window.withdraw()

    def open_camera_selection():
        login_window = tk.Toplevel(window)
        login_window.title("Select Camera Type")

        tk.Label(login_window, text="VR 트래커가 실행될 환경을 선택해주세요!", width=50).pack()
        

        def set_camera(camid):
            param["camid"] = camid
            login_window.destroy()
            window.destroy()
            pickle.dump(param, open("params.p", "wb"))
            save_and_continue()

        tk.Button(login_window, text="Webcam", command=lambda: set_camera("1")).pack()
        tk.Button(login_window, text="Phonecam", command=lambda: set_camera("http://192.168.1.103:8080/video")).pack()
        tk.Button(login_window, text="Labtopcam", command=lambda: set_camera("0")).pack()
    tk.Button(text='Login', command=on_button_click).pack()

    def save_and_continue():
        param["user_id"] = user_id.get()
        param["user_password"] = user_password.get()
        param["switch_advanced"] = False

        pickle.dump(param, open("params.p", "wb"))
        window.quit()


    window.mainloop()

    return param

if __name__ == "__main__":
    print(getparams())
