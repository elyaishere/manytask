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

def nix_compile_database_response_file(build_dir: Path) -> str | None:
    flags = [
        f"--extra-arg={arg}"
        for name, value in os.environ.items()
        if name.startswith("NIX_CFLAGS_COMPILE")
        for arg in shlex.split(value)
    ]
    if not flags:
        return None

    response_file = build_dir / ".checker-nix-cflags.rsp"
    response_file.write_text("\n".join(map(shlex.quote, flags)) + "\n")
    return "@" + str(response_file)

def nix_toolchain_env() -> list[str]:
    return [name for name in os.environ if name == "PATH" or name.startswith("NIX_")]