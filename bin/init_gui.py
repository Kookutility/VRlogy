import tkinter as tk
from pathlib import Path
from tkinter import Tk, Canvas, PhotoImage, NW
import os
import pickle

# 현재 스크립트의 디렉토리 경로를 가져옴
script_dir = os.path.dirname(os.path.abspath(__file__))

# 아이콘 파일의 상대 경로 설정
icon_path = os.path.join(script_dir, 'assets', 'icon', 'VRlogy_icon.ico')

# 상대 경로 설정
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets/frame2")

def getparams():
    # 파라미터 파일 로드
    # 파일 실행 시 파라미터 값 확인 후 실행 설정
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
        "use_hands": True,
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

    # 카메라 선택 창 생성
    window = Tk()
    
    window.geometry("534x392+100+100")
    window.wm_iconbitmap(icon_path)
    window.configure(bg = "#FFFFFF")
    window.title("VRlogy")
    
    def set_camera(camid):
        param["camid"] = camid
        pickle.dump(param, open("params.p", "wb"))
        window.quit()

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    def on_button_click(button_id):
        if button_id == 1:
            set_camera("1")  # 웹캠
        elif button_id == 2:
            set_camera("http://192.168.1.103:8080/video")  # 임시 설정
        elif button_id == 3:
            set_camera("0")  # 내장 카메라(노트북)

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

    # 텍스트 대신 이미지 사용
    cam0_text_image = PhotoImage(
        file=relative_to_assets("cam0_text.png"))
    cam0_text = canvas.create_image(
        413.0,
        288.0,
        image=cam0_text_image,
        anchor="nw"
    )

    phone_cam_text_image = PhotoImage(
        file=relative_to_assets("phone_cam_text.png"))
    phone_cam_text = canvas.create_image(
        240.0,
        289.0,
        image=phone_cam_text_image,
        anchor="nw"
    )

    cam1_text_image = PhotoImage(
        file=relative_to_assets("cam1_text.png"))
    cam1_text = canvas.create_image(
        77.0,
        289.0,
        image=cam1_text_image,
        anchor="nw"
    )

    # 선택된 camid에 따라 빨간색 아이콘 표시
    red_sign_image = PhotoImage(
        file=relative_to_assets("red_sign.png"))

    if param.get("camid") == "0":
        canvas.create_image(
            396.0,
            288.0,
            image=red_sign_image,
            anchor="nw"
        )

    if param.get("camid") == "http://192.168.1.103:8080/video":
        canvas.create_image(
            229.0,
            289.0,
            image=red_sign_image,
            anchor="nw"
        )

    if param.get("camid") == "1":
        canvas.create_image(
            57.0,
            289.0,
            image=red_sign_image,
            anchor="nw"
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
        file=relative_to_assets("button_1.png"))
    button_3 = canvas.create_image(
        436.5,
        212.5,
        image=button_image_3
    )
    canvas.tag_bind(button_3, "<Button-1>", lambda e: on_button_click(3))

    # 이미지로 텍스트를 대체
    tracker_select_text_image = PhotoImage(
        file=relative_to_assets("tracker_select_text.png"))
    tracker_select_text = canvas.create_image(
        267.0,
        76.0,
        image=tracker_select_text_image
    )

    window.resizable(False, False)
    window.mainloop()
    window.destroy()

    return param

if __name__ == "__main__":
    # 파라미터 가져오기
    params = getparams()
    print("Parameters:", params)
