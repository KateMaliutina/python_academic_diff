import hashlib
import os
import pathlib
import struct
import typing as tp

from pyvcs.objects import hash_object


class GitIndexEntry(tp.NamedTuple):
    # @see: https://github.com/git/git/blob/master/Documentation/technical/index-format.txt
    ctime_s: int
    ctime_n: int
    mtime_s: int
    mtime_n: int
    dev: int
    ino: int
    mode: int
    uid: int
    gid: int
    size: int
    sha1: bytes
    flags: int
    name: str

    def pack(self) -> bytes:
        return struct.pack(
            f"!4L6i20sh{len(self.name)}s3x",
            *[
                self.ctime_s,
                self.ctime_n,
                self.mtime_s,
                self.mtime_n,
                self.dev,
                self.ino,
                self.mode,
                self.uid,
                self.gid,
                self.size,
                self.sha1,
                self.flags,
                self.name.encode(),
            ],
        )

    @staticmethod
    def unpack(data: bytes) -> "GitIndexEntry":
        unpacked = list(struct.unpack(f"!4L6i20sh{len(data) - 62}s", data))
        remove_fill = unpacked[len(unpacked) - 1]
        unpacked[len(unpacked) - 1] = remove_fill[: len(remove_fill) - 3].decode()
        return GitIndexEntry(*unpacked)


def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
    out = []
    try:
        file = open(gitdir / "index", "rb")
        data = file.read()
        length = int.from_bytes(data[8:12], "big")
        content = data[12: len(data) - 20]
        count = 0
        filler = b"\x00\x00\x00"
        for i in range(length):
            start = count + 62
            end = start + content[start:].find(filler) + 3
            out.append(GitIndexEntry.unpack(content[count:end]))
            count = end
        file.close()
        return out
    except:
        return out


def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    file = open(gitdir / "index", "wb")
    file.write(struct.pack("!4s2i", *[b"DIRC", 2, len(entries)]))
    hashed = struct.pack("!4s2i", *[b"DIRC", 2, len(entries)])
    for entry in entries:
        file.write(entry.pack())
        hashed += entry.pack()
    hashed = str(hashlib.sha1(hashed).hexdigest())  # type: ignore
    file.write(struct.pack(f"!{len(bytes.fromhex(hashed))}s", bytes.fromhex(hashed)))  # type: ignore
    file.close()


def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:
    files = read_index(gitdir)
    for file in files:
        if details:
            print(f"{oct(file.mode)[2:]} {file.sha1.hex()} 0	{file.name}")
        else:
            print(file.name)


def update_index(gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = True) -> None:
    if (gitdir / "index").exists():
        indexes = read_index(gitdir)
    else:
        indexes = []
    for path in paths:
        file = open(path, "rb")
        content = file.read()
        hashed = hash_object(content, fmt="blob", write=True)
        stat = os.stat(path)
        indexes.append(
            GitIndexEntry(
                ctime_s=int(stat.st_ctime),
                ctime_n=int(stat.st_ctime_ns) // 1000000000,
                mtime_s=int(stat.st_mtime),
                mtime_n=int(stat.st_mtime_ns) // 1000000000,
                dev=stat.st_dev,
                ino=stat.st_ino,
                mode=stat.st_mode,
                uid=stat.st_uid,
                gid=stat.st_gid,
                size=stat.st_size,
                sha1=bytes.fromhex(hashed),
                flags=7,
                name=str(path),
            )
        )
        file.close()
    indexes = sorted(indexes, key=lambda index: index.name)
    write_index(gitdir, indexes)
