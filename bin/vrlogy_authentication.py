import tkinter as tk

def login():
    # 로그인 정보를 담을 리스트
    login_info = []

    # 로그인 창을 생성합니다.
    login_window = tk.Tk()
    login_window.title("Login")

    tk.Label(login_window, text="User ID:", width=50).pack()
    user_id_entry = tk.Entry(login_window, width=50)
    user_id_entry.pack()

    tk.Label(login_window, text="Password:", width=50).pack()
    user_password_entry = tk.Entry(login_window, width=50, show="*")
    user_password_entry.pack()

    def on_login_click():
        # 입력된 사용자 아이디와 비밀번호를 리스트에 저장합니다.
        login_info.append(user_id_entry.get())
        login_info.append(user_password_entry.get())
        login_window.quit()

    tk.Button(login_window, text='Login', command=on_login_click).pack()

    # 로그인 창을 실행합니다.
    login_window.mainloop()
    
    # 로그인 창을 파괴합니다.
    login_window.destroy()

    return login_info