import subprocess
from functools import lru_cache


@lru_cache(maxsize=1)
def get_version() -> str:
    for cmd in (
        ["git", "describe", "--tags", "--abbrev=0"],
        ["git", "rev-parse", "--short", "HEAD"],
    ):
        try:
            out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, text=True).strip()
            if out:
                return out
        except Exception:
            continue
    return "dev"