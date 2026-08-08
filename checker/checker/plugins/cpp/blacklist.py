import os
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
    return [name for name in os.environ if name == "PATH" or name.startswith("NIX_")]