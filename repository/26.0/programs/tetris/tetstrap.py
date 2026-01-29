import json
import os
from pathlib import Path

parts = command.split(' ', 2)

class Tetstrap:
    def __init__(self):
        self.cwd = memu.get_info(f'{disk}/usr/cwd')['content']
        self.curr_user = memu.get_info(f'{disk}/usr/curr_user')['content']
        curr_user_groups_raw = memu.get_info(f'{disk}/config/users.json')['content']
        self.curr_user_groups = json.loads(curr_user_groups_raw)[self.curr_user]['groups']

    def tetstrap(self):
        try:
            tdisk = parts[1]
        except IndexError:
            print('tetstrap: missing disk to install packages to')
            return

        if not f'{tdisk}.db' in disks or tdisk == disk:
            print('tetstrap: invalid disk')
            return

        try:
            packages = parts[2].split()
        except IndexError:
            print('tetstrap: missing packages to install')
            return

        if not 'root' in self.curr_user_groups:
            print(f'tetstrap: you don\'t have permissions to install packages into {tdisk}')
            return
        
        tdisk_info = memu.get_info(tdisk)

        if tdisk_info['parent'] != '/':
            print('tetstrap: invalid disk')
            return

        if not memu.get_info(f'{tdisk}/programs'):
            memu.mk(tdisk, 'programs', 'folder', 'r')

        for package in packages:
            if package == 'base/memuboot':
                if memu.get_info(f'{tdisk}/memu/boot.py'):
                    print(f'memuboot.py is already installed - reinstalling')
                    memu.rm(f'{tdisk}/memu/boot.py')
                    memu.rm(f'{tdisk}/memu')
                
                memu.mk(tdisk, 'memu', 'folder', 'r')
                memu.mk(f'{tdisk}/memu', 'boot.py', 'file', 'r')
                with open((Path(memu_path) / 'repository' / boot.version / 'programs' / 'base' / 'memu_boot.py'), 'r') as f:
                    pkg_data = f.read()
                memu.write_file(f'{tdisk}/memu/boot.py', pkg_data)
                print(f'memuboot.py was successfully installed')

            elif package == 'base/muskatos':
                if memu.get_info(f'{tdisk}/usr') and memu.get_info(f'{tdisk}/config') and memu.get_info(f'{tdisk}/home') and memu.get_info(f'{tdisk}/root'):
                    print(f'muskatos is already installed - can\'t reinstall base directories and files')
                    return

                root_objects = [
                    ('config', 'folder', 'r'),
                    ('usr', 'folder', 'r'),
                    ('home', 'folder', 'r'),
                    ('root', 'folder', 'r')
                ]
                
                for name, obj_type, perms in root_objects:
                    result = memu.mk(tdisk, name, obj_type, perms)

                objects = [
                    (f'{tdisk}/config', 'hostname', 'file', 'r'),
                    (f'{tdisk}/config', 'users.json', 'file', 'r'),
                    (f'{tdisk}/usr', 'curr_user', 'file', 'r'),
                    (f'{tdisk}/usr', 'cwd', 'file', 'r,w')
                ]

                for path, name, obj_type, perms in objects:
                    result = memu.mk(path, name, obj_type, perms)

                root_password = input('tetstrap: root password for your new system: ')
                
                hostname = 'muskatos'
                users = json.dumps({
                    'root': {
                        'password': root_password,
                        'groups': ['users', 'sudoers', 'root'],
                        'home': f'{tdisk}/root'
                    }
                })

                memu.write_file(f'{tdisk}/config/users.json', users)
                memu.write_file(f'{tdisk}/config/hostname', hostname)
                print(f'muskatos was successfully installed')

            else:
                pkg_parts = package.split('/')

                if len(pkg_parts) > 2:
                    print('tetstrap: incorrect package group to install')
                    return

                path = pkg_parts[0]
                try:
                    name = pkg_parts[1]
                except IndexError:
                    name = False

                if not name:
                    if (Path(memu_path) / 'repository' / boot.version / 'programs' / path).exists():
                        pkgs = os.listdir(Path(memu_path) / 'repository' / boot.version / 'programs' / path)
                        
                        if 'memu_boot.py' in pkgs:
                            if memu.get_info(f'{tdisk}/memu/boot.py'):
                                print(f'memuboot.py is already installed - reinstalling')
                                memu.rm(f'{tdisk}/memu/boot.py')
                                memu.rm(f'{tdisk}/memu')
                            
                            memu.mk(tdisk, 'memu', 'folder', 'r')
                            memu.mk(f'{tdisk}/memu', 'boot.py', 'file', 'r')
                            with open((Path(memu_path) / 'repository' / boot.version / 'programs' / 'base' / 'memu_boot.py'), 'r') as f:
                                pkg_data = f.read()
                            memu.write_file(f'{tdisk}/memu/boot.py', pkg_data)
                            print(f'memuboot.py was successfully installed')
                            pkgs.pop(pkgs.index('memu_boot.py'))

                        if 'muskatos' in pkgs:
                            if memu.get_info(f'{tdisk}/usr') and memu.get_info(f'{tdisk}/config') and memu.get_info(f'{tdisk}/home') and memu.get_info(f'{tdisk}/root'):
                                print(f'muskatos is already installed - can\'t reinstall base directories and files')
                                return
                            else:
                                root_objects = [
                                    ('config', 'folder', 'r'),
                                    ('usr', 'folder', 'r'),
                                    ('home', 'folder', 'r'),
                                    ('root', 'folder', 'r')
                                ]
                                
                                for obj_name, obj_type, perms in root_objects:
                                    memu.mk(tdisk, obj_name, obj_type, perms)

                                objects = [
                                    (f'{tdisk}/config', 'hostname', 'file', 'r'),
                                    (f'{tdisk}/config', 'users.json', 'file', 'r'),
                                    (f'{tdisk}/usr', 'curr_user', 'file', 'r'),
                                    (f'{tdisk}/usr', 'cwd', 'file', 'r,w')
                                ]

                                for obj_path, obj_name, obj_type, perms in objects:
                                    memu.mk(obj_path, obj_name, obj_type, perms)

                                root_password = input('tetstrap: root password for your new system: ')                                
                                hostname = 'muskatos'
                                users = json.dumps({
                                    'root': {
                                        'password': root_password,
                                        'groups': ['users', 'sudoers', 'root'],
                                        'home': f'{tdisk}/root'
                                    }
                                })

                                memu.write_file(f'{tdisk}/config/users.json', users)
                                memu.write_file(f'{tdisk}/config/hostname', hostname)
                                print(f'muskatos was successfully installed')
                                pkgs.pop(pkgs.index('muskatos'))
                        
                        for pkg in pkgs:
                            if (Path(memu_path) / 'repository' / boot.version / 'programs' / path / pkg).exists() and pkg != 'memu_boot.py' and pkg != 'memu_boot_live.py' and pkg != 'tetstrap.py' and pkg != 'muskatos':
                                if memu.get_info(f'{tdisk}/programs/{pkg}'):
                                    print(f'{pkg} is already installed - reinstalling')
                                    memu.rm(f'{tdisk}/programs/{pkg}')

                                memu.mk(f'{tdisk}/programs', pkg, 'file', 'r')
                                with open((Path(memu_path) / 'repository' / boot.version / 'programs' / path / pkg), 'r') as f:
                                    pkg_data = f.read()
                                memu.write_file(f'{tdisk}/programs/{pkg}', pkg_data)
                                print(f'{pkg} was successfully installed')
                        return
                    else:
                        print('tetstrap: incorrect package path to install')
                        return

                if (Path(memu_path) / 'repository' / boot.version / 'programs' / path).exists():
                    if (Path(memu_path) / 'repository' / boot.version / 'programs' / path / f'{name}.py').exists() and f'{name}.py' != 'memu_boot.py' and f'{name}.py' != 'memu_boot_live.py' and f'{name}.py' != 'tetstrap.py':
                        pkg = f'{name}.py'

                        if memu.get_info(f'{tdisk}/programs/{pkg}'):
                            print(f'{pkg} is already installed - reinstalling')
                            memu.rm(f'{tdisk}/programs/{pkg}')

                        memu.mk(f'{tdisk}/programs', pkg, 'file', 'r')
                        with open((Path(memu_path) / 'repository' / boot.version / 'programs' / path / pkg), 'r') as f:
                            pkg_data = f.read()
                        memu.write_file(f'{tdisk}/programs/{pkg}', pkg_data)
                        print(f'{pkg} was successfully installed')
                    else:
                        print('tetstrap: incorrect package name to install')
                        return    
                else:
                    print('tetstrap: incorrect package path to install')
                    return

Tetstrap().tetstrap()
