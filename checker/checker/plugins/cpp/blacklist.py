import json
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

def prepare_nix_compile_database(build_dir: Path) -> None:
    flags = [
        arg
        for name, value in os.environ.items()
        if name.startswith("NIX_CFLAGS_COMPILE")
        for arg in shlex.split(value)
    ]
    compile_database = build_dir / "compile_commands.json"
    if not flags or not compile_database.exists():
        return

    commands = json.loads(compile_database.read_text())
    for command in commands:
        if "arguments" in command:
            command["arguments"].extend(flags)
        elif "command" in command:
            command["command"] += " " + shlex.join(flags)
    compile_database.write_text(json.dumps(commands, indent=2) + "\n")

def nix_toolchain_env() -> list[str]:
    return [name for name in os.environ if name == "PATH" or name.startswith("NIX_")]