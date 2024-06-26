from pathlib import Path
from tkinter import Tk, Canvas, Entry, PhotoImage, messagebox
import requests
import webbrowser
import os

# 현재 스크립트의 디렉토리 경로를 가져옴
script_dir = os.path.dirname(os.path.abspath(__file__))

# 아이콘 파일의 상대 경로 설정
icon_path = os.path.join(script_dir, 'assets', 'icon', 'VRlogy_icon.ico')

# 상대 경로 설정
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets/frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def display_message_box(title, message, type="info"):
    if type == "info":
        messagebox.showinfo(title, message)
    elif type == "error":
        messagebox.showerror(title, message)

def handle_login_response(response):
    try:
        response_data = response.json()
    except ValueError:
        return "Invalid response format", False

    if response.status_code == 200:
        if response_data.get("status") == "success":
            return response_data, True
        else:
            return response_data.get("message", "Login failed"), False
    elif response.status_code == 400:
        return "Bad Request: 요청이 잘못되었습니다.", False
    elif response.status_code == 401:
        return "Unauthorized: 인증에 실패했습니다. 사용자 이름 또는 비밀번호를 확인하세요.", False
    elif response.status_code == 403:
        return "Forbidden: 이 작업을 수행할 권한이 없습니다.", False
    elif response.status_code == 404:
        return "Not Found: 요청한 리소스를 찾을 수 없습니다.", False
    elif response.status_code == 415:
        return "Unsupported Media Type: 미디어 타입이 지원되지 않습니다.", False
    elif response.status_code == 500:
        return "Internal Server Error: 서버에서 오류가 발생했습니다.", False
    else:
        return f"Unexpected Error: HTTP {response.status_code}", False

def login(username, password):
    # POST 요청을 통해 로그인 시도
    login_url = "https://www.vrlogy.store/auth/login"
    token_url = "https://www.vrlogy.store/auth/csrf-token"
    
    session = requests.Session()
    
    # GET 요청을 통해 CSRF 토큰을 받아옴
    token_response = session.get(token_url)
    if token_response.status_code != 200:
        return "Failed to retrieve CSRF token", False
    
    token_data = token_response.json()
    xsrf_token = token_data.get("csrfToken")
    if not xsrf_token:
        return "CSRF token not found", False
    
    # CSRF 토큰을 헤더에 설정
    headers = {
        'X-XSRF-TOKEN': xsrf_token
    }
    
    # 로그인 정보
    data = {
        "username": username,
        "password": password
    }
    
    # POST 요청으로 로그인 시도
    response = session.post(login_url, json=data, headers=headers)
    return handle_login_response(response)

def on_login_click(entry_1, entry_2):
    username = entry_1.get()
    password = entry_2.get()
    result, success = login(username, password)
    
    if success:  # 로그인 성공
        global login_success
        login_success = True
        window.quit()
        display_message_box("Success", "Login successful!")
    else:  # 로그인 실패
        display_message_box("Error", result, "error")
        entry_1.delete(0, 'end')
        entry_2.delete(0, 'end')

def open_signup_url():
    webbrowser.open("https://www.vrlogy.store/signup")

def create_login_window():
    print("i'm login")
    global window
    window = Tk()
    window.wm_iconbitmap(icon_path)
    window.geometry("534x392+100+100")
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
    
    window.image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    canvas.create_image(267.0, 196.0, image=window.image_image_1)

    window.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    window.button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))

    button_1 = canvas.create_image(367.0, 352.0, image=window.button_image_1, anchor="center")
    button_2 = canvas.create_image(125.0, 352.0, image=window.button_image_2, anchor="center")

    canvas.tag_bind(button_1, "<Button-1>", lambda e: on_login_click(entry_1, entry_2))
    canvas.tag_bind(button_2, "<Button-1>", lambda e: open_signup_url())

    window.entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
    canvas.create_image(369.5, 217.0, image=window.entry_image_1)
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

    window.entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
    canvas.create_image(369.5, 281.0, image=window.entry_image_2)
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

    window.image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    canvas.create_image(261.0, 95.0, image=window.image_image_2)

    def on_closing():
        global login_success
        login_success = False
        window.quit()

    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.resizable(False, False)
    window.mainloop()

login_success = False

def run_login_loop():
    create_login_window()
    return login_success
