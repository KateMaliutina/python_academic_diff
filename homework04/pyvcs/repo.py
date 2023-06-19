import os
import pathlib
import typing as tp


def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:
    env_git = pathlib.Path(os.getenv("GIT_DIR")) if os.getenv("GIT_DIR") else pathlib.Path(".git")  # type: ignore
    # check if dir has git directory or parents have
    gitdir = workdir / env_git
    if not pathlib.Path(gitdir).exists():
        gitdir = ""  # type: ignore
        if pathlib.Path(workdir).parents:
            for path in workdir.parents:  # type: ignore
                if pathlib.Path.exists(path / env_git):
                    gitdir = path / env_git
            if gitdir == "":
                raise Exception("Not a git repository")
        else:
            raise Exception("Not a git repository")
    return gitdir


def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:
    env_git = pathlib.Path(os.getenv("GIT_DIR")) if os.getenv("GIT_DIR") else pathlib.Path(".git")  # type: ignore
    gitdir = workdir / env_git
    try:
        os.makedirs(f"{gitdir.resolve()}/objects", 0o777, exist_ok=True)
        (gitdir / "HEAD").write_text("ref: refs/heads/master\n")
        (gitdir / "config").write_text(
            "[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = false\n"
        )
        (gitdir / "description").write_text("Unnamed pyvcs repository.\n")
        os.makedirs(f"{gitdir.resolve()}/refs/heads", 0o777, exist_ok=True)
        os.makedirs(f"{gitdir.resolve()}/refs/tags", 0o777, exist_ok=True)
    except:
        raise Exception(f"{workdir} is not a directory")
    return gitdir
