print('''commands:
    base:
        help - gives you some help
        echo <text> (optional) > <path> - types text or writes it into the file
        clear - clears the display
        poweroff - shuts down the system
        
    filesystem:
        cat <file> - shows file's content
        cd <directory> - moves you into specific directory
        chmod <permissions> <file> - gives file specific permissions
        cp <source file> <destination path> - copies file into specific directory
        ls (optional) path - shows every file in current directory
        mkdir <directory> - makes new directory
        mv <source file> <destination path> - moves file into specific directory
        pwd - shows current directory
        rm <file> - removes files
        rmdir <directory> - removes directories
        touch <file> - makes a new empty file
        
    users management:
        adduser <user> <groups> - creates new users
        passwd <user> - sets the user password
        rmuser <user> - removes users
        su <user> - logs into another users
        whoami - shows the current user\n''')
