import dataclasses
import enum
import platform
import shutil
import pathlib
import urllib.request

from typing import (
    ClassVar, TypeVar, Type, Optional, Generic, cast
)


class UnsupportedHostPlatformError(Exception):
    pass


class OS(enum.Enum):
    macos = enum.auto()
    linux = enum.auto()
    windows = enum.auto()

    @property
    def is_posix(self) -> bool:
        return self != OS.windows

    @classmethod
    def current(cls) -> 'OS':
        return {
            'Darwin': cls.macos,
            'Linux': cls.linux,
            'Windows': cls.windows,
        }[platform.system()]


class Arch(enum.Enum):
    x86 = enum.auto()
    x86_64 = enum.auto()
    armv7 = enum.auto()
    aarch64 = enum.auto()

    @classmethod
    def current(cls) -> 'Arch':
        return {
            'x86_64': cls.x86_64,
            'arm64': cls.aarch64,
        }[platform.machine()]


@dataclasses.dataclass(frozen=True)
class Context:
    host_os: OS = OS.current()
    host_arch: Arch = Arch.current()

    target_os: OS = cast(OS, None)
    target_arch: Arch = cast(Arch, None)

    def __post_init__(self):
        if self.target_os is None:
            object.__setattr__(self, 'target_os', self.host_os)

        if self.target_arch is None:
            object.__setattr__(self, 'target_arch', self.host_arch)


@dataclasses.dataclass(frozen=True)
class Tools:
    cc: pathlib.Path
    cxx: pathlib.Path
    ar: pathlib.Path
    runlib: pathlib.Path
    nm: pathlib.Path
    ld: pathlib.Path

    cmake: pathlib.Path
    ninja: pathlib.Path


@dataclasses.dataclass(frozen=True)
class Toolchain:
    ctx: Context
    root: pathlib.Path
    tools: Tools

    cppflags: list[str]
    cflags: list[str]
    ccflags: list[str]
    cxxflags: list[str]
    ldflags: list[str]


@dataclasses.dataclass(frozen=True)
class SDK:
    root: pathlib.Path
    target_os: OS
    target_arch: Arch


def detect_archive_extensions():
    result = set()

    for _, extensions, _ in shutil.get_unpack_formats():
        result.update(extensions)

    return result


@dataclasses.dataclass(frozen=True)
class BaseBuildContext:
    distfiles: pathlib.Path
    srcs: pathlib.Path

    archive_extensions: ClassVar[set[str]] = detect_archive_extensions()

    def copytree(self, src: pathlib.Path, dest: pathlib.Path) -> None:
        return shutil.copytree(src, dest)

    def is_archive(self, path: pathlib.Path) -> bool:
        return path.name.endswith(tuple(self.archive_extensions))

    def unpack(self, src: pathlib.Path, *,
               dest: Optional[pathlib.Path] = None) -> None:
        if dest is None:
            dest = self.srcs

        if not self.is_archive(src):
            return

        shutil.unpack_archive(src, extract_dir=dest)


@dataclasses.dataclass(frozen=True)
class BuildContext(BaseBuildContext):
    context: Context

    toolchain: Toolchain
    sdk: SDK
    workdir: pathlib.Path
    destdir: pathlib.Path


T = TypeVar('T', bound='Recipy')


@dataclasses.dataclass(frozen=True)
class Recipy:
    name: ClassVar[str]

    version: str
    context: Context

    src_urls: dict[str, str] = dataclasses.field(
        init=False, default_factory=dict)
    provides_tools: dict[str, pathlib.Path] = dataclasses.field(
        init=False, default_factory=dict)
    build_deps: set[str] = dataclasses.field(
        init=False, default_factory=set)

    def __post_init__(self):
        self.__class__.setup(MutableRecipy(self))

    def setup(self):
        pass

    def fetch(self, ctx: BaseBuildContext):
        for filename, url in self.src_urls.items():
            path = ctx.distfiles / filename
            if path.exists():
                continue

            urllib.request.urlretrieve(url, filename=path)

    def unpack(self, ctx: BaseBuildContext):
        for filename in self.src_urls:
            path = ctx.distfiles / filename

            if ctx.is_archive(path):
                ctx.unpack(path, dest=ctx.srcs)

    def install(self, ctx: BuildContext):
        pass

    @classmethod
    def collect(cls: Type[T]) -> dict[str, Type[T]]:
        return {}


class MutableRecipy(Generic[T]):
    _recipy: T

    def __init__(self, recipy: T):
        super().__init__()
        object.__setattr__(self, '_recipy', recipy)

    def __setattr__(self, name, value):
        object.__setattr__(self._recipy, name, value)

    def __getattr__(self, name):
        return getattr(self._recipy, name)
