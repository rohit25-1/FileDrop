import os
import socket
import tqdm
import tkinter as tk
from tkinter import filedialog, messagebox, LabelFrame, CENTER, FLAT, ttk
import threading
import struct
import time
from pathlib import Path
import platform

button = "none"
location = ""
file_name = ""
file_size = 0
ctr = 1


def open_file():
    global button, location, file_name, file_size
    button = "opened"
    location = filedialog.askopenfilename()
    file_name = os.path.basename(location)
    if len(file_name) > 15:
        label_nameOffile["text"] = "File: " + file_name[:15] + ".."
    else:
        label_nameOffile["text"] = "File: " + file_name
    file_size = os.path.getsize(location)


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = "127.0.0.1"
    s.close()
    return local_ip


def get_broadcast_address():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    subnet_mask = socket.inet_ntoa(
        struct.pack(">I", (0xFFFFFFFF << (32 - 24)) & 0xFFFFFFFF)
    )

    # Calculate the broadcast address
    ip_parts = local_ip.split(".")
    mask_parts = subnet_mask.split(".")
    broadcast_parts = [
        str(int(ip_parts[i]) | (255 - int(mask_parts[i]))) for i in range(4)
    ]
    broadcast_address = ".".join(broadcast_parts)

    return broadcast_address


def broadcast_listener():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.bind(("", 37020))

    while True:
        data, addr = s.recvfrom(1024)
        if data.decode() == "DISCOVER_AIRDROP_SERVICES":
            response_message = "AIR_DROP_RECEIVER"
            s.sendto(response_message.encode(), addr)
            print(f"Responded to broadcast from {addr}")


def find_receivers():
    message = "DISCOVER_AIRDROP_SERVICES"
    broadcast_address = (get_broadcast_address(), 37020)
    timeout = 5

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.settimeout(timeout)

    print("Broadcasting to find receivers...")
    s.sendto(message.encode(), broadcast_address)

    start_time = time.time()
    receivers = []

    while True:
        if time.time() - start_time > timeout:
            break
        try:
            data, addr = s.recvfrom(1024)
            if data.decode() == "AIR_DROP_RECEIVER" and addr[0] != socket.gethostbyname(
                socket.gethostname()
            ):
                receivers.append(addr)
                print(f"Found receiver: {addr}")
        except socket.timeout:
            break

    s.close()
    return receivers


def send():
    global button, ctr
    if button != "opened" or file_name == "":
        messagebox.showinfo("my message", "Please Open A File To Transfer")
        return

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        local_ip = get_local_ip()

        s.bind((local_ip, 12345))
        print(s)
        print(local_ip)
        SEPARATOR = "<SEPARATOR>"
        s.listen(10)
        c, addr = s.accept()

        c.send(f"{file_name}{SEPARATOR}{file_size}".encode())
        progress_bar["value"] = 0
        progress_bar["maximum"] = file_size
        progress = tqdm.tqdm(
            range(file_size), f"Sending ", unit="B", unit_scale=True, unit_divisor=1024
        )
        f = open(location, "rb")
        datas = f.read(4096)
        while datas:
            c.send(datas)
            progress.update(len(datas))
            progress_bar["value"] += len(datas)
            window.update_idletasks()
            datas = f.read(4096)
        f.close()
        messagebox.showinfo("my message", "Done Transferring!")
        button = "none"
        c.close()
        s.close()
        ctr += 1

    except OSError as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        if s:
            s.close()


def get_downloads_folder():
    if os.name == "nt":
        downloads_path = Path.home() / "Downloads"
    else:
        downloads_path = Path.home() / "Downloads"

    return downloads_path


def receive():
    SEPARATOR = "<SEPARATOR>"
    receivers = find_receivers()
    if not receivers:
        messagebox.showinfo("my message", "No receivers found.")
        return

    receiver_ip, port = receivers[0]
    print(receiver_ip)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((receiver_ip, 12345))
    received = s.recv(4096).decode()
    filename, filesize = received.split(SEPARATOR)
    filesize = int(filesize)
    progress_bar["value"] = 0
    progress_bar["maximum"] = filesize
    progress = tqdm.tqdm(
        range(filesize), f"Receiving ", unit="B", unit_scale=True, unit_divisor=4096
    )
    downloads_folder = get_downloads_folder()
    name = downloads_folder / filename
    f = open(name, "wb")
    while True:
        datas = s.recv(4096)
        if not datas:
            break
        f.write(datas)
        progress.update(len(datas))
        progress_bar["value"] += len(datas)
        window.update_idletasks()
    f.close()
    messagebox.showinfo("my message", "Done Receiving!")
    s.close()


def run_send_thread():
    threading.Thread(target=send).start()


def run_receive_thread():
    threading.Thread(target=receive).start()


threading.Thread(target=broadcast_listener, daemon=True).start()

window = tk.Tk()
window.resizable(0, 0)
windowWidth = window.winfo_reqwidth()
windowHeight = window.winfo_reqheight()
positionRight = int(window.winfo_screenwidth() / 2 - windowWidth / 2)
positionDown = int(window.winfo_screenheight() / 2 - windowHeight / 2)
window.geometry("+{}+{}".format(positionRight, positionDown))
window.geometry("500x250")
window.title("Filedrop")

labelframe = LabelFrame(window, bd=0, height=400)
labelframe.pack(fill="both", expand="yes")
labelframe.place(relx=0.5, rely=0.5, anchor=CENTER)

label1 = tk.Label(labelframe, text="FileDrop", font=("Helvetica", 50), pady=5)
label1.pack()

label_nameOffile = tk.Label(labelframe, text="", font=("Helvetica", 15), fg="gray46")
label_nameOffile.pack()

labelframe2 = LabelFrame(labelframe, bd=0, height=10)
labelframe2.pack(fill="both", expand="no")
labelframe3 = LabelFrame(labelframe, bd=0, height=10)
labelframe3.pack(fill="both", expand="no")
labelframe4 = LabelFrame(labelframe, bd=0, height=10)
labelframe4.pack(fill="both", expand="no")


open_button = tk.Button(
    labelframe2, text="open", relief=FLAT, width=5, command=open_file
)
open_button.grid(row=0, column=1, pady=10)

send_button = tk.Button(
    labelframe2, text="send", relief=FLAT, width=5, command=run_send_thread
)
send_button.grid(row=0, column=3)

receive_button = tk.Button(
    labelframe3, text="receive", relief=FLAT, width=5, command=run_receive_thread
)
receive_button.grid(row=0, column=2)

progress_bar = ttk.Progressbar(
    labelframe4, orient="horizontal", length=200, mode="determinate"
)
progress_bar.pack(pady=20)

window.mainloop()
