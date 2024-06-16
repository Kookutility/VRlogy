import tkinter as tk
import sys
import pickle
from sys import platform



def getparams():
    # 파라미터 파일을 로드하거나 기본값을 설정합니다.
    try:
        param = pickle.load(open("params.p", "rb"))
        if not isinstance(param, dict):
            raise ValueError("Loaded parameter is not a dictionary.")
    except (FileNotFoundError, ValueError):
        param = {}

    param_defaults = {
        "camid": "0",
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

    # 카메라 선택 창을 생성합니다.
    window = tk.Tk()
    window.title("Select Camera Type")

    tk.Label(window, text="VR 트래커가 실행될 환경을 선택해주세요!", width=50).pack()
    
    def set_camera(camid):
        param["camid"] = camid
        pickle.dump(param, open("params.p", "wb"))
        window.quit()

    tk.Button(window, text="Webcam", command=lambda: set_camera("1")).pack()
    tk.Button(window, text="Phonecam", command=lambda: set_camera("http://192.168.1.103:8080/video")).pack()
    tk.Button(window, text="Labtopcam", command=lambda: set_camera("0")).pack()

    # 카메라 선택 창을 실행합니다.
    window.mainloop()
    
    # 카메라 선택 창을 파괴합니다.
    window.destroy()

    return param

if __name__ == "__main__":
    # 파라미터를 가져옵니다.
    params = getparams()
    print("Parameters:", params)