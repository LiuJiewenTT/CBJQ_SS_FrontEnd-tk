import tkinter
from tkinter import ttk

tkinter_NWES = (tkinter.N, tkinter.W, tkinter.E, tkinter.S)


def func_none(*args):
    print('none')


class CBJQ_SS_FrontEnd_tk:

    def __init__(self):
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
        if kwargs.get('action') in ['s', 's&r']:
            print('do switch')
            if kwargs['action'] == 's&r':
                print('launch')

        pass


if __name__ == '__main__':
    CBJQ_SS_FrontEnd_tk().run()
