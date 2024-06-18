from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button
from PIL import Image, ImageTk

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\kook\Desktop\build\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

login_info = []

def on_login_click(window, entry_1, entry_2, button_1):
    login_info.append(entry_1.get())  # Get text from entry_1
    login_info.append(entry_2.get())  # Get text from entry_2
    window.quit() 
    
def login():
    
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
    image_image_1 = ImageTk.PhotoImage(
        Image.open(relative_to_assets("image_1.png")).convert("RGBA"))
    canvas.create_image(
        267.0,
        196.0,
        image=image_image_1
    )

    button_image_1 = ImageTk.PhotoImage(
        Image.open(relative_to_assets("button_1.png")).convert("RGBA"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: on_login_click(window, entry_1, entry_2, button_1),  # Set command to on_login_click
        relief="flat",
        bg="#FFFFFF",
        activebackground="#FFFFFF"
    )
    button_1.place(
        x=235.0,
        y=308.0,
        width=269.0,
        height=48.0
    )

    button_image_2 = ImageTk.PhotoImage(
        Image.open(relative_to_assets("button_2.png")).convert("RGBA"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_2 clicked"),
        relief="flat",
        bg="#FFFFFF",
        activebackground="#FFFFFF"
    )
    button_2.place(
        x=30.0,
        y=308.0,
        width=190.0,
        height=48.0
    )

    entry_image_1 = ImageTk.PhotoImage(
        Image.open(relative_to_assets("entry_1.png")).convert("RGBA"))
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

    entry_image_2 = ImageTk.PhotoImage(
        Image.open(relative_to_assets("entry_2.png")).convert("RGBA"))
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

    image_image_2 = ImageTk.PhotoImage(
        Image.open(relative_to_assets("image_2.png")).convert("RGBA"))
    canvas.create_image(
        261.0,
        95.0,
        image=image_image_2
    )

    window.resizable(False, False)
    window.mainloop()
    window.destroy() 
    return login_info

