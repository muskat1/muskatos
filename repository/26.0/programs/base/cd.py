parts = command.split()

class CD:
    def cd(self):
        try:
            cd_path = parts[1]
        except IndexError:
            print('cd: missing path to cd')
            print('usage: cd <path or file name>')
            return

        cd_path = memu.get_abs_path(cd_path)

        path_info = memu.get_info(cd_path)

        if not path_info:
            print(f'cd: directory {cd_path} doesn\'t exist')
            return

        if path_info['type'] != 'folder':
            print(f'cd: {cd_path} is not a directory')
            return

        memu.write_file(f'{disk}/usr/cwd', cd_path)

CD().cd()
