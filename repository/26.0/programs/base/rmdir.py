import json

parts = command.split()

class RMDir:
    def __init__(self):
        self.cwd = memu.get_info(f'{disk}/usr/cwd')['content']
        self.curr_user = memu.get_info(f'{disk}/usr/curr_user')['content']
        curr_user_groups_raw = memu.get_info(f'{disk}/config/users.json')['content']
        self.curr_user_groups = json.loads(curr_user_groups_raw)[self.curr_user]['groups']

    def rmdir(self):
        try:
            path = parts[1]
        except IndexError:
            print('rmdir: missing directory to remove')
            print('usage: rmdir <directory>')
            return

        path = memu.get_abs_path(path)

        info = memu.get_info(path)
        children = memu.get_children(path)
        
        if not info:
            print('rmdir: directory does not exist')
            return

        if info['type'] != 'folder':
            print(f'rmdir: {path} is not a folder')
            return

        if not 'w' in info['permissions'].split(',') and not 'root' in self.curr_user_groups:
            print(f'rmdir: you don\'t have permission to remove {path}')
            return

        if children:
            print('rmdir: directory is not empty')
            return

        if not memu.rm(path):
            print(f'rmdir: something went wrong when removing {path}')

RMDir().rmdir()
