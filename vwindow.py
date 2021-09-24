#!/usr/bin/python3

import win32con, win32gui
import keyboard as kb
import taskbar as tb
import time


def is_real_window(hwnd):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) \
            and win32gui.IsWindowVisible(hwnd):
        lExStyle = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        return not (lExStyle & win32con.WS_EX_TOOLWINDOW)


class VWindow(object):

    def __init__(self):
        self.hwnd = dict()

    def find_all_child(self):
        def get_all_hwnd(hwnd, mouse):
            if is_real_window(hwnd):
                self.hwnd.update({hwnd: win32gui.GetWindowText(hwnd)})

        win32gui.EnumWindows(get_all_hwnd, 0)

    def hide_visual_window(self):
        self.find_all_child()
        for h, t in self.hwnd.items():
            win32gui.ShowWindow(h, win32con.SW_HIDE)

    def show_visual_window(self):
        for h, t in self.hwnd.items():
            win32gui.ShowWindow(h, win32con.SW_SHOW)


class _Main(object):
    vw = list()
    old = 0

    def __init__(self, vw_num=5):
        self.SysTrayIcon = None
        self.vw_num = vw_num
        for i in range(0, vw_num):
            self.vw.append(VWindow())

    def switch_to_window(self, param):
        if param == self.old:
            return
        self.vw[self.old].hide_visual_window()
        self.vw[param].show_visual_window()
        self.old = param
        self.switch_icon(icon="./VisualDesktop" + str(param + 1) + ".ico")

    def exit(self):
        for i in range(0, self.vw_num):
            self.vw[i].show_visual_window()
        try:
            self.SysTrayIcon.destroy()
        except BaseException as e:
            print(e.args)

    def main(self):
        self.add_SysTrayIcon()
        kb.add_hotkey("alt+1", self.switch_to_window, args=(0,))
        kb.add_hotkey("alt+2", self.switch_to_window, args=(1,))
        kb.add_hotkey("alt+3", self.switch_to_window, args=(2,))
        kb.add_hotkey("alt+4", self.switch_to_window, args=(3,))
        kb.add_hotkey("alt+5", self.switch_to_window, args=(4,))
        kb.add_hotkey("ctrl+alt+q", self.exit)
        kb.wait("ctrl+alt+q")

    def switch_icon(self, icon, text='0'):
        if self.SysTrayIcon:
            self.SysTrayIcon.refresh(icon=icon)

    def add_SysTrayIcon(self, icon='./VisualDesktop1.ico', hover_text="vwindow"):
        self.SysTrayIcon = tb.SysTrayIcon(icon=icon)
        self.SysTrayIcon.active()


if __name__ == '__main__':
    app = _Main(6)
    app.main()
