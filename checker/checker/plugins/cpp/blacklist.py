import os
import shlex
from pathlib import Path


def get_cpp_blacklist(root: Path) -> list[str]:
    result = [".task.*"]
    for _ in range(5):
        result.append("*/" + result[-1])
    result.append("*private*")
    for _ in range(5):
        result.append("*/" + result[-1])
    return [str(root / p) for p in result]

def nix_toolchain_env() -> list[str]:
    return [name for name in ("PATH", "NIX_CFLAGS_COMPILE", "NIX_LDFLAGS") if name in os.environ]

def nix_compile_database_args() -> list[str]:
    return [f"--extra-arg={arg}" for arg in shlex.split(os.environ.get("NIX_CFLAGS_COMPILE", ""))]
