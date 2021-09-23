import win32con, win32gui, win32gui_struct


class window_tray_icon(object):
    QUIT = "QUIT"
    ID = 1234

    def __init__(self, icon, hover_text, menu_options, on_quit=None):
        self.icon = icon
        self.hover_text = hover_text
        self.on_quit = on_quit

        menu_options = menu_options + (("exit", None, self.QUIT),)

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
        hinst = win32gui.GetModuleHandle(None)
        self.hwnd = win32gui.CreateWindow(self.classAtom,
                                          "Taskbar",
                                          win32con.WS_OVERLAPPED | win32con.WS_SYSMENU,
                                          0, 0,
                                          win32con.CW_USEDEFAULT,
                                          win32con.CW_USEDEFAULT,
                                          0, 0, hinst, None)
        win32gui.UpdateWindow(self.hwnd)
        self.notify_id = None
        self.refresh(icon=self.icon, title="app start", msg="open")

    def refresh(self, icon, title, msg, time=200):
        hinst = win32gui.GetModuleHandle(None)

        try:
            hicon = win32gui.LoadImage(hinst, icon, win32con.IMAGE_ICON, 0, 0,
                                       win32con.LR_LOADFROMFILE | win32con.IMAGE_ICON)
        except:
            hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)

        if self.notify_id:
            message = win32gui.NIM_MODIFY
        else:
            message = win32gui.NIM_ADD

        self.notify_id = (self.hwnd, 0,
                          win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP | win32gui.NIF_INFO,
                          win32con.WM_USER + 20, hicon, self.hover_text)
        win32gui.Shell_NotifyIcon(message, self.notify_id)

    def add_tary_icon(self):
        iconPathName = "VisualDesktop.ico"
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        try:
            hicon = win32gui.LoadImage(self.hinst, iconPathName, win32con.IMAGE_ICON, 0, 0, icon_flags)
        except:
            hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)

        flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP

        nid = (self.hwnd, 0, flags, win32con.WM_USER + 20, hicon, "tooltip")
        win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)

    def notify(self, hwnd, msg, wparam, lparam):
        pass

    def show(self, title, msg):
        win32gui.UpdateWindow(self.hwnd)
        iconPathName = "VisualDesktop.ico"
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        try:
            hicon = win32gui.LoadImage(self.hinst, iconPathName, win32con.IMAGE_ICON, 0, 0, icon_flags)
        except:
            hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
        flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP
        nid = (self.hwnd, 0, flags, win32con.WM_USER + 20, hicon, "tooltip")
        win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)
        nid = (self.hwnd, 0, win32gui.NIF_INFO, win32con.WM_USER + 20, hicon,
               "ballon tooltip", msg, 200, title)
        win32gui.Shell_NotifyIcon(win32gui.NIM_MODIFY, nid)

    def destroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        win32gui.PostQuitMessage(0)
