# 虚拟桌面

- [虚拟桌面](#虚拟桌面)
  - [背景](#背景)
  - [安装](#安装)
  - [使用说明](#使用说明)
  - [使用许可](#使用许可)

## 背景
使用 Windows 下的虚拟桌面着实不爽，所有写了这样一个用起来起码会很顺手的虚拟桌面

## 安装
这个项目使用[python3](https://www.python.org/)，请确保你本地安装了它。

本项目使用到的 `module` 包含 `pywin32`、`keyboard`，你在运行该程序之前需要先安装它们
```sh
$ python -m pip install pywin32
$ python -m pip install keyboard
```

## 使用说明
这是一个 python 脚本，你可以下载下来直接运行该脚本
```sh
$ git clone https://github.com/sczzr/visual-window.git
$ cd visual-window/
$ python ./vwindow.py
```

描述：
- 拥有 5 个虚拟桌面
- 通过快捷键去切换桌面
  
快捷键：
```
alt + 1, 2, 3, 4, 5
使用这些快捷键进行虚拟桌面的切换
```

## 使用许可

[MIT](LICENSE) © Richard Littauer