import os
import getpass
from utils.command_runner import run_command
from src.constants import SYSTEM

def change_permissions(path, mode):
    try:
        if not os.path.exists(path):
            return
        system = SYSTEM
        if system in ("linux", "darwin"):
            import pwd, grp
            root_uid = pwd.getpwnam("root").pw_uid
            root_gid = grp.getgrnam("root").gr_gid
            os.chown(path, root_uid, root_gid)
            os.chmod(path, mode)
        elif system == "windows":
            import stat
            user = getpass.getuser()
            read_only = not bool(mode & stat.S_IWUSR)
            if read_only:
                run_command(f'icacls "{path}" /inheritance:r /grant {user}:R')
            else:
                run_command(f'icacls "{path}" /grant {user}:F')
        else:
            raise RuntimeError("Unsupported operating system.")
    except PermissionError:
        raise PermissionError("Permission denied. Run the script as Administrator/with sudo.")
    except Exception as e:
        raise Exception(f"{e}")
