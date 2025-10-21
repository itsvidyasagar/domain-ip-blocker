import subprocess

def run_command(command,expected_return_codes=[0]):
    try:
        result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
        )
        if not result.returncode in expected_return_codes:
            raise RuntimeError(f"{result.stderr.strip()}")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Command failed: {command}\nError: {e.stderr.strip()}")