import tkinter
from tkinter import ttk
import subprocess
import shutil
import os.path as osp
import os
import sys
from typing import Dict, Tuple, Callable, Any
from functools import partial
import threading
import unicodedata

tkinter_NWES = (tkinter.N, tkinter.W, tkinter.E, tkinter.S)


def func_none(*args):
    print('none')


unicodeCharWidth: Callable[[str], int] = (lambda x: 2 if unicodedata.east_asian_width(x) in 'WF' else 1)

lenCJK: Callable[[str], int] = lambda x: sum(unicodeCharWidth(c) for c in x)

strOverDivider: Callable[[int, str, int], str] = lambda x, sign, maxcnt: x + sign * (lambda y: 0 if y < 0 else y)(
    maxcnt - lenCJK(x))


def getProgramResourcePath(path) -> str:
    global frontend_programdir, build_flag
    path = osp.join(frontend_programdir + ('' if build_flag else '/../../'), path)
    path = osp.normpath(path)
    return path


def checkExecutableReadiness(exec_name: str) -> bool:
    if not osp.exists(exec_name) and not shutil.which(exec_name):
        return False
    return True


def printAndInsertWrapper(func: Callable[[Any], Any]) -> Callable:
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


class CBJQ_SS_FrontEnd_tk:
    server_list: Dict[str, str]
    backend_path: str
    displayLog_frame_state: bool
    divider_length: int = 50

    def __init__(self, **kwargs):
        """初始化

        :param kwargs:  backend_path: str,
                        server_list: Dict[str, str]
        """
        self.backend_path = kwargs.get('backend_path')
        self.server_list = kwargs.get('server_list')

        self.displayLog_frame_state = False

        self.root_window = tkinter.Tk()
        self.root_window.title("尘白禁区服务器切换器 - 前端")
        # print(getProgramResourcePath('res/icon1.png'))
        self.root_window.iconphoto(True, tkinter.PhotoImage(file=getProgramResourcePath('res/icon1.png')))  # 使用核心目录
        # self.root_window.iconphoto(True, tkinter.PhotoImage(file=frontend_programdir + '/../../res/icon1.png'))

        # Define Section
        # 命名规则：实例名称+类名

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
        # Define displayLog_frame
        self.displayLog_frame = ttk.Frame(self.main_frame, padding=(5, 5))
        # Define displayLog_titlebar_frame
        self.displayLog_titlebar_frame = ttk.Frame(self.displayLog_frame)
        # Define displayLog_label
        self.displayLog_label_Var = tkinter.StringVar(value='日志输出：')
        self.displayLog_label = ttk.Label(self.displayLog_titlebar_frame, textvariable=self.displayLog_label_Var,
                                          anchor=tkinter.W)
        # Define displayLog_clean_button
        self.displayLog_clean_button_Var = tkinter.StringVar(value='清空')
        self.displayLog_clean_button = ttk.Button(self.displayLog_titlebar_frame,
                                                  textvariable=self.displayLog_clean_button_Var,
                                                  command=self.cleanLogDisplayed)
        # Define displayLog_text
        self.displayLog_text = tkinter.Text(self.displayLog_frame, width=100, height=30)
        # self.displayLog_text['state'] = 'normal'
        # self.displayLog_text.bind('<Control C>', lambda e: self.root_window.clipboard_append(e), print('copied'))
        self.displayLog_text.bind('<Key>', lambda e: (self.root_window.clipboard_append(e)
                                                      if e.state == 12 and e.keysym == 'c' else "break"))  # Read Only
        # Define displayLog_label_scrollbar
        self.displayLog_text_scrollbar = ttk.Scrollbar(self.displayLog_frame, orient=tkinter.VERTICAL,
                                                       command=self.displayLog_text.yview)
        self.displayLog_text['yscrollcommand'] = self.displayLog_text_scrollbar.set  # 设置双方回调以实现交流
        # Define statusbar
        self.statusbar_label_Var = tkinter.StringVar(value='作者: LiuJiewenTT <liuljwtt@163.com>。')
        self.statusbar_label = ttk.Label(self.root_window, textvariable=self.statusbar_label_Var, anchor=tkinter.W)

        # instance methods
        self.main_frame.getPaddingTuple_Regular = partial(getPaddingTuple_Regular, self.main_frame)
        self.doAction_frame.getPaddingTuple_Regular = partial(getPaddingTuple_Regular, self.doAction_frame)
        self.displayLog_text.insertAndScrollToEnd = partial(insertAndScrollToEnd, self.displayLog_text)

    def run(self):
        # Geometry Management
        self.root_window.rowconfigure(0, weight=1)
        self.root_window.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure((0, 2), weight=1)
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.grid(sticky=tkinter_NWES)
        self.listServer_frame.columnconfigure(0, weight=1)
        self.listServer_frame.rowconfigure(1, weight=1)
        self.listServer_frame.grid(column=0, row=0, sticky=tkinter_NWES)
        self.listServer_label.grid(column=0, row=0, sticky=(tkinter.W, tkinter.S))
        self.listServer_listbox.grid(column=0, row=1, sticky=tkinter_NWES)
        self.doAction_frame.grid(column=1, row=0, rowspan=1, sticky=tkinter.N)
        self.doSwitch_button.grid(column=0, row=0)
        self.doSwitchAndRun_button.grid(column=0, row=1)
        self.doRun_button.grid(column=0, row=2)
        self.toggleLogDisplay_button.grid(column=0, row=3, sticky=tkinter.S)
        self.displayLog_frame.columnconfigure(0, weight=1)
        self.displayLog_frame.rowconfigure(1, weight=1)
        self.displayLog_titlebar_frame.columnconfigure(1, weight=1)
        self.displayLog_titlebar_frame.grid(column=0, row=0, columnspan=2, sticky=tkinter_NWES)
        self.displayLog_label.grid(column=0, row=0, sticky=(tkinter.W, tkinter.S))
        self.displayLog_clean_button.grid(column=1, row=0, sticky=(tkinter.E, tkinter.S))
        self.displayLog_text.grid(column=0, row=1, sticky=tkinter_NWES)
        self.displayLog_text_scrollbar.grid(column=1, row=1, sticky=(tkinter.N, tkinter.S))
        self.statusbar_label.grid(column=0, row=1, columnspan=3, sticky=(tkinter.W, tkinter.S))

        self.root_window.update()
        self.root_window.minsize(width=self.doAction_frame.winfo_width(),
                                 height=self.doAction_frame.winfo_height() + self.statusbar_label.winfo_height()
                                        + self.main_frame.getPaddingTuple_Regular()[1]
                                        + self.main_frame.getPaddingTuple_Regular()[3])
        self.root_window.mainloop()
        return

    def toggleLogDisplay(self):
        if self.displayLog_frame_state:
            self.displayLog_frame_state = False
            self.displayLog_frame.grid_forget()
            self.toggleLogDisplay_button_Var.set('日志 >')
        else:
            self.displayLog_frame_state = True
            self.displayLog_frame.grid(column=2, row=0, rowspan=1, sticky=tkinter_NWES)
            self.toggleLogDisplay_button_Var.set('日志 <')
        return

    def cleanLogDisplayed(self):
        self.displayLog_text.delete('1.0', tkinter.END)

    def execAction_threading(self, **kwargs):
        thread = threading.Thread(target=self.execAction, kwargs=kwargs)
        thread.start()

    def execAction(self, **kwargs):
        self.displayLog_text.insertAndScrollToEnd('[+]' + strOverDivider('运行前报告', '=', self.divider_length))
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
            with subprocess.Popen(launch_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8') as sp:
                self.displayLog_text.insertAndScrollToEnd(f'sp.pid: {sp.pid}')
                self.displayLog_text.insertAndScrollToEnd('[+]' + strOverDivider('运行报告', '-', self.divider_length))
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
                    '[-]' + strOverDivider(f'运行后报告(pid: {sp.pid})', '-', self.divider_length))
                self.displayLog_text.insertAndScrollToEnd(f'sp.pid: {sp.pid}')
                self.displayLog_text.insertAndScrollToEnd(f'返回值: {sp.poll()}')
                self.displayLog_text.insertAndScrollToEnd(f'返回值表明的运行结果: {self.resolveBackendRetv(sp.returncode)}')
            self.displayLog_text.insertAndScrollToEnd('[-]' + '' + '=' * self.divider_length)
        else:
            self.displayLog_text.insertAndScrollToEnd('[-]' + strOverDivider('未运行', '=', self.divider_length))
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


if __name__ == '__main__':
    backend_path = 'CBJQ_SS.main.bat'
    server_list = {'国际服': 'worldwide', 'B服': 'bilibili', '官服': 'kingsoft'}

    frontend_programdir = osp.normpath(osp.dirname(__file__))
    if osp.exists(__file__):
        build_flag = False
    else:
        build_flag = True
    print(f'frontend_programdir: {frontend_programdir}')
    # input()
    argv = sys.argv
    for i in range(0, len(argv)):
        if argv[i] == '-cwd':
            cwd = argv[i + 1]
            print('Old CWD: ' + os.getcwd())
            os.chdir(cwd)
            print('New CWD: ' + os.getcwd())
            break

    exec_readiness = checkExecutableReadiness('CBJQ_SS.main.bat')
    if exec_readiness is False:
        print('Executable not found.')
    CBJQ_SS_FrontEnd_tk(backend_path=backend_path, server_list=server_list).run()
