import random
import subprocess
import shutil
import os.path as osp
import os
import sys
from typing import Dict, Tuple, Callable, Union, Any, List
from functools import partial
import threading
import orjson
import tkinter
from tkinter import ttk
import tkinter.font
import PIL
import PIL.ImageTk
import PIL.Image
import unicodedata
from ctypes import windll
from CBJQ_SS_FrontEnd_tk.programinfo import *
if getattr(sys, 'frozen', False):
    import pyi_splash

# Windows Section
GWL_STYLE = -16
GWLP_HWNDPARENT = -8
WS_CAPTION = 0x00C00000
WS_THICKFRAME = 0x00040000
WS_BORDER = 0x00800000
GWL_EXSTYLE = -20
WS_EX_APPWINDOW = 0x00040000
WS_EX_TOOLWINDOW = 0x00000080
# WS_POPUP = 0x80000000
GetWindowLongPtrW = windll.user32.GetWindowLongPtrW
SetWindowLongPtrW = windll.user32.SetWindowLongPtrW


class Logger_Identifer:
    id: str = 'unknown'
    newline: bool = False


class Logger(object):
    def __init__(self, identifier: Logger_Identifer, filename, mode='a', encoding='UTF-8'):
        self.identifier = identifier
        self.terminal = sys.stdout
        self.log = open(filename, mode, encoding=encoding)
        self.log_KeepFlushing = True

    def write(self, message):
        message: str
        if self.terminal:
            self.terminal.write(message)
        # message = message.replace('\n', '\n[stdout] ', message.count('\n', 0, -1))
        message = message[:-1].replace('\n', '\n[stdout] ') + (message[-1] if len(message) else '')
        if self.identifier.id != 'stdout' or self.identifier.newline is True:
            self.identifier.id = 'stdout'
            self.log.write('[stdout] ')
        if message.endswith('\n'):
            self.identifier.newline = True
        else:
            self.identifier.newline = False
        self.log.write(message)
        if self.log_KeepFlushing is True:
            self.flush()

    def flush(self):
        if self.terminal:
            self.terminal.flush()
        self.log.flush()


class Logger_ERR2OUTLOG(object):
    def __init__(self, identifier: Logger_Identifer, out: Logger):
        self.identifier = identifier
        self.terminal = sys.stderr
        self.log = out.log
        self.log_KeepFlushing = True

    def write(self, message):
        message: str
        if self.terminal:
            self.terminal.write(message)
        # message = message.replace('\n', '\n[stderr] ', message.count('\n', 0, -1))
        message = message[:-1].replace('\n', '\n[stderr] ') + (message[-1] if len(message) else '')
        if self.identifier.id != 'stderr' or self.identifier.newline is True:
            self.identifier.id = 'stderr'
            self.log.write('[stderr] ')
        if message.endswith('\n'):
            self.identifier.newline = True
        else:
            self.identifier.newline = False
        self.log.write(message)
        if self.log_KeepFlushing is True:
            self.flush()

    def flush(self):
        if self.terminal:
            self.terminal.flush()
        self.log.flush()


def get_window_handle(root) -> int:
    root.update_idletasks()
    # This gets the window's parent same as `ctypes.windll.user32.GetParent`
    return GetWindowLongPtrW(root.winfo_id(), GWLP_HWNDPARENT)


# Rumtime globals
runtime_global_standard_font: tkinter.font.Font
runtime_global_resultBonus_pics_success_list_photoimage: List[Union[None, PIL.ImageTk.PhotoImage]]

tkinter_NWES = (tkinter.N, tkinter.W, tkinter.E, tkinter.S)


def func_none(*args):
    print('none')


returnIfNotNone: Callable[[Any, Any], Any] = (lambda x, default: default if x is None else x)

returnIFNotLogicalFalse: Callable[[Any, Any], Any] = (lambda x, default: default if x else x)

unicodeCharWidth: Callable[[str], int] = (lambda x: 2 if unicodedata.east_asian_width(x) in 'WF' else 1)

lenCJK: Callable[[str], int] = lambda x: sum(unicodeCharWidth(c) for c in x)

strOverDivider_fixed: Callable[[str, str, int], str] = lambda x, sign, maxcnt: x + sign * (lambda y: 0 if y < 0 else y)(
    maxcnt - lenCJK(x))


def strOverDivider(string: str, sign: str, maxcnt: int, font: Union[None, tkinter.font.Font] = None,
                   standard_font: Union[None, tkinter.font.Font] = None) -> str:
    if font is None:
        return strOverDivider_fixed(string, sign, maxcnt)
    else:
        divider = sign * maxcnt
        if standard_font is None:
            global runtime_global_standard_font
            if 'runtime_global_standard_font' not in globals():
                runtime_global_standard_font = tkinter.font.Font(
                    family=tkinter.font.nametofont('TkFixedFont').actual('family'), size=font.actual('size'))
            standard_font = runtime_global_standard_font

        # print(f'font: {font}')
        # print(f'standard_font: {standard_font}')
        sign_length = font.measure(sign)
        div_length = standard_font.measure(divider)
        str_length = font.measure(string)
        remain_length = (lambda x: 0 if x < 0 else x)(div_length - str_length)
        cnt = round(remain_length * 1.0 / sign_length)
        # 不需要手动删除吧，大概？反正下面两种都可以删除。
        # standard_font.__del__()
        # tkinter._get_default_root('use font').call('font', 'delete', standard_font.name)
        return string + sign * cnt


def getProgramResourcePath(path) -> str:
    global frontend_programdir, build_flag
    path = osp.join(frontend_programdir + ('' if build_flag else '/../../'), path)
    path = osp.normpath(path)
    return path


getNonBuildinProgramResourcePath: Callable[[str], str] = lambda x: osp.join(cwd_initial, x)


def checkExecutableReadiness(exec_name: str) -> bool:
    if not osp.exists(exec_name) and not shutil.which(exec_name):
        return False
    return True


def printAndInsertWrapper(func):
    def func2(*args, **kwargs):
        print_flag = kwargs.get('print')
        if print_flag is not False:
            endding = kwargs.get('end')
            if print_flag is not None:  # print=True (by default)
                kwargs.pop('print')
            print(args[1], end=endding)
        return func.__call__(*args, **kwargs)

    return func2


@printAndInsertWrapper
def insertAndScrollToEnd(self, arg2, end='\n'):
    self.insert('end', str(arg2) + end)
    self.yview_moveto(1)


def getPaddingTuple_Regular(self) -> Tuple[int]:
    rawtuple = self['padding']
    retv = [int(str(x)) for x in rawtuple]
    if len(rawtuple) != 4:
        retv = retv[:2] + retv[:2]
    # print(self, retv)
    return tuple(retv)


def calcIMG_MAX_WHTuple(original_WH: Tuple[int, int], frame_WH: Tuple[int, int]) -> Tuple[int, int]:
    # o_w, o_h = original_WH
    # f_w, f_h = frame_WH
    # print(original_WH, frame_WH)
    scale_w, scale_h = [frame_WH[i] / original_WH[i] for i in range(0, 2)]
    scale = min(scale_w, scale_h)
    retv = (round(original_WH[i] * scale) for i in range(2))
    return retv


resizeImgIntoFrame: Callable[[PIL.Image.Image, Tuple[int, int]], PIL.Image.Image] = \
    (lambda img, framesize: img.resize(calcIMG_MAX_WHTuple(original_WH=(img.width, img.height),
                                                           frame_WH=framesize)))


def window_setRedirect(root):
    root.overrideredirect(True)

    def set_appwindow(root):
        hwnd = windll.user32.GetParent(root.winfo_id())
        style = windll.user32.GetWindowLongPtrW(hwnd, GWL_EXSTYLE)
        style = style & ~WS_EX_TOOLWINDOW
        style = style | WS_EX_APPWINDOW
        res = windll.user32.SetWindowLongPtrW(hwnd, GWL_EXSTYLE, style)
        # re-assert the new window style    # 下面两句恢复任务栏图标
        root.withdraw()
        root.after(10, root.deiconify)

    root.after(10, set_appwindow, root)


class CBJQ_SS_FrontEnd_tk_Splash:
    splash_canvas: tkinter.Canvas
    canvas_size: Tuple[int, int]
    splash_img: PIL.Image.Image
    splash_logo_img: PIL.Image.Image
    splash_play_img: PIL.Image.Image
    broken: bool = False
    isRandom: bool = True
    logo_framesize = (480, 270)
    play_button_framesize = (100, 100)
    close_button_framesize = (50, 50)
    quitProgram_flag: int = 0

    def __init__(self, imgpathinfolist: List[Dict[str, str]], size: Tuple[int, int] = (640, 360),
                 isRandom: bool = True, autoSkipTime: int = 0, splashWindowKind: str = 'borderless'):
        idx = 0
        if len(imgpathinfolist) <= 0:
            self.broken = True
            return
        self.isRandom = isRandom
        if isRandom:
            idx = random.randrange(0, len(imgpathinfolist), 1)
        imgpathinfo = imgpathinfolist[idx]
        imgpath = imgpathinfo.get('path')
        imgtype = imgpathinfo.get('type')
        if not imgpath:
            self.broken = True
            return
        if imgtype == 'buildin':
            imgpath = getProgramResourcePath(imgpath)
        elif imgtype == 'nonbuildin':
            imgpath = getNonBuildinProgramResourcePath(imgpath)

        self.autoSkipTime = autoSkipTime
        self.splashWindowKind = splashWindowKind

        self.root_window = tkinter.Tk()
        self.root_window.title(f'{product_name} - {author_name}')
        self.root_window.iconphoto(True, tkinter.PhotoImage(file=getProgramResourcePath(program_iconpicture_path)))
        # self.root_window.configure(bg='blue')
        self.root_window.scheduleRecords = []

        self.splash_img = PIL.Image.open(imgpath)
        self.splash_photoimg = PIL.ImageTk.PhotoImage(resizeImgIntoFrame(self.splash_img, size))

        self.canvas_size = (self.splash_photoimg.width(), self.splash_photoimg.height())
        # print(self.canvas_size)
        self.splash_canvas = tkinter.Canvas(self.root_window,
                                            width=self.canvas_size[0], height=self.canvas_size[1],
                                            highlightthickness=0, selectborderwidth=0)
        # self.splash_canvas.configure(bg='red')
        self.splash_canvas.canvas_texts = []

        self.splash_logo_img = PIL.Image.open(getProgramResourcePath('res\\启动页资源\\logo.png'))
        self.splash_logo_photoimg = PIL.ImageTk.PhotoImage(resizeImgIntoFrame(self.splash_logo_img,
                                                                              framesize=self.logo_framesize))
        # self.splash_logo_photoimg = PIL.ImageTk.PhotoImage(resizeImgIntoFrame(self.splash_logo_img,
        #                                                                       framesize=self.logo_framesize))
        self.splash_play_img = PIL.Image.open(getProgramResourcePath('res\\启动页资源\\play.png')).convert("RGBA")
        self.splash_play_photoimg = PIL.ImageTk.PhotoImage(image=resizeImgIntoFrame(self.splash_play_img,
                                                                                    framesize=self.play_button_framesize))
        # print(self.splash_play_img.mode)

        self.splash_close_img = PIL.Image.open(getProgramResourcePath('res\\启动页资源\\close.png'))
        self.splash_close_photoimg = PIL.ImageTk.PhotoImage(image=resizeImgIntoFrame(self.splash_close_img,
                                                                                     framesize=self.close_button_framesize))

        # self.root_window.overrideredirect(1)  # 暂时注释
        # self.root_window.wm_attributes('-type', 'desktop')   # linux可用
        # self.root_window.wm_attributes('-transparentcolor', "white")
        # self.root_window.wm_attributes('-topmost', True)
        # self.root_window.wm_attributes('-disabled', True)
        # self.root_window.wm_attributes('-toolwindow', False)

        # self.root_window.resizable(False, False)
        self.root_window.configure(width=self.canvas_size[0], height=self.canvas_size[1])
        self.root_window.eval('tk::PlaceWindow . center')

        # 根据splashWindowKind决定后续
        if self.splashWindowKind == 'true-borderless':
            # self.root_window.overrideredirect(1)
            self.root_window.wm_attributes('-topmost', True)
            pass
        elif self.splashWindowKind == 'normal':
            pass
        else:
            # if self.splashWindowKind == 'grasped-in' or True:
            #     self.root_window.resizable(False, False)
            hwnd: int = get_window_handle(self.root_window)
            style: int = GetWindowLongPtrW(hwnd, GWL_STYLE)
            # style &= ~(WS_CAPTION | WS_THICKFRAME | WS_BORDER)
            if self.splashWindowKind == 'borderless' and True:
                style &= ~(WS_CAPTION | WS_THICKFRAME)
                # style &= ~(WS_CAPTION)
            elif self.splashWindowKind == 'photo-frame' and True:
                style &= ~(WS_THICKFRAME | WS_BORDER)
            elif self.splashWindowKind == 'grasped-in' or self.splashWindowKind == 'no-caption' and True:
                # when resizeable
                style &= ~(WS_BORDER)
                # style &= ~(WS_CAPTION)    # 会添加额外padding，不如上面那句
            elif self.splashWindowKind == 'non-resizeable-normal' and True:
                style &= ~(WS_THICKFRAME)

            SetWindowLongPtrW(hwnd, GWL_STYLE, style)
        # self.root_window.wm_sizefrom('program')
        # print('wm_frame', self.root_window.wm_frame())
        # self.root_window.update_idletasks()
        # print(self.root_window.winfo_width(), self.root_window.winfo_height())
        # print(self.root_window.winfo_reqwidth(), self.root_window.winfo_reqheight())

    def run(self):
        if self.broken:
            return

        relx = lambda x: self.canvas_size[0] * x
        rely = lambda y: self.canvas_size[1] * y
        # self.root_window.configure(width=self.canvas_size[0], height=self.canvas_size[1])
        self.root_window.configure(width=self.canvas_size[0] + 1, height=self.canvas_size[1] + 1)  # 加一是似乎是tk有bug
        self.root_window.update_idletasks()
        self.splash_canvas.pack()
        # self.splash_canvas.pack(padx=0, pady=0, ipadx=0, ipady=0)
        # self.splash_canvas.place()
        # self.root_window.eval('tk::PlaceWindow . center')
        self.splash_canvas.create_image(0, 0, image=self.splash_photoimg, anchor="nw")
        self.splash_canvas.create_image(relx(0.5), rely(0.3),
                                        image=self.splash_logo_photoimg)
        self.splash_canvas.canvas_texts.append(
            self.splash_canvas.create_text(relx(0.5), rely(0.5),
                                           text='切服器', fill='white',
                                           font=tkinter.font.Font(self.root_window,
                                                                  family=tkinter.font.nametofont('TkTextFont')[
                                                                      'family'],
                                                                  size='-{}'.format(int(rely(0.1))) )))

        self.play_button = self.splash_canvas.create_image(relx(0.5), rely(0.75), image=self.splash_play_photoimg)
        self.splash_canvas.tag_bind(self.play_button, "<Button-1>", lambda event: self.destroy())
        self.close_button = self.splash_canvas.create_image(relx(1), rely(0),
                                                            image=self.splash_close_photoimg, anchor="ne")
        self.splash_canvas.tag_bind(self.close_button, "<Button-1>", lambda event: self.destroy(opt=1))
        if self.autoSkipTime > 250:
            scheduleId = self.root_window.after(self.autoSkipTime, lambda: self.destroy())
            self.root_window.scheduleRecords.append(scheduleId)

        self.root_window.configure(width=self.canvas_size[0], height=self.canvas_size[1])
        self.root_window.update()
        print('splash window size: ', self.root_window.winfo_width(), self.root_window.winfo_height())
        print('splash canvas size: ', self.splash_canvas.winfo_width(), self.splash_canvas.winfo_height())
        # self.root_window.eval('tk::PlaceWindow . center')

        # 根据splashWindowKind决定后续
        if self.splashWindowKind == 'true-borderless':
            scheduleId = self.root_window.after(300, window_setRedirect, self.root_window)
            self.root_window.scheduleRecords.append(scheduleId)
            scheduleId = self.root_window.after(1000, lambda: self.root_window.wm_attributes('-topmost', False))
            self.root_window.scheduleRecords.append(scheduleId)

        self.root_window.mainloop()
        return self.quitProgram_flag

    def destroy(self, opt=0):
        # print('销毁')
        # self.splash_photoimg.__del__()
        print('window size when destroy: ', self.root_window.winfo_width(), self.root_window.winfo_height())
        for item in self.splash_canvas.canvas_texts:
            self.splash_canvas.delete(item)
        if self.root_window.scheduleRecords:
            scheduleRecords = self.root_window.scheduleRecords.copy()
            # print(scheduleRecords)
            for item in scheduleRecords:
                # print(item)
                self.root_window.after_cancel(item)
                self.root_window.scheduleRecords.remove(item)
        self.root_window.destroy()
        if opt:
            self.quitProgram_flag = opt


class CBJQ_SS_FrontEnd_tk:
    server_list: Dict[str, str]
    backend_path: str
    displayLog_frame_state: bool
    divider_length: int = 50
    resutlBonus_pics_framesize: Tuple[int, int] = (200, 200)
    resultBonus_pics_success_list: List[Dict]
    resultBonus_pics_fail_list: List[Dict]

    def __init__(self, **kwargs):
        """初始化

        :param kwargs:  backend_path: str,
                        server_list: Dict[str, str]
        """
        self.config: Union[None, dict] = None
        self.config_savepath: Union[None, str] = None
        self.backend_path = kwargs.get('backend_path')
        self.server_list = kwargs.get('server_list')
        if self.server_list is None:
            self.server_list = {}

        # Define Section
        # 命名规则：实例名称+类名
        self.text_fixed_font: tkinter.font.Font
        self.text_unfixed_font: tkinter.font.Font

        # Define rootWindow
        self.__init_rootWindow__()

        # Define aboutWindow
        # self.__init_aboutWindow__()

    def __init_rootWindow__(self):
        self.root_window = tkinter.Tk()
        self.root_window.title(frontend_name)

        # print(getProgramResourcePath('res/icon1.png'))
        self.root_window.iconphoto(True, tkinter.PhotoImage(file=getProgramResourcePath(program_iconpicture_path)))  # 使用核心目录
        # self.root_window.iconphoto(True, tkinter.PhotoImage(file=frontend_programdir + '/../../res/icon1.png'))
        # Dev: define img
        # self.img1 = PIL.ImageTk.PhotoImage(PIL.Image.open(getProgramResourcePath('res/让芙提雅老师看看谁在.jpg')))
        # self.root_window.wm_attributes('-transparentcolor', 'lightgrey')
        # self.root_window.wm_attributes('-alpha', '0.9')
        # self.background_label_1 = ttk.Label(self.main_frame, image=self.img1)
        # self.background_label_1.place(x=0, y=0, relwidth=1, relheight=1)
        self.root_window.protocol("WM_DELETE_WINDOW", func=self.onDeleteMainWindow)

        displayLog_ifWrapChar = True
        displayLog_text_ifUseFixedFont = False
        self.displayLog_frame_state = False

        # Define Section
        # 命名规则：实例名称+类名

        # Define Fonts
        self.text_fixed_font = tkinter.font.nametofont('TkFixedFont')
        self.text_unfixed_font = tkinter.font.nametofont('TkTextFont')

        # Define main_frame_style
        self.main_frame_style = ttk.Style()
        self.main_frame_style.configure('main_frame.TFrame', background='lightgrey')
        # Define main_frame
        self.main_frame = ttk.Frame(self.root_window, padding=(3, 12),
                                    width=400, height=300, style='main_frame.TFrame')
        # Define listServer_frame
        self.listServer_frame = ttk.Frame(self.main_frame, padding=(5, 5))
        # Define listServer_label
        self.listServer_label_Var = tkinter.StringVar(value='预设服务器列表：')
        self.listServer_label = ttk.Label(self.listServer_frame, textvariable=self.listServer_label_Var)
        # Define listServer_listbox
        self.listServer_listbox_choice = list(self.server_list.keys())
        self.listServer_listbox_choice_Var = tkinter.StringVar(value=self.listServer_listbox_choice)
        self.listServer_listbox = tkinter.Listbox(self.listServer_frame,
                                                  listvariable=self.listServer_listbox_choice_Var, width=20)
        # Define doAction_frame
        self.doAction_frame = ttk.Frame(self.main_frame, padding=(5, 5))
        # Define doSwitch_button
        self.doSwitch_button_Var = tkinter.StringVar(value='切换')
        self.doSwitch_button = ttk.Button(self.doAction_frame, textvariable=self.doSwitch_button_Var,
                                          command=lambda: self.execAction_threading(action='s'))
        # Define doSwitchAndRun_button
        self.doSwitchAndRun_button_Var = tkinter.StringVar(value='切换并启动')
        self.doSwitchAndRun_button = ttk.Button(self.doAction_frame, textvariable=self.doSwitchAndRun_button_Var,
                                                command=lambda: self.execAction_threading(action='s&r'))
        # Define doRun_button
        self.doRun_button_Var = tkinter.StringVar(value='直接启动')
        self.doRun_button = ttk.Button(self.doAction_frame, textvariable=self.doRun_button_Var,
                                       command=lambda: self.execAction_threading(action='r'))
        # Define toggleLogDisplay_button
        self.toggleLogDisplay_button_Var = tkinter.StringVar(value='日志 >')
        self.toggleLogDisplay_button = ttk.Button(self.doAction_frame, textvariable=self.toggleLogDisplay_button_Var,
                                                  command=self.toggleLogDisplay)
        # Define nonAction_frame1
        self.nonAction_frame1 = ttk.Frame(self.main_frame)
        # Define aboutWindow_showButton
        self.aboutWindow_showButton_ImgVar = PIL.ImageTk.PhotoImage(
            resizeImgIntoFrame(
                PIL.Image.open(getProgramResourcePath('res/通用资源/info-1459077_640.png')), framesize=(50, 50)))
        self.aboutWindow_showButton = ttk.Button(self.nonAction_frame1, image=self.aboutWindow_showButton_ImgVar,
                                                 command=self.run_aboutWindow)
        # Define displayLog_frame
        self.displayLog_frame = ttk.Frame(self.main_frame, padding=(5, 5))
        # Define displayLog_titlebar_frame
        self.displayLog_titlebar_frame = ttk.Frame(self.displayLog_frame)
        # Define displayLog_label
        self.displayLog_label_Var = tkinter.StringVar(value='日志输出：')
        self.displayLog_label = ttk.Label(self.displayLog_titlebar_frame, textvariable=self.displayLog_label_Var,
                                          anchor=tkinter.W)
        # Define displayLog_wrapchar_checkbutton
        self.displayLog_wrapchar_checkbutton_Var = tkinter.StringVar(value='自动换行')
        self.displayLog_wrapchar_checkbutton_Val = tkinter.StringVar(
            value='char' if displayLog_ifWrapChar else 'none')  # 默认勾选
        self.displayLog_wrapchar_checkbutton = ttk.Checkbutton(self.displayLog_titlebar_frame,
                                                               textvariable=self.displayLog_wrapchar_checkbutton_Var,
                                                               variable=self.displayLog_wrapchar_checkbutton_Val,
                                                               onvalue='char', offvalue='none',
                                                               command=self.toggleLogLineWrapStyle)
        # Define displayLog_UseFixedFont_checkbutton
        self.displayLog_UseFixedFont_checkbutton_Var = tkinter.StringVar(value='等宽字体')
        self.displayLog_UseFixedFont_checkbutton_Val = tkinter.StringVar(
            value='fixed' if displayLog_text_ifUseFixedFont else 'unfixed')
        self.displayLog_UseFixedFont_checkbutton = ttk.Checkbutton(self.displayLog_titlebar_frame,
                                                                   textvariable=self.displayLog_UseFixedFont_checkbutton_Var,
                                                                   variable=self.displayLog_UseFixedFont_checkbutton_Val,
                                                                   onvalue='fixed', offvalue='unfixed',
                                                                   command=self.toggleLogFontFixedChoice)
        # Define displayLog_clean_button
        self.displayLog_clean_button_Var = tkinter.StringVar(value='清空')
        self.displayLog_clean_button = ttk.Button(self.displayLog_titlebar_frame,
                                                  textvariable=self.displayLog_clean_button_Var,
                                                  command=self.cleanLogDisplayed)
        # Define displayLog_text
        self.displayLog_text_font = self.text_unfixed_font
        self.displayLog_text = tkinter.Text(self.displayLog_frame, width=100, height=30,
                                            font=self.displayLog_text_font)
        # self.displayLog_text['state'] = 'normal'
        # self.displayLog_text.bind('<Control C>', lambda e: self.root_window.clipboard_append(e), print('copied'))
        self.displayLog_text.bind('<Key>', lambda e: (self.root_window.clipboard_append(e)
                                                      if e.state == 12 and e.keysym == 'c' else "break"))  # Read Only
        # Define displayLog_text_scrollbar
        self.displayLog_text_scrollbar = ttk.Scrollbar(self.displayLog_frame, orient=tkinter.VERTICAL,
                                                       command=self.displayLog_text.yview)
        self.displayLog_text['yscrollcommand'] = self.displayLog_text_scrollbar.set  # 设置双方回调以实现交流
        # Define displayLog_text_scrollbar_x
        self.displayLog_text_scrollbar_x = ttk.Scrollbar(self.displayLog_frame, orient=tkinter.HORIZONTAL,
                                                         command=self.displayLog_text.xview)
        self.displayLog_text['xscrollcommand'] = self.displayLog_text_scrollbar_x.set
        # Define statusbar
        # self.statusbar_label_Var = tkinter.StringVar(value=f'作者: {author_name} <{author_email}>。')
        self.statusbar_label_Var = tkinter.StringVar(
            value=f'作者: {author_name} <{author_email}> 版本: {program_version_str}')
        self.statusbar_label = ttk.Label(self.root_window, textvariable=self.statusbar_label_Var, anchor=tkinter.W)

        # instance methods
        self.main_frame.getPaddingTuple_Regular = partial(getPaddingTuple_Regular, self.main_frame)
        self.doAction_frame.getPaddingTuple_Regular = partial(getPaddingTuple_Regular, self.doAction_frame)
        self.displayLog_text.insertAndScrollToEnd = partial(insertAndScrollToEnd, self.displayLog_text)

    def __init_aboutWindow__(self):
        self.aboutWindow = tkinter.Toplevel(self.root_window)
        self.aboutWindow.withdraw()
        self.aboutWindow.title('关于')
        self.aboutWindow.configure(padx=10, pady=10)

        # Define aboutWindow_programIconImgLabel
        self.aboutWindow_programIconImgLabel_ImgVar = PIL.ImageTk.PhotoImage(
            resizeImgIntoFrame(PIL.Image.open(getProgramResourcePath(program_iconpicture_path)), framesize=(256, 256)))
        self.aboutWindow_programIconImgLabel = ttk.Label(self.aboutWindow,
                                                         image=self.aboutWindow_programIconImgLabel_ImgVar)
        # Define aboutWindow_contentLabel
        self.aboutWindow_contentLabel_Var = tkinter.StringVar(value=programinfo_str1)
        self.aboutWindow_contentLabel = ttk.Label(self.aboutWindow, textvariable=self.aboutWindow_contentLabel_Var,
                                                  padding=(10, 10))

    def run(self):
        self.run_rootWindow()

    def run_rootWindow(self):
        # Geometry Management
        self.root_window.rowconfigure(0, weight=1)
        self.root_window.columnconfigure(0, weight=1)
        self.main_frame.grid(sticky=tkinter_NWES)
        self.main_frame.columnconfigure((0, 2), weight=1)
        self.main_frame.rowconfigure((1,), weight=1)
        self.listServer_frame.grid(column=0, row=0, rowspan=2, sticky=tkinter_NWES)
        self.listServer_frame.columnconfigure(0, weight=1)
        self.listServer_frame.rowconfigure(1, weight=1)
        self.listServer_label.grid(column=0, row=0, sticky=(tkinter.W, tkinter.S))
        self.listServer_listbox.grid(column=0, row=1, sticky=tkinter_NWES)
        self.doAction_frame.grid(column=1, row=0, rowspan=1, sticky=tkinter.N)
        self.doSwitch_button.grid(column=0, row=0)
        self.doSwitchAndRun_button.grid(column=0, row=1)
        self.doRun_button.grid(column=0, row=2)
        self.toggleLogDisplay_button.grid(column=0, row=3, sticky=tkinter.S)
        self.nonAction_frame1.grid(column=1, row=1, sticky=tkinter.S)
        self.aboutWindow_showButton.grid(column=0, row=0)
        self.displayLog_frame.columnconfigure(0, weight=1)
        self.displayLog_frame.rowconfigure(1, weight=1)
        self.displayLog_titlebar_frame.grid(column=0, row=0, columnspan=2, sticky=tkinter_NWES)
        self.displayLog_titlebar_frame.columnconfigure((1, 2,), weight=1)
        self.displayLog_label.grid(column=0, row=0, sticky=(tkinter.W, tkinter.S))
        self.displayLog_wrapchar_checkbutton.grid(column=1, row=0, sticky=(tkinter.E, tkinter.S))
        self.displayLog_UseFixedFont_checkbutton.grid(column=2, row=0, sticky=(tkinter.E, tkinter.S))
        self.displayLog_clean_button.grid(column=3, row=0, sticky=(tkinter.E, tkinter.S))
        self.displayLog_text.grid(column=0, row=1, sticky=tkinter_NWES)
        self.displayLog_text_scrollbar.grid(column=1, row=1, sticky=(tkinter.N, tkinter.S))
        # self.displayLog_text_scrollbar_x.grid(column=0, row=2, sticky=(tkinter.W, tkinter.N, tkinter.E))
        self.statusbar_label.grid(column=0, row=1, columnspan=3, sticky=(tkinter.W, tkinter.S))

        self.root_window.update()
        self.root_window.minsize(width=self.doAction_frame.winfo_width(),
                                 height=self.doAction_frame.winfo_height() + self.statusbar_label.winfo_height()
                                        + self.main_frame.getPaddingTuple_Regular()[1]
                                        + self.main_frame.getPaddingTuple_Regular()[3])
        # self.root_window.configure(width=self.doAction_frame.winfo_width()+self.listServer_frame.winfo_width())
        self.root_window.mainloop()
        return

    def run_aboutWindow(self):
        # Define aboutWindow
        self.__init_aboutWindow__()     # Define window when called.
        self.aboutWindow.deiconify()
        self.aboutWindow.rowconfigure((0, ), weight=1)
        self.aboutWindow.columnconfigure((0, ), weight=1)
        self.aboutWindow_programIconImgLabel.grid(column=0, row=0)
        self.aboutWindow_contentLabel.grid(column=0, row=1)

    def toggleLogDisplay(self):
        if self.displayLog_frame_state:
            self.displayLog_frame_state = False
            self.displayLog_frame.grid_forget()
            self.toggleLogDisplay_button_Var.set('日志 >')
        else:
            self.displayLog_frame_state = True
            self.displayLog_frame.grid(column=2, row=0, rowspan=2, sticky=tkinter_NWES)
            self.toggleLogDisplay_button_Var.set('日志 <')
        return

    def toggleLogLineWrapStyle(self):
        # print(self.displayLog_wrapchar_checkbutton_Val.get())
        if self.displayLog_wrapchar_checkbutton_Val.get() == 'char':
            self.displayLog_text.configure(wrap='char')
            self.displayLog_text_scrollbar_x.grid_forget()
        elif self.displayLog_wrapchar_checkbutton_Val.get() == 'none':
            self.displayLog_text.configure(wrap='none')
            self.displayLog_text_scrollbar_x.grid(column=0, row=2, sticky=(tkinter.W, tkinter.N, tkinter.E))

    def toggleLogFontFixedChoice(self):
        if self.displayLog_UseFixedFont_checkbutton_Val.get() == 'fixed':
            # print('切换到等宽字体')
            self.displayLog_text_font = self.text_fixed_font
            self.displayLog_text.config(font=self.text_fixed_font)
        elif self.displayLog_UseFixedFont_checkbutton_Val.get() == 'unfixed':
            # print('切换到非等宽字体')
            self.displayLog_text_font = self.text_unfixed_font
            self.displayLog_text.config(font=self.text_unfixed_font)

    def cleanLogDisplayed(self):
        self.displayLog_text.delete('1.0', tkinter.END)

    def execAction_threading(self, **kwargs):
        thread = threading.Thread(target=self.execAction, kwargs=kwargs)
        thread.start()

    def execAction(self, **kwargs):
        self.displayLog_text.insertAndScrollToEnd(strOverDivider('[+]' + '运行前报告', '=', self.divider_length,
                                                                 self.displayLog_text_font))
        self.displayLog_text.insertAndScrollToEnd(kwargs)
        launch_args = []
        action = kwargs.get('action')
        if action in ['s', 's&r']:
            self.displayLog_text.insertAndScrollToEnd('do switch')
            if action == 's&r':
                self.displayLog_text.insertAndScrollToEnd('launch')
            else:
                launch_args.append('-nostart')
        elif action in ['r']:
            self.displayLog_text.insertAndScrollToEnd('only launch')
            launch_args.append('-noswitch')

        if launch_args or action in ['s&r']:
            launch_args.append('-nopause')
            curselection_idxs: tuple = self.listServer_listbox.curselection()
            if len(curselection_idxs) > 0:
                curselection_idx = int(curselection_idxs[0])
                curselection_value = self.server_list[self.listServer_listbox_choice[curselection_idx]]
                launch_args.append(curselection_value)
                self.displayLog_text.insertAndScrollToEnd(
                    f'curselection: {curselection_idxs}, [{self.listServer_listbox_choice[curselection_idx]}]')
            else:
                self.displayLog_text.insertAndScrollToEnd(f'curselection: {curselection_idxs}, [无]')
            launch_cmd = [self.backend_path]
            launch_cmd.extend(launch_args)
            self.displayLog_text.insertAndScrollToEnd(f'launch_cmd: {launch_cmd}')
            exec_readiness = checkExecutableReadiness(self.backend_path)
            if exec_readiness:
                startupinfo = subprocess.STARTUPINFO()
                if exec_noWindow:
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    startupinfo.wShowWindow = subprocess.SW_HIDE
                with subprocess.Popen(launch_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                      encoding='utf-8', startupinfo=startupinfo) as sp:
                    self.displayLog_text.insertAndScrollToEnd(f'sp.pid: {sp.pid}')
                    self.displayLog_text.insertAndScrollToEnd(strOverDivider('[+]' + '运行报告', '-', self.divider_length,
                                                                             self.displayLog_text_font))
                    while True:
                        # print('to read')
                        try:
                            output = sp.stdout.__next__()
                            # print(output.encode())
                        except StopIteration:
                            break
                        # output = sp.stdout.readline()
                        # print(f'[stdout]: {i}', end='')
                        # self.displayLog_text.insert('end', i)
                        # self.displayLog_text.yview_moveto(1)
                        self.displayLog_text.insertAndScrollToEnd(output, end='')  # instance method
                        # self.displayLog_text.update()
                    print('')
                    self.displayLog_text.insertAndScrollToEnd(
                        strOverDivider('[-]' + f'运行后报告(pid: {sp.pid})', '-', self.divider_length,
                                       self.displayLog_text_font))
                    self.displayLog_text.insertAndScrollToEnd(f'sp.pid: {sp.pid}')
                    self.displayLog_text.insertAndScrollToEnd(f'返回值: {sp.poll()}')
                    self.displayLog_text.insertAndScrollToEnd(f'返回值表明的运行结果: {self.resolveBackendRetv(sp.returncode)}')
                    if self.displayInText_ResultBonus_pics(sp.returncode, self.displayLog_text):
                        self.displayLog_text.insert(tkinter.END, '\n')
            else:
                self.displayLog_text.insertAndScrollToEnd('后端程序未就绪：找不到后端程序，请移动切服器或修改切服器配置。')
            self.displayLog_text.insertAndScrollToEnd(strOverDivider('[-]' + '', '=', self.divider_length,
                                                                     self.displayLog_text_font))
        else:
            self.displayLog_text.insertAndScrollToEnd(strOverDivider('[-]' + '未运行', '=', self.divider_length,
                                                                     self.displayLog_text_font))
        pass

    def resolveBackendRetv(self, returncode: int) -> str:
        """
        解析后端返回值的含义

        :param returncode: 后端返回值
        :return: 含义str
        """
        if returncode == 0:
            return '正常结束'
        elif returncode == 1:
            return '指示未完成设定的错误，约等于未知错误。'
        elif returncode == 2:
            return '不存在可执行的启动器。'
        elif returncode == 3:
            return '切服器未找到此服务器启动选项的配置。'
        elif returncode == 4:
            return '目的地的启动器并非符号链接，非本程序创建。'
        elif returncode == 5:
            return '启动器链接失败。 '
        return '未查找到解释'

    def getResultBonus_pics_success(self, idx: Union[None, int] = None) -> Union[None, PIL.ImageTk.PhotoImage]:
        """
        获取结果奖励表情包(成功时)。此函数与失败时几乎相同，由于还没有想到优雅的整合方式，故分成两个函数。

        :param idx: [可选] 指定序号为idx的表情包
        :return: 表情包
        """
        if not self.resultBonus_pics_success_list:
            return None
        length_resultBonus_pics_success_list = len(self.resultBonus_pics_success_list)
        imgidx: int
        if idx is None:
            imgidx = random.randrange(0, length_resultBonus_pics_success_list, 1)
        else:
            imgidx = idx
            if imgidx >= length_resultBonus_pics_success_list:
                return None
        imginfo = self.resultBonus_pics_success_list[imgidx]
        if imginfo:
            imgtype = imginfo.get('type')
            imgpath = imginfo.get('path')
            if imgpath:
                # print(imgtype)
                if imgtype == 'buildin':
                    imgpath = getProgramResourcePath(imgpath)
                elif imgtype == 'nonbuildin':
                    imgpath = getNonBuildinProgramResourcePath(imgpath)
                global runtime_global_resultBonus_pics_success_list_photoimage
                if 'runtime_global_resultBonus_pics_success_list_photoimage' not in globals():
                    runtime_global_resultBonus_pics_success_list_photoimage = [None] * len(
                        self.resultBonus_pics_success_list)
                if runtime_global_resultBonus_pics_success_list_photoimage[imgidx] is None:
                    img1 = PIL.Image.open(imgpath)
                    img1 = resizeImgIntoFrame(img1, self.resutlBonus_pics_framesize)
                    runtime_global_resultBonus_pics_success_list_photoimage[imgidx] = PIL.ImageTk.PhotoImage(img1)
                img = runtime_global_resultBonus_pics_success_list_photoimage[imgidx]
                return img
        return None

    def getResultBonus_pics_fail(self, idx: Union[None, int] = None) -> Union[None, PIL.ImageTk.PhotoImage]:
        """
        获取结果奖励表情包(失败时)。此函数与成功时几乎相同，由于还没有想到优雅的整合方式，故分成两个函数。

        :param idx: [可选] 指定序号为idx的表情包
        :return: 表情包
        """
        if not self.resultBonus_pics_fail_list:
            return None
        length_resultBonus_pics_fail_list = len(self.resultBonus_pics_fail_list)
        imgidx: int
        if idx is None:
            imgidx = random.randrange(0, length_resultBonus_pics_fail_list, 1)
        else:
            imgidx = idx
            if imgidx >= length_resultBonus_pics_fail_list:
                return None
        imginfo = self.resultBonus_pics_fail_list[imgidx]
        if imginfo:
            imgtype = imginfo.get('type')
            imgpath = imginfo.get('path')
            if imgpath:
                # print(imgtype)
                if imgtype == 'buildin':
                    imgpath = getProgramResourcePath(imgpath)
                elif imgtype == 'nonbuildin':
                    imgpath = getNonBuildinProgramResourcePath(imgpath)
                global runtime_global_resultBonus_pics_fail_list_photoimage
                if 'runtime_global_resultBonus_pics_fail_list_photoimage' not in globals():
                    runtime_global_resultBonus_pics_fail_list_photoimage = [None] * len(
                        self.resultBonus_pics_fail_list)
                if runtime_global_resultBonus_pics_fail_list_photoimage[imgidx] is None:
                    img1 = PIL.Image.open(imgpath)
                    img1 = resizeImgIntoFrame(img1, self.resutlBonus_pics_framesize)
                    runtime_global_resultBonus_pics_fail_list_photoimage[imgidx] = PIL.ImageTk.PhotoImage(img1)
                img = runtime_global_resultBonus_pics_fail_list_photoimage[imgidx]
                return img
        return None

    def displayInText_ResultBonus_pics(self, returncode: int, widget: tkinter.Text, insertPosition=tkinter.END) -> bool:
        if returncode == 0:
            img = self.getResultBonus_pics_success()
        else:
            img = self.getResultBonus_pics_fail()
        if img:
            widget.image_create(insertPosition, image=img)
            # widget.window_create(insertPosition, window=ttk.Label(widget, image=img))
            # widget.insert(tkinter.CURRENT, '\n')
            # widget.insert(tkinter.CURRENT+' + 1c', '\n')
            return True
        return False

    def ApplyConfig(self, config: dict):
        self.config = config
        global backend_path, server_list
        local_backend_path = returnIfNotNone(config.get('backend_path'), backend_path)
        self.backend_path = local_backend_path
        local_server_list = returnIfNotNone(config.get('server_list'), server_list)
        self.server_list.update(local_server_list)
        self.listServer_listbox_choice = list(self.server_list.keys())
        self.listServer_listbox_choice_Var.set(self.listServer_listbox_choice)
        server_curselection_value = config.get('server_curselection')
        if server_curselection_value:
            self.listServer_listbox.select_set(
                [self.listServer_listbox_choice.index(i) for i in server_curselection_value])

        displayLog_ifWrapChar = returnIfNotNone(config.get('displayLog_ifWrapChar'), True)
        displayLog_ifWrapChar = 'char' if displayLog_ifWrapChar else 'none'
        if displayLog_ifWrapChar != self.displayLog_wrapchar_checkbutton_Val.get():
            self.displayLog_wrapchar_checkbutton.invoke()

        displayLog_text_ifUseFixedFont = returnIfNotNone(config.get('displayLog_text_ifUseFixedFont'), False)
        displayLog_text_ifUseFixedFont = 'fixed' if displayLog_text_ifUseFixedFont is True else 'unfixed'
        if displayLog_text_ifUseFixedFont != self.displayLog_UseFixedFont_checkbutton_Val.get():
            self.displayLog_UseFixedFont_checkbutton.invoke()
        # self.displayLog_UseFixedFont_checkbutton_Val.set('fixed' if displayLog_text_ifUseFixedFont else 'unfixed')

        self.resutlBonus_pics_framesize = returnIfNotNone(config.get('resutlBonus_pics_framesize'),
                                                          self.resutlBonus_pics_framesize)
        self.resultBonus_pics_success_list = config.get('resultBonus_pics_success_list')
        self.resultBonus_pics_fail_list = config.get('resultBonus_pics_fail_list')
        return

    def PackConfig(self) -> dict:
        retv: dict = self.config
        retv['backend_path'] = self.backend_path
        retv['server_list'] = self.server_list
        retv['server_curselection'] = [self.listServer_listbox_choice[i] for i in
                                       self.listServer_listbox.curselection()]
        retv['displayLog_ifWrapChar'] = True if self.displayLog_wrapchar_checkbutton_Val.get() == 'char' else False
        retv['displayLog_text_ifUseFixedFont'] = \
            True if self.displayLog_UseFixedFont_checkbutton_Val.get() == 'fixed' else False
        retv['resutlBonus_pics_framesize'] = self.resutlBonus_pics_framesize
        retv['resultBonus_pics_success_list'] = self.resultBonus_pics_success_list
        retv['resultBonus_pics_fail_list'] = self.resultBonus_pics_fail_list
        self.config = retv
        return retv

    def WriteConfig(self, filepath: Union[str, None] = None):
        content = orjson.dumps(self.config, option=orjson.OPT_INDENT_2)
        if filepath is None:
            filepath = self.config_savepath
        print(f'Write config to: {filepath}')
        with open(filepath, 'w', encoding='UTF-8') as f:
            if printConfigOnWrite:
                print(content.decode(encoding='UTF-8'))
            f.write(content.decode(encoding='UTF-8'))
        print(f'Write success.')

    def onDeleteMainWindow(self):
        self.PackConfig()
        if not LOCKCONFIG:
            self.WriteConfig()
        else:
            print('LOCKCONFIG = True')
        self.root_window.destroy()


def changeCWD(the_new_cwd: str):
    global cwd_old, cwd
    if os.getcwd() == osp.abspath(osp.normpath(the_new_cwd)):
        return
    cwd_old = os.getcwd()
    print('Old CWD: ' + cwd_old)
    cwd = the_new_cwd
    os.chdir(cwd)
    print('New CWD: ' + os.getcwd())


def ApplyGlobalConfig(AppConfig: dict):
    global LOCKCONFIG, backend_path, server_list, cwd, \
        showSplash, splashWindowKind, showSplash_autoSkipAfter, splashSize, showSplashRandomly, splash_ImgPathInfoList,\
        exec_noWindow, printConfigOnWrite, log_keepFlushing
    LOCKCONFIG = returnIfNotNone(AppConfig.get('LOCKCONFIG'), LOCKCONFIG)
    backend_path = returnIfNotNone(AppConfig.get('backend_path'), backend_path)
    server_list = returnIfNotNone(AppConfig.get('server_list'), server_list)
    showSplash = returnIfNotNone(AppConfig.get('showSplash'), showSplash)
    splashWindowKind = returnIfNotNone(AppConfig.get('splashWindowKind'), splashWindowKind)
    showSplash_autoSkipAfter = returnIfNotNone(AppConfig.get('showSplash_autoSkipAfter'), 0)
    splashSize = returnIfNotNone(AppConfig.get('splashSize'), splashSize)
    showSplashRandomly = returnIfNotNone(AppConfig.get('showSplashRandomly'), showSplashRandomly)
    splash_ImgPathInfoList = returnIfNotNone(AppConfig.get('splash_ImgPathInfoList'), splash_ImgPathInfoList)
    changeCWD(returnIfNotNone(AppConfig.get('cwd'), cwd))
    exec_noWindow = returnIfNotNone(AppConfig.get('exec_noWindow'), exec_noWindow)
    printConfigOnWrite = returnIfNotNone(AppConfig.get('printConfigOnWrite'), printConfigOnWrite)
    log_keepFlushing = returnIfNotNone(AppConfig.get('log_keepFlushing'), log_keepFlushing)
    sys.stdout.log_KeepFlushing = log_keepFlushing
    sys.stderr.log_KeepFlushing = log_keepFlushing
    pass


def PackGlobalConfig(AppConfig: dict) -> dict:
    retv = AppConfig
    # global backend_path, server_list
    retv['LOCKCONFIG'] = LOCKCONFIG
    retv['backend_path'] = backend_path
    retv['server_list'] = server_list
    retv['showSplash'] = showSplash
    retv['splashWindowKind'] = splashWindowKind
    retv['showSplash_autoSkipAfter'] = showSplash_autoSkipAfter
    retv['splashSize'] = splashSize
    retv['showSplashRandomly'] = showSplashRandomly
    retv['splash_ImgPathInfoList'] = splash_ImgPathInfoList
    retv['cwd'] = cwd
    retv['exec_noWindow'] = exec_noWindow
    retv['printConfigOnWrite'] = printConfigOnWrite
    retv['log_keepFlushing'] = log_keepFlushing
    return retv


if __name__ == '__main__':
    config_filename = 'CBJQ_SS_FrontEnd-tk.config.json'
    appConfig: Union[None, dict] = None
    LOCKCONFIG: bool = False
    cwd: str = '.'
    cwd_old: str = ''
    cwd_initial: str = os.getcwd()
    showSplash: bool = True
    splashWindowKind: str = 'borderless'  # borderless, true-borderless, photo-frame, non-resizeable-normal （其它暂不应使用）
    showSplash_autoSkipAfter: int = 0
    splashSize: Tuple[int, int] = (640, 360)
    showSplashRandomly: bool = True
    splash_ImgPathInfoList: List[Dict[str, str]] = []
    backend_path = 'CBJQ_SS.main.bat'
    server_list = {'国际服': 'worldwide', 'B服': 'bilibili', '官服': 'kingsoft'}
    exec_noWindow = True
    printConfigOnWrite = False
    log_keepFlushing = True

    stdout_raw = sys.stdout
    std_identifer = Logger_Identifer()
    sys.stdout = Logger(std_identifer, 'log.txt', 'w')
    sys.stderr = Logger_ERR2OUTLOG(std_identifer, sys.stdout)

    programinfo_str1 = (f'Product Name: {product_name}\n'
                        f'FrontEnd Name: {frontend_name}\n'
                        f'Author: {author_name} <{author_email}>\n'
                        f'Program Version: {program_version_str}\n'
                        f'Project Name: {project_name}\n'
                        f'Project Link: {project_link}\n'
                        f'License Type: {license_type}\n')

    print(programinfo_str1)

    if osp.exists(config_filename):
        with open(config_filename, 'r', encoding='UTF-8') as f:
            config_content = f.read()
            if config_content:
                appConfig: dict = orjson.loads(config_content)
        if appConfig is not None:
            ApplyGlobalConfig(appConfig)

    frontend_programdir = osp.normpath(osp.dirname(__file__))
    if osp.exists(__file__):
        build_flag = False
    else:
        build_flag = True
    print(f'frontend_programdir: {frontend_programdir}')
    # input()
    argv = sys.argv
    arg_cwd = ''
    for i in range(0, len(argv)):
        if argv[i] == '-cwd':
            arg_cwd = argv[i + 1]
            break
    if arg_cwd != '':
        changeCWD(arg_cwd)
    appConfig = PackGlobalConfig(returnIfNotNone(appConfig, {}))

    if getattr(sys, 'frozen', False):
        pyi_splash.close()

    exec_readiness = checkExecutableReadiness('CBJQ_SS.main.bat')
    if exec_readiness is False:
        print('Executable not found.')

    if showSplash:
        FrontEnd_Splash_instance = CBJQ_SS_FrontEnd_tk_Splash(imgpathinfolist=splash_ImgPathInfoList,
                                                              size=splashSize,
                                                              isRandom=showSplashRandomly,
                                                              autoSkipTime=showSplash_autoSkipAfter,
                                                              splashWindowKind=splashWindowKind)
        retv = FrontEnd_Splash_instance.run()
        if retv:
            sys.exit(0)
        # input('end of splash')

    if appConfig is not None:
        FrontEnd_instance = CBJQ_SS_FrontEnd_tk()
        FrontEnd_instance.ApplyConfig(appConfig)
    else:
        FrontEnd_instance = CBJQ_SS_FrontEnd_tk(backend_path=backend_path, server_list=server_list)
    FrontEnd_instance.config_savepath = osp.join(cwd_old, config_filename)
    # print(cwd_old)
    FrontEnd_instance.run()
