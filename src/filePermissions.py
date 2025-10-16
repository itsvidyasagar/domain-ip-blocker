import os
import pwd
import grp

def changeMode(path, mode):
    try:
        root_uid = pwd.getpwnam("root").pw_uid
        root_gid = grp.getgrnam("root").gr_gid
        os.chown(path, root_uid, root_gid)
        os.chmod(path, mode)
    except PermissionError:
        print("Permission denied. Run the script as Administrator/with sudo.")
    except FileNotFoundError:
        print(f"File not found: {path}")
    except Exception as e:
        print(f"An error occurred: {e}")
