import os
import pathlib
import shutil
import typing as tp
from pyvcs.index import read_index, update_index
from pyvcs.objects import commit_parse, find_object, find_tree_files, read_object
from pyvcs.tree import commit_tree, write_tree


def add(gitdir: pathlib.Path, paths: tp.List[pathlib.Path]) -> None:
    update_index(gitdir, paths)


def commit(gitdir: pathlib.Path, message: str, author: tp.Optional[str] = None) -> str:
    return commit_tree(gitdir, write_tree(gitdir, read_index(gitdir)), message, author)


def checkout(gitdir: pathlib.Path, obj_name: str) -> None:
    head = gitdir / "refs/heads" / obj_name
    if head.exists():
        obj_name = head.read_text()  # type: ignore
    index = read_index(gitdir)
    for file in index:
        if pathlib.Path(file.name).is_file():
            name = file.name.split("/")
            if len(name) > 1:
                shutil.rmtree(name[0])
            else:
                os.chmod(file.name, 0o777)
                os.remove(file.name)
    path = gitdir / "objects" / obj_name[:2] / obj_name[2:]
    f = path.open("rb")
    data = f.read()
    f.close()
    hash_sum = commit_parse(data).decode()
    for file in find_tree_files(hash_sum, gitdir):  # type: ignore
        name = file[0].split("/")  # type: ignore
        if len(name) > 1:
            try:
                pathlib.Path(name[0]).absolute().mkdir()
            except:
                pass
        fmt, data = read_object(file[1], gitdir)  # type: ignore
        f = open(file[0], "w")  # type: ignore
        f.write(str(data, "utf-8"))  # type: ignore
        f.close()
