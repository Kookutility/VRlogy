from pathlib import Path
from tkinter import *

import os
import pickle
# 현재 스크립트의 디렉토리 경로를 가져옴
script_dir = os.path.dirname(os.path.abspath(__file__))
import vrlogy
import bug_report_gui
# 아이콘 파일의 상대 경로 설정
icon_path = os.path.join(script_dir, 'assets', 'icon', 'VRlogy_icon.ico')

# 상대 경로 설정
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets/frame3")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def make_gui(params):
    window = Tk()
    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=392,
        width=534,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)

    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    canvas.create_image(267.0, 196.0, image=image_image_1)

    launch_steamvr_text_image = PhotoImage(file=relative_to_assets("Launch_steamvr_text.png"))
    canvas.create_image(33.0, 80.0, image=launch_steamvr_text_image, anchor="nw")

    launch_text_image = PhotoImage(file=relative_to_assets("launch_text.png"))
    canvas.create_image(393.0, 287.0, image=launch_text_image, anchor="nw")

    back_text_image = PhotoImage(file=relative_to_assets("back_text.png"))
    canvas.create_image(75.0, 287.0, image=back_text_image, anchor="nw")

    customer_center_text_image = PhotoImage(file=relative_to_assets("customer_center_text.png"))
    canvas.create_image(245.0, 287.0, image=customer_center_text_image, anchor="nw")

    window.title("VRlogy")
    window.wm_iconbitmap(icon_path)
    window.geometry("534x392+100+100")
    window.configure(bg="#FFFFFF")

    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
    button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))

    button_1 = canvas.create_image(436.5, 212.5, image=button_image_1)
    button_2 = canvas.create_image(269.5, 212.5, image=button_image_2)
    button_3 = canvas.create_image(100.5, 212.5, image=button_image_3)

    def on_click(event, button_name, instance):
        if button_name == "button_1":
            instance.connect_steamvr()
        elif button_name == "button_2":
            window.destroy()
            bug_report_gui.create_bug_report_window()
        elif button_name == "button_3":
            instance.go_back()

    instance = vrlogy.InitialWindow(window, params)
    canvas.tag_bind(button_1, "<Button-1>", lambda event: on_click(event, "button_1", instance))
    canvas.tag_bind(button_2, "<Button-1>", lambda event: on_click(event, "button_2", instance))
    canvas.tag_bind(button_3, "<Button-1>", lambda event: on_click(event, "button_3", instance))

    window.resizable(False, False)
    window.mainloop()