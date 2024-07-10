from pathlib import Path
from tkinter import *

import os
import pickle
# 현재 스크립트의 디렉토리 경로를 가져옴
script_dir = os.path.dirname(os.path.abspath(__file__))
import vrlogy
# 아이콘 파일의 상대 경로 설정
icon_path = os.path.join(script_dir, 'assets', 'icon', 'VRlogy_icon.ico')

# 상대 경로 설정
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets/frame3")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

    return {}
def on_click(event, button_name, instance):
    if button_name == "button_1":
        instance.connect_steamvr()
    elif button_name == "button_2":
        instance.open_settings()
    elif button_name == "button_3":
        instance.go_back()

def make_gui(params):

    window = Tk()
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
        50.0,
        80.0,
        anchor="nw",
        text="헤드셋을 착용후 steamVR을 실행해주세요!",
        fill="#E7EFFF",
        font=("SourceSansPro SemiBold", 23 * -1)
    )

    canvas.create_text(
        387.0,
        287.0,
        anchor="nw",
        text="VR 트래커 실행",
        fill="#E7EFFF",
        font=("SourceSansPro SemiBold", 15 * -1)
    )

    canvas.create_text(
        75.0,
        287.0,
        anchor="nw",
        text="뒤로가기",
        fill="#E7EFFF",
        font=("SourceSansPro SemiBold", 15 * -1)
    )

    canvas.create_text(
        258.0,
        287.0,
        anchor="nw",
        text="설정",
        fill="#E7EFFF",
        font=("SourceSansPro SemiBold", 15 * -1)
    )
    window.title("VRlogy")
    window.wm_iconbitmap(icon_path)
    window.geometry("534x392+100+100")
    window.configure(bg="#FFFFFF")
    # Load button images
    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
    button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))

    # Create buttons as canvas images
    button_1 = canvas.create_image(
        436.5, 212.5,
        image=button_image_1
    )

    button_2 = canvas.create_image(
        269.5, 212.5,
        image=button_image_2
    )

    button_3 = canvas.create_image(
        100.5, 212.5,
        image=button_image_3
    )

    # InitialWindow 인스턴스를 생성합니다
    instance = vrlogy.InitialWindow(window, params)

    # 인스턴스를 on_click 함수에 전달하여 버튼 이벤트와 바인딩합니다
    canvas.tag_bind(button_1, "<Button-1>", lambda event: on_click(event, "button_1", instance))
    canvas.tag_bind(button_2, "<Button-1>", lambda event: on_click(event, "button_2", instance))
    canvas.tag_bind(button_3, "<Button-1>", lambda event: on_click(event, "button_3", instance))

    window.resizable(False, False)
    window.mainloop()
