import dataclasses
import pathlib

from ..recipy import (
    Recipy, BuildContext, OS,
    UnsupportedHostPlatformError,
)


@dataclasses.dataclass(frozen=True)
class CMakeBin(Recipy):
    name = 'cmake-bin'

    src_filename: str = dataclasses.field(init=False)
    src_dirname: str = dataclasses.field(init=False)

    def setup(self):
        if self.context.host_os == OS.macos:
            self.src_filename = f'cmake-{self.version}-macos-universal.tar.gz'
            self.src_dirname = f'cmake-{self.version}-macos-universal'
            cmake_path = pathlib.Path('CMake.app/Contents/bin/cmake')
        elif self.context.host_os == OS.linux:
            self.src_filename = (
                f'cmake-{self.version}-linux-'
                f'{self.context.host_arch.name}.tar.gz'
            )
            self.src_dirname = (
                f'cmake-{self.version}-linux-{self.context.host_arch.name}'
            )
            cmake_path = pathlib.Path('/bin/cmake')
        elif self.context.host_os == OS.windows:
            self.src_filename = (
                f'cmake-{self.version}-windows-'
                f'{self.context.host_arch.name}.zip'
            )
            self.src_dirname = (
                f'cmake-{self.version}-windows-{self.context.host_arch.name}'
            )
            cmake_path = pathlib.Path('/bin/cmake')
        else:
            raise UnsupportedHostPlatformError(
                f'{self.name} supports only linux, macos & windows host '
                f'platforms (host_os == {self.context.host_os.name!r}')

        self.src_urls[self.src_filename] = (
            'https://github.com/Kitware/CMake/releases/download/'
            f'v{self.version}/{self.src_filename}'
        )
        self.provides_tools['cmake'] = cmake_path
        self.build_deps.add('host-toolchain')

    def install(self, ctx: BuildContext):
        ctx.copytree(ctx.srcs / self.src_dirname, ctx.destdir)
