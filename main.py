import os
import time
from PIL import ImageGrab
# import win32gui

path = './screenshots/'
if not os.path.exists(path):
    os.makedirs(path)


# date = os.popen("date/t").read().strip()
# hostname = os.popen("hostname").read().strip()
# print("Date: " + date)
# print("Hostname: " + hostname)

def screenshot(name, path=path):
    screenshot = ImageGrab.grab()  # Take the screenshot
    screenshot.save(path+f'{name}.png', 'PNG')  

os.system("start cmd /k \"hostname & date/t\"")
time.sleep(2)
import ctypes

kernel32 = ctypes.WinDLL('kernel32')
user32 = ctypes.WinDLL('user32')

SW_MAXIMIZE = 3

hWnd = kernel32.GetConsoleWindow()
print(hWnd)
user32.ShowWindow(hWnd, SW_MAXIMIZE)

# # import subprocess as sp
# # sp.Popen("start cmd /k date/t", shell=True)

# # 打開防毒軟體
# # os.popen(r"C:\Program Files (x86)\Notepad++\notepad++.exe")
# # os.popen(r"start /max cmd /k date/t")

# # https://dotblogs.com.tw/hung-chin/2011/01/14/20806
# # 螢幕保護裝置
# os.system("start rundll32.exe shell32.dll,Control_RunDLL desk.cpl,,1")
# # os.system("start rundll32.exe shell32.dll,Control_RunDLL mmsys.cpl,,0")
# # time.sleep(5)
# # output = os.popen("tasklist /M mmsys.cpl /FI \"IMAGENAME eq rundll32.exe\"").read()
# output = os.popen("tasklist /M desk.cpl /FI \"IMAGENAME eq rundll32.exe\"").read()
# print(output)
# pid = output.split("\n")[3].split()[1] if 'PID' in output else None
# # print(pid)
# # time.sleep(5)
# # screenshot("螢幕保護裝置")
# # print('kill ' + pid)
# # os.system(f'taskkill /F /PID {pid}')

# # 程式和功能
# # os.system("control appwiz.cpl")
# # os.system("control desk.cpl")
# # os.system("pause")





