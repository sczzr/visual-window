import os
import sys
import win32con
import win32gui


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("./icon"), relative_path)


class SysTrayIcon(object):
    QUIT = "QUIT"
    ID = 1234

    def __init__(self, icon):
        self.hwnd = None
        self.notify_id = None
        self.icon = icon

        message_map = {
            win32con.WM_DESTROY: self.destroy,
            win32con.WM_USER + 20: self.notify
        }

        wc = win32gui.WNDCLASS()
        wc.hInstance = win32gui.GetModuleHandle(None)
        wc.lpszClassName = "PythonTaskbar"
        wc.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW
        wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
        wc.hbrBackground = win32con.COLOR_WINDOW
        wc.lpfnWndProc = message_map
        self.classAtom = win32gui.RegisterClass(wc)

    def active(self):
        h_inst = win32gui.GetModuleHandle(None)
        self.hwnd = win32gui.CreateWindow(self.classAtom,
                                          "Taskbar",
                                          win32con.WS_OVERLAPPED | win32con.WS_SYSMENU,
                                          0, 0,
                                          win32con.CW_USEDEFAULT,
                                          win32con.CW_USEDEFAULT,
                                          0, 0, h_inst, None)
        win32gui.UpdateWindow(self.hwnd)
        self.notify_id = None
        self.refresh(icon=self.icon)

    def refresh(self, icon, time=200):
        h_inst = win32gui.GetModuleHandle(None)
        icon = resource_path(icon)
        try:
            hicon = win32gui.LoadImage(h_inst, icon, win32con.IMAGE_ICON, 0, 0,
                                       win32con.LR_LOADFROMFILE | win32con.IMAGE_ICON)
        except BaseException as e:
            hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
        if self.notify_id:
            message = win32gui.NIM_MODIFY
        else:
            message = win32gui.NIM_ADD

        self.notify_id = (self.hwnd, 0,
                          win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP | win32gui.NIF_INFO,
                          win32con.WM_USER + 20, hicon)
        win32gui.Shell_NotifyIcon(message, self.notify_id)

    def notify(self, hwnd, msg, wparam, lparam):
        pass

    def destroy(self):
        nid = (self.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        win32gui.PostQuitMessage(0)
