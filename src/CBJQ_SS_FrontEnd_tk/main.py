import tkinter
from tkinter import ttk
import subprocess
import shutil
import os.path as osp
import os
import sys

tkinter_NWES = (tkinter.N, tkinter.W, tkinter.E, tkinter.S)


def func_none(*args):
    print('none')


def checkExecutableReadiness(exec_name: str):
    if not osp.exists(exec_name) and not shutil.which(exec_name):
        return False
    return True


class CBJQ_SS_FrontEnd_tk:

    backend_path: str

    def __init__(self, **kwargs):
        self.backend_path = kwargs.get('backend_path')

        self.root_window = tkinter.Tk()
        self.root_window.title("尘白禁区服务器切换器 - 前端")

        # Define Section
        # 命名规则：实例名称+类名

        # Define main_frame_style
        self.main_frame_style = ttk.Style()
        self.main_frame_style.configure('main_frame.TFrame', background='lightgrey')
        # Define main_frame
        self.main_frame = ttk.Frame(self.root_window, padding=(3, 12),
                               width=400, height=300, style='main_frame.TFrame')
        self.main_frame.grid(sticky=tkinter_NWES)
        # Define listServer_label
        self.listServer_label_Var = tkinter.StringVar(value='预设服务器列表：')
        self.listServer_label = ttk.Label(self.main_frame, textvariable=self.listServer_label_Var)
        # Define listServer_listbox
        self.listServer_listbox_choice = ['worldwide', 'bilibili', 'kingsoft']
        self.listServer_listbox_choice_Var = tkinter.StringVar(value=self.listServer_listbox_choice)
        self.listServer_listbox = tkinter.Listbox(self.main_frame, listvariable=self.listServer_listbox_choice_Var, width=20)
        # Define doAction_frame
        self.doAction_frame = ttk.Frame(self.main_frame, padding=(5, 5))
        # Define doSwitch_button
        self.doSwitch_button_Var = tkinter.StringVar(value='切换')
        self.doSwitch_button = ttk.Button(self.doAction_frame, textvariable=self.doSwitch_button_Var,
                                          command=lambda: self.execAction(action='s'))
        # Define doSwitchAndRun_button
        self.doSwitchAndRun_button_Var = tkinter.StringVar(value='切换并启动')
        self.doSwitchAndRun_button = ttk.Button(self.doAction_frame, textvariable=self.doSwitchAndRun_button_Var,
                                                command=lambda: self.execAction(action='s&r'))

    def run(self):
        # Geometry Management
        self.listServer_label.grid(column=0, row=0, sticky=tkinter.W)
        self.listServer_listbox.grid(column=0, row=1)
        self.doSwitch_button.grid(column=0, row=0)
        self.doSwitchAndRun_button.grid(column=0, row=1)
        self.doAction_frame.grid(column=1, row=0, rowspan=2, sticky=tkinter.N)
        self.root_window.mainloop()
        return

    def execAction(self, **kwargs):
        print(kwargs)
        launch_args = []
        if kwargs.get('action') in ['s', 's&r']:
            print('do switch')
            launch_args.append('-nopause')
            if kwargs['action'] == 's&r':
                print('launch')
            else:
                launch_args.append('-nostart')
            launch_cmd = [self.backend_path]
            launch_cmd.extend(launch_args)
            print(launch_cmd)
            with subprocess.Popen(launch_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8') as sp:
                print(sp.pid)
                output = sp.stdout.readlines()
                for i in output:
                    print(f'[stdout]: {i}', end='')
                print('')
        pass


if __name__ == '__main__':
    backend_path = 'CBJQ_SS.main.bat'

    argv = sys.argv
    for i in range(0, len(argv)):
        if argv[i] == '-cwd':
            cwd = argv[i+1]
            print('Old CWD: ' + os.getcwd())
            os.chdir(cwd)
            print('New CWD: ' + os.getcwd())
            break

    exec_readiness = checkExecutableReadiness('CBJQ_SS.main.bat')
    if exec_readiness is False:
        print('Executable not found.')
    CBJQ_SS_FrontEnd_tk(backend_path=backend_path).run()
