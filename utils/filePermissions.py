import os
import platform

def change_permissions(path, mode):
    try:
        if not os.path.exists(path):
            print(f"File not found: {path}")
            return
        system = platform.system().lower()
        if system in ("linux", "darwin"):
            import pwd, grp
            root_uid = pwd.getpwnam("root").pw_uid
            root_gid = grp.getgrnam("root").gr_gid
            os.chown(path, root_uid, root_gid)
            os.chmod(path, mode)
        elif system == "windows":
            import stat, subprocess
            read_only = not bool(mode & stat.S_IWUSR)
            try:
                if read_only:
                    subprocess.run(
                        ["icacls", path, "/inheritance:r", "/grant", f"{os.getlogin()}:R"],
                        capture_output=True, text=True
                    )
                else:
                    subprocess.run(
                        ["icacls", path, "/grant", f"{os.getlogin()}:F"],
                        capture_output=True, text=True
                    )
            except Exception:
                print("Error: Could not apply permissions on Windows.")
        else:
            print("Unsupported operating system.")
    except Exception as e:
        print(f"An error occurred: {e}")
