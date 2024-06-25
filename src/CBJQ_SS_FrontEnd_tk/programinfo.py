import sys
import os.path as osp

build_flag: bool
author_name = 'LiuJiewenTT'
author_email = 'liuljwtt@163.com'
author_info: dict
project_name = 'CBJQ_SS_FrontEnd-tk'
project_link = 'https://github.com/LiuJiewenTT/CBJQ_SS_FrontEnd-tk'
product_name = '尘白禁区切服器'
program_name = 'CBJQ_SS_FrontEnd-tk'
product_version = (1, 1, 1, 0)
program_version = (1, 1, 1, 0)
program_version_str: str
program_iconpicture_paths = [
    'res/icon1.png',
    'res/里芙带来了她的两个包子-透明背景.png',
    'res/里芙和她的两个包子.png',
]
program_iconpicture_idx = 1
program_iconpicture_path: str
frontend_name = '尘白禁区服务器切换器 - 前端'
license_type = 'MIT License'
buildin_exinfo: object


# 以下自动生成
author_info = {
    'author_name': author_name,
    'author_email': author_email
}

if not osp.exists(__file__) and getattr(sys, 'frozen', False):
    build_flag = True
else:
    build_flag = False

if build_flag is True:
    # from ...keep_local.build import builtin_exinfo
    from .builtin_exinfo import Builtin_ExInfo
else:
    from .builtin_exinfo_default import Builtin_ExInfo
builtin_exinfo = Builtin_ExInfo()


def override_programinfo_vars(self):
    global program_iconpicture_idx
    if self.program_iconpicture_idx is not None:
        program_iconpicture_idx = self.program_iconpicture_idx


override_programinfo_vars(builtin_exinfo)


def ver2str(version_tuple: tuple):
    version_str = 'v'
    for i in version_tuple:
        version_str += f'{i}.'
    version_str = version_str[:-1].rstrip('.0')
    return version_str


product_version_str = ver2str(product_version)
program_version_str = ver2str(program_version)
program_iconpicture_path = program_iconpicture_paths[program_iconpicture_idx]
