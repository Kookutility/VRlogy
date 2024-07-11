import http.client
import json
import os
from pathlib import Path
from tkinter import Tk, Canvas, Text, PhotoImage, messagebox
import vrlogy
import launch_setting_gui  # Make sure this import is added to access make_gui
from http.cookies import SimpleCookie

LOGIN_INFO_PATH = Path(__file__).parent / "login_info.json"

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets/frame5")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def get_csrf_token(url, token_path):
    connection = http.client.HTTPSConnection(url)
    connection.request("GET", token_path)
    token_response = connection.getresponse()
    
    if token_response.status != 200:
        return None, "Failed to retrieve CSRF token"
    
    token_data = json.loads(token_response.read().decode())
    xsrf_token = token_data.get("csrfToken")
    if not xsrf_token:
        return None, "CSRF token not found"
    
    # 쿠키 설정
    cookie = SimpleCookie(token_response.getheader("Set-Cookie"))
    cookie_header = "; ".join([f"{key}={value.value}" for key, value in cookie.items()])
    
    connection.close()
    return xsrf_token, cookie_header

def send_bug_report(username, message):
    bug_report_url = "www.vrlogy.store"
    bug_report_path = "/report"
    token_path = "/auth/csrf-token"

    # CSRF 토큰 가져오기
    xsrf_token, cookie_header = get_csrf_token(bug_report_url, token_path)
    if not xsrf_token:
        return False, "CSRF token not found"

    connection = http.client.HTTPSConnection(bug_report_url)
    headers = {
        'Content-Type': 'application/json',
        'X-XSRF-TOKEN': xsrf_token,
        'Cookie': cookie_header
    }
    
    data = json.dumps({
        "username": username,
        "usermessage": message
    })
    
    connection.request("POST", bug_report_path, body=data, headers=headers)
    response = connection.getresponse()
    response_content = response.read().decode()
    connection.close()

    if response.status == 200:
        return True, "성공적으로 전송되었습니다."
    else:
        return False, f"버그 보고 전송에 실패했습니다: {response_content}"

def on_send_button_click(entry):
    if LOGIN_INFO_PATH.exists():
        with open(LOGIN_INFO_PATH, "r") as file:
            login_info = json.load(file)
            username = login_info.get("username")
            if username:
                user_message = entry.get("1.0", 'end-1c')
                success, message = send_bug_report(username, user_message)
                if success:
                    messagebox.showinfo("성공", message)
                else:
                    messagebox.showerror("실패", message)
            else:
                messagebox.showerror("오류", "로그인된 사용자가 없습니다.")
    else:
        messagebox.showerror("오류", "로그인된 사용자가 없습니다.")

def on_closing():
    if LOGIN_INFO_PATH.exists():
        with open(LOGIN_INFO_PATH, "w") as file:
            json.dump({}, file)
    window.destroy()

def go_back(self):
    self.root.destroy()
    vrlogy.main()

def create_bug_report_window():
    global window
    window = Tk()
    window.geometry("534x392")
    window.configure(bg="#FFFFFF")

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

    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    canvas.create_image(469.0, 30.0, image=image_image_2)

    entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
    canvas.create_image(265.5, 200.0, image=entry_image_1)
    
    entry_1 = Text(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    entry_1.place(
        x=87.0,
        y=90.0,
        width=357.0,
        height=218.0
    )

    image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
    canvas.create_image(267.0, 61.0, image=image_image_3)

    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1 = canvas.create_image(351.0, 354.0, image=button_image_1)

    button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
    button_2 = canvas.create_image(180.0, 354.0, image=button_image_2)

    def on_click(event, button_name):
        if button_name == "button_1":
            on_send_button_click(entry_1)
            window.destroy()
            launch_setting_gui.make_gui({})
        elif button_name == "button_2":
            window.destroy()
            launch_setting_gui.make_gui({})  # Pass appropriate parameters if needed

    canvas.tag_bind(button_1, "<Button-1>", lambda event: on_click(event, "button_1"))
    canvas.tag_bind(button_2, "<Button-1>", lambda event: on_click(event, "button_2"))

    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.resizable(False, False)
    window.mainloop()

if __name__ == "__main__":
    create_bug_report_window()
