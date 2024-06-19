import tkinter as tk
from pathlib import Path
from tkinter import Tk, Canvas, PhotoImage, NW
import pickle

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
    window = Tk()
    window.geometry("534x392")
    window.configure(bg = "#FFFFFF")
    window.title("Select Camera Type")

    def set_camera(camid):
        param["camid"] = camid
        pickle.dump(param, open("params.p", "wb"))
        window.quit()

    # 새로운 프론트엔드 코드
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\VRlogy\Mediapipe-VR-Fullbody-Tracking\bin\assets\frame2")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    def on_button_click(button_id):
        if button_id == 1:
            set_camera("1")  # Webcam
        elif button_id == 2:
            set_camera("http://192.168.1.103:8080/video")  # Phonecam
        elif button_id == 3:
            set_camera("0")  # Labtopcam

    canvas = Canvas(
        window,
        bg = "#FFFFFF",
        height = 392,
        width = 534,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        267.0,
        196.0,
        image=image_image_1
    )

    canvas.create_text(
        42.0,
        289.0,
        anchor="nw",
        text="WEBCAM\n",
        fill="#FFFFFF",
        font=("Roboto", 10, "normal")
    )

    canvas.create_text(
        214.0,
        289.0,
        anchor="nw",
        text="PHONE\nCAMERA",
        fill="#FFFFFF",
        font=("Roboto", 10, "normal")
    )

    canvas.create_text(
        381.0,
        288.0,
        anchor="nw",
        text="INNER\n(LABTOP)",
        fill="#FFFFFF",
        font=("Roboto", 10, "normal")
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = canvas.create_image(
        97.5,
        212.5,
        image=button_image_1
    )
    canvas.tag_bind(button_1, "<Button-1>", lambda e: on_button_click(1))

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = canvas.create_image(
        269.5,
        212.5,
        image=button_image_2
    )
    canvas.tag_bind(button_2, "<Button-1>", lambda e: on_button_click(2))

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    button_3 = canvas.create_image(
        436.5,
        212.5,
        image=button_image_3
    )
    canvas.tag_bind(button_3, "<Button-1>", lambda e: on_button_click(3))

    canvas.create_text(
        30.0,
        76.0,
        anchor="nw",
        text="VRlogy 트래커를 사용할 환경을 선택해주세요!",
        fill="#E7EFFF",
        font=("SourceSansPro", 17, "normal")
    )

    window.resizable(False, False)
    window.mainloop()
    window.destroy()

    return param

if __name__ == "__main__":
    # 파라미터를 가져옵니다.
    params = getparams()
    print("Parameters:", params)
