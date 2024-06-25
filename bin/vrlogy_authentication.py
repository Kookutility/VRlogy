from pathlib import Path
from tkinter import Tk, Canvas, Entry, PhotoImage

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\VRlogy\Mediapipe-VR-Fullbody-Tracking\bin\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

login_info = []

def on_login_click(entry_1, entry_2):
    login_info.append(entry_1.get())  # Get text from entry_1
    login_info.append(entry_2.get())  # Get text from entry_2
    window.quit()

def login():
    global window  # Make window global so we can close it in on_login_click
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
    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    canvas.create_image(
        267.0,
        196.0,
        image=image_image_1
    )

    # Load button images
    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))

    # Create image buttons on canvas with adjusted height
    button_1 = canvas.create_image(367.0, 352.0, image=button_image_1, anchor="center")  # Adjusted y-coordinate
    button_2 = canvas.create_image(125.0, 352.0, image=button_image_2, anchor="center")  # Adjusted y-coordinate

    # Bind the image buttons to click events
    canvas.tag_bind(button_1, "<Button-1>", lambda e: on_login_click(entry_1, entry_2))
    canvas.tag_bind(button_2, "<Button-1>", lambda e: print("Button 2 clicked"))

    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    canvas.create_image(
        369.5,
        217.0,  # Adjusted y coordinate
        image=entry_image_1
    )
    entry_1 = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        font=("SourceSansPro SemiBold", 15),  # Adjust font size and weight
        insertbackground='#000000',
        justify="left"
    )
    entry_1.place(
        x=243.0,
        y=195.0,  # Adjusted y coordinate
        width=253.0,
        height=42.0
    )

    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    canvas.create_image(
        369.5,
        281.0,  # Adjusted y coordinate
        image=entry_image_2
    )
    entry_2 = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        font=("SourceSansPro SemiBold", 15),  # Adjust font size and weight
        show="*",  # Hide password characters
        insertbackground='#000000',
        justify="left"
    )
    entry_2.place(
        x=243.0,
        y=259.0,  # Adjusted y coordinate
        width=253.0,
        height=42.0
    )

    canvas.create_text(
        30.0,
        202.0,  # Adjusted y coordinate
        anchor="nw",
        text="ID",
        fill="#E7EFFF",
        font=("SourceSansPro SemiBold", 22 * -1)
    )

    canvas.create_text(
        30.0,
        257.0,  # Adjusted y coordinate
        anchor="nw",
        text="PASSWORD",
        fill="#E7EFFF",
        font=("SourceSansPro SemiBold", 22 * -1)
    )

    image_image_2 = PhotoImage(
        file=relative_to_assets("image_2.png"))
    canvas.create_image(
        261.0,
        95.0,
        image=image_image_2
    )

    window.resizable(False, False)
    window.mainloop()
    window.destroy()
    return login_info


