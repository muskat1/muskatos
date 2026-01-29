parts = command.split()

class Cat:
    def __init__(self):
        self.cwd = memu.get_info(f'{disk}/usr/cwd')['content']

    def cat(self):
        try:
            path = parts[1]
        except IndexError:
            print('cat: missing file to cat')
            print('usage: cat <path or file name>')
            return

        path = memu.get_abs_path(path)

        path_info = memu.get_info(path)

        if not path_info:
            print(f'cat: file {path} is not found')
            return

        if path_info['type'] != 'file':
            print(f'cat: {path} is {path_info['type']}')
            return

        if path_info['content'] == None:
            return

        print(path_info['content'])

Cat().cat()
