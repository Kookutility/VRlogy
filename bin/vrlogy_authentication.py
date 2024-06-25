from pathlib import Path
from tkinter import Tk, Canvas, Entry, PhotoImage, messagebox
import requests

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\VRlogy\Mediapipe-VR-Fullbody-Tracking\bin\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def display_message_box(title, message, type="info"):
    if type == "info":
        messagebox.showinfo(title, message)
    elif type == "error":
        messagebox.showerror(title, message)

def handle_login_response(response):
    if response.status_code == 200:
        return response.json()  # 성공적인 로그인 응답 처리
    elif response.status_code == 400:
        return "Bad Request: 요청이 잘못되었습니다."
    elif response.status_code == 401:
        return "Unauthorized: 인증에 실패했습니다. 사용자 이름 또는 비밀번호를 확인하세요."
    elif response.status_code == 403:
        return "Forbidden: 이 작업을 수행할 권한이 없습니다."
    elif response.status_code == 404:
        return "Not Found: 요청한 리소스를 찾을 수 없습니다."
    elif response.status_code == 415:
        return "Unsupported Media Type: 미디어 타입이 지원되지 않습니다."
    elif response.status_code == 500:
        return "Internal Server Error: 서버에서 오류가 발생했습니다."
    else:
        return f"Unexpected Error: HTTP {response.status_code}"

def login(username, password):
    url = "https://www.vrlogy.store/login"
    data = {
        "username": username,
        "password": password
    }
    response = requests.post(url, json=data)
    return handle_login_response(response)

def on_login_click(entry_1, entry_2):
    username = entry_1.get()
    password = entry_2.get()
    result = login(username, password)
    
    if isinstance(result, dict):  # 로그인 성공
        display_message_box("Success", "Login successful!")
        window.quit()
        return True  # 로그인 성공을 표시
    else:  # 로그인 실패
        display_message_box("Error", result, "error")
        entry_1.delete(0, 'end')
        entry_2.delete(0, 'end')
        return False  # 로그인 실패를 표시

def create_login_window():
    global window
    window = Tk()
    window.wm_iconbitmap(r'C:\VRlogy\Mediapipe-VR-Fullbody-Tracking\bin\assets\icon\VRlogy_icon.ico')
    window.geometry("534x392")
    window.configure(bg="#FFFFFF")
    window.title("VRlogy")
    
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

    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))

    button_1 = canvas.create_image(367.0, 352.0, image=button_image_1, anchor="center")
    button_2 = canvas.create_image(125.0, 352.0, image=button_image_2, anchor="center")

    canvas.tag_bind(button_1, "<Button-1>", lambda e: window.quit() if on_login_click(entry_1, entry_2) else None)
    canvas.tag_bind(button_2, "<Button-1>", lambda e: print("Button 2 clicked"))

    entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
    canvas.create_image(369.5, 217.0, image=entry_image_1)
    entry_1 = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        font=("SourceSansPro SemiBold", 15),
        insertbackground='#000000',
        justify="left"
    )
    entry_1.place(x=243.0, y=195.0, width=253.0, height=42.0)

    entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
    canvas.create_image(369.5, 281.0, image=entry_image_2)
    entry_2 = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        font=("SourceSansPro SemiBold", 15),
        show="*",
        insertbackground='#000000',
        justify="left"
    )
    entry_2.place(x=243.0, y=259.0, width=253.0, height=42.0)

    canvas.create_text(30.0, 202.0, anchor="nw", text="ID", fill="#E7EFFF", font=("SourceSansPro SemiBold", 22 * -1))
    canvas.create_text(30.0, 257.0, anchor="nw", text="PASSWORD", fill="#E7EFFF", font=("SourceSansPro SemiBold", 22 * -1))

    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    canvas.create_image(261.0, 95.0, image=image_image_2)

    window.resizable(False, False)
    window.mainloop()

def run_login_loop():
    login_success = False
    while not login_success:
        create_login_window()
        if "window" in globals():
            window.destroy()
            del window
        login_success = "window" not in globals()  # 로그인 성공 시 루프 종료