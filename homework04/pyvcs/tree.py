import pathlib
import time
import typing as tp
from pyvcs.index import GitIndexEntry
from pyvcs.objects import hash_object


def write_tree(gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = "") -> str:
    tree_content = b""
    for i in index:
        path = i.name.split("/")
        if len(path) > 1:
            tree_content += b"40000 "
            tree_content += path[0].encode() + b"\0"
            next_files = (
                    oct(i.mode)[2:].encode() + b" " + "/".join(path[1:]).encode() + b"\0" + i.sha1
            )
            hashed = hash_object(next_files, fmt="tree", write=True)
            tree_content += bytes.fromhex(hashed)
        else:
            file = path[0]
            tree_content += oct(i.mode)[2:].encode() + b" "
            tree_content += file.encode() + b"\0"
            tree_content += i.sha1
    return hash_object(tree_content, fmt="tree", write=True)


def commit_tree(
        gitdir: pathlib.Path,
        tree: str,
        message: str,
        parent: tp.Optional[str] = None,
        author: tp.Optional[str] = None,
) -> str:
    timestamp = int(time.mktime(time.localtime()))
    tz_sign = "+" if time.timezone < 0 else "-"
    tz_hours = abs(time.timezone // 3600)
    tz_hours = "0" + str(tz_hours) if tz_hours < 10 else tz_hours  # type: ignore
    tz_secs = abs((time.timezone // 60) % 60)
    tz_secs = "0" + str(tz_secs) if tz_secs < 10 else tz_secs  # type: ignore
    content_time = f"{timestamp} {tz_sign}{tz_hours}{tz_secs}"
    content = f"tree {tree}\n"
    if parent:
        content += f"parent {parent}\n"
    content += f"author {author} {content_time}\ncommitter {author} {content_time}\n\n{message}\n"
    hashed = hash_object(content.encode("ascii"), fmt="commit", write=True)
    return hashed
