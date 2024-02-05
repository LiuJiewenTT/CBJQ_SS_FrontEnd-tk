# 《尘白禁区》服务器切换器 前端（tk）

此前端程序由tkinter库支持。

当前版本已支持配置文件。

![icon_png](res/icon1.png)

## 构建

### 环境配置

作者的Python版本为`3.8.8`，使用的库见<venv/Lib/installation_notes/pip_list.txt>。

### 构建exe

此项目使用PyInstaller-6.3.0构建。

## 使用

当前版本在当前路径下查找脚本`CBJQ_SS.main.bat`，可以通过`-cwd [path/to/script]`切换工作目录，或在配置文件中设定。

本程序只是前端，后端/内核请转到此项目下载：<https://github.com/LiuJiewenTT/Snowbreak_ServerSwitcher>。

## 程序说明

版本说明：
1. A版为单文件版，且启用了upx压缩，运行前会临时解压到暂存目录下，因此启动较慢。
2. B版为文件夹版，此版本暂不提供。

功能备注：

1. 程序可以自动生成**配置文件**，但适不适合你的情况要你自己检查。
2. 生成的配置文件会在每次程序正常退出时自动更新重写，但内部信息不会随意变动，持续保持原有数据，除非受到**启动参数的影响**（如`-cwd`）。
3. **运行后报告**需要后端版本不低于`v1.0.1`。

### 配置文件说明

>  注：不同程序版本可能使用的配置文件不完全相同，若有出入，请依照此节说明进行更新。（不保证未来会有配置更新迁移功能。）

> 注：配置文件为 *JSON* 格式，参数请依照 JSON 基本规范修改。（JSON无注释，以下示例使用Python的注释方式不代表带着注释可以运行。）

``` json
{
  "backend_path": "CBJQ_SS.main.bat",		# 设置后端程序CBJQ_SS.main.bat的文件路径。若为相对路径则受cwd影响。
  "server_list": {							# 设置显示的服务器列表和对应的用于传递给后端程序使其指定服务器的值
    "国际服": "worldwide",					# 格式："显示名称": "对应参数值"。显示名称必须唯一，不可重复。
    "B服": "bilibili",
    "官服": "kingsoft"
  },
  "showSplash": true,						# 显示启动页。true表示显示，false表示不显示。
  "showSplash_autoSkipAfter": 0,			# 设置启动页自动跳过计时时长，低于（或等于）250ms不生效。
  "splashSize": [							# 设置启动页在启动时的最大尺寸。启动页会自动适配启动图尺寸。
    640,									# 宽度。单位：像素
    360										# 高度。单位：像素
  ],
  "showSplashRandomly": true,				# 设置是否随机选取启动图
  "splash_ImgPathInfoList": [				# 启动图列表
    {
      "path": "res\\启动页资源\\预设启动图\\截图\\屏幕截图(770).png",	# 图片路径
      "type": "buildin"											# 图片的路径类型，buildin表示程序自带，nonbuildin表示程序启动时的工作目录下依路径寻找，其它值视为无效并进行默认操作：在当前运行的工作目录依路径寻找。
    }
  ],
  "cwd": ".",								# 运行时的工作目录。
  "server_curselection": [					# 当前选择的，在服务器列表中供选择的服务器选项
    "B服"									# 使用“显示名称”而非“对应参数值”。
  ],
  "displayLog_ifWrapChar": true,				# 设置日志文本是否启用自动换行。
  "displayLog_text_ifUseFixedFont": false,		# 设置日志文本是否使用等宽字体。在Win10上，不使用等宽字体将会使用更好看的“微软雅黑”字体。
  "resutlBonus_pics_framesize": [			# 运行后报告显示的表情包的最大尺寸限制
    200,									# 宽度。单位：像素
    200										# 高度。单位：像素
  ],
  "resultBonus_pics_success_list": null,	# 运行后报告显示的在程序运行正常时的表情包。同上splash_ImgPathInfoList的格式。
  "resultBonus_pics_fail_list": null		# 运行后报告显示的在程序运行出错时的表情包。同上splash_ImgPathInfoList的格式。
}
```



## License

当前版本使用：MIT License。
