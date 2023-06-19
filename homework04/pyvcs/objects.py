import hashlib
import pathlib
import typing as tp
import zlib
from pyvcs.repo import repo_find


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    fmt_data = f"{fmt} {len(data)}\0".encode() + data
    hashed = hashlib.sha1(fmt_data).hexdigest()
    if write:
        root = repo_find()
        path = root / "objects" / hashed[:2]
        if not path.exists():
            path.mkdir(parents=True)
        file = path / hashed[2:]
        if not file.exists():
            file.write_bytes(zlib.compress(fmt_data))
    return hashed


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    root = gitdir / "objects" / obj_name[:2]
    if 4 <= len(obj_name) <= 40:
        objects = []
        for path in root.iterdir():
            el = find_object(obj_name, path)
            if el is not None:
                objects.append(str(el))
        if len(objects) == 0:
            raise Exception(f"Not a valid object name {obj_name}")
        return objects
    else:
        raise Exception(f"Not a valid object name {obj_name}")


def find_object(obj_name: str, gitdir: pathlib.Path) -> tp.Optional[str]:
    if obj_name[2:] in str(gitdir.parts[-1]):
        return f"{gitdir.parts[-2]}{gitdir.parts[-1]}"
    else:
        return None


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    file = gitdir / "objects" / sha[:2] / sha[2:]
    data = zlib.decompress(file.read_bytes())
    pivot = data.find(b"\x00")
    fmt = data[:pivot].split()[0]
    content = data[(pivot + 1):]
    return fmt.decode(), content


def read_tree(data: bytes) -> tp.List[tp.Dict[str, tp.Any]]:
    out = []
    while data != b"":
        ind = data.find(b" ")
        mode = int(str(data[:ind], "utf-8"))
        data = data[ind + 1:]
        ind = data.find(b"\x00")
        name = str(data[:ind], "utf-8")
        data = data[ind + 1:]
        hashed = bytes.hex(data[:20])
        data = data[20:]
        out.append({"mode": mode, "name": name, "hash": hashed})
    return out


def cat_file(obj_name: str, pretty: bool = True) -> None:
    root = repo_find()
    for obj in resolve_object(obj_name, root):
        fmt, data = read_object(obj, root)
        if fmt == "tree":
            result = ""
            tree_files = read_tree(data)
            for file in tree_files:
                result += f"{str(file['mode']).zfill(6)} {read_object(file['hash'], repo_find())[0]} {file['hash']}"
                result += "\t" + file["name"] + "\n"
            print(result)
        else:
            print(str(data, "utf-8"))


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    out = []
    fmt, data = read_object(tree_sha, gitdir)
    for file in read_tree(data):
        obj_format, obj_data = read_object(file["hash"], gitdir)
        if obj_format == "tree":
            tree = find_tree_files(file["hash"], gitdir)
            for f in tree:
                out.append((f"{file['name']}/{f[0]}", f[1]))
        else:
            out.append((file["name"], file["hash"]))
    return out


def commit_parse(raw: bytes, start: int = 0, dct=None):
    data = zlib.decompress(raw)
    index = data.find(b"tree")
    return data[index + 5: index + 45]
