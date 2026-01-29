import json

parts = command.split()

class MKDir:
    def __init__(self):
        self.cwd = memu.get_info(f'{disk}/usr/cwd')['content']
        self.curr_user = memu.get_info(f'{disk}/usr/curr_user')['content']
        curr_user_groups_raw = memu.get_info(f'{disk}/config/users.json')['content']
        self.curr_user_groups = json.loads(curr_user_groups_raw)[self.curr_user]['groups']

    def mkdir(self):
        try:
            path = parts[1]
        except IndexError:
            print('mkdir: missing directory to create')
            print('usage: mkdir <directory name or path to the directory>')
            return

        path = memu.get_abs_path(path)

        name = path.split('/')[-1]

        if memu.get_info(path):
            print('mkdir: directory already exists')
            return

        path_parts = path.split('/')
        path_parts.pop(-1)
        parent = '/'.join(path_parts)
        parent_info = memu.get_info(parent)
        if not parent_info:
            print(f'mkdir: cannot access parent \'{parent}\': No such file or directory')
            return
        parent_perms = parent_info['permissions'].split(',')

        if parent_info['type'] != 'folder':
            print('mkdir: parent is not a directory')
            return

        if not 'w' in parent_perms and not 'root' in self.curr_user_groups:
            print(f'mkdir: you don\'t have permissions to make directories in {parent_info['path']}')
            return

        if not memu.mk(parent, name, 'folder', 'r,w'):
            print(f'mkdir: something went wrong when making {path}')

MKDir().mkdir()
