# 《尘白禁区》服务器切换器 前端（tk）

此前端程序由tkinter库支持。

当前版本暂不支持配置文件。

![icon_png](res/icon1.png)

## 构建

### 环境配置

作者的Python版本为`3.8.8`，使用的库见<venv/Lib/installation_notes/pip_list.txt>。

### 构建exe

此项目使用PyInstaller-6.3.0构建。

## 使用

当前版本在当前路径下查找脚本`CBJQ_SS.main.bat`，可以通过`-cwd [path/to/script]`切换工作目录。

本程序只是前端，后端/内核请转到此项目下载：<https://github.com/LiuJiewenTT/Snowbreak_ServerSwitcher>

## 程序说明

版本说明：
1. A版为单文件版，且启用了upx压缩，运行前会临时解压到暂存目录下，因此启动较慢。
2. B版为文件夹版，此版本暂不提供。

## License

当前版本使用：MIT License。
