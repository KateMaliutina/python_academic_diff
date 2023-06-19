import pathlib
import typing as tp


def update_ref(gitdir: pathlib.Path, ref: tp.Union[str, pathlib.Path], new_value: str) -> None:
    file = (gitdir / ref).open("w")
    file.write(new_value)
    file.close()


def symbolic_ref(gitdir: pathlib.Path, name: str, ref: str) -> None:
    if ref_resolve(gitdir, ref):
        file = (gitdir / name).open("w")
        file.write(f"ref: {ref}")
        file.close()


def ref_resolve(gitdir: pathlib.Path, refname: str) -> tp.Optional[str]:
    if refname == "HEAD":
        refname = get_ref(gitdir)
    try:
        file = (gitdir / refname).open("r")
        out = file.read()
        file.close()
        return out
    except:
        return None


def resolve_head(gitdir: pathlib.Path) -> tp.Optional[str]:
    return ref_resolve(gitdir, "HEAD")


def is_detached(gitdir: pathlib.Path) -> bool:
    file = (gitdir / "HEAD").open("r")
    content = str(file.read())
    file.close()
    return "ref" not in content


def get_ref(gitdir: pathlib.Path) -> str:
    file = (gitdir / "HEAD").open("r")
    refname = file.read().split()[1]
    file.close()
    return refname
