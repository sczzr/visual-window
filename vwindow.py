#!/usr/bin/python3

import win32con, win32gui
import keyboard
import sys


def is_real_window(hwnd):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) \
            and win32gui.IsWindowVisible(hwnd):
        # hasNoOwner = win32gui.GetWindow(hwnd, win32con.GW_OWNER) == 0
        lExStyle = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        if (lExStyle & win32con.WS_EX_TOOLWINDOW) == 0:
            if win32gui.GetWindowText(hwnd):
                return True
        return False


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


old = 0
vw = list()


def exit():
    for i in range(0, 5):
        vw[i].show_visual_window()


def switch_to_window(param):
    global old
    if param == old:
        return
    try:
        vw[old].hide_visual_window()
        vw[param].show_visual_window()
        old = param
    except:
        exit()


if __name__ == '__main__':
    for i in range(0, 5):
        vw.append(VWindow())
    old = 0
    keyboard.add_hotkey("alt+1", switch_to_window, args=(0,))
    keyboard.add_hotkey("alt+2", switch_to_window, args=(1,))
    keyboard.add_hotkey("alt+3", switch_to_window, args=(2,))
    keyboard.add_hotkey("alt+4", switch_to_window, args=(3,))
    keyboard.add_hotkey("alt+5", switch_to_window, args=(4,))
    keyboard.add_hotkey("ctrl+alt+q", exit)
    keyboard.wait("ctrl+alt+q")
