# tools
A set of scripts for building convinient llvm-toolchain and SDKs for later use.

Toolchain - a set of executable tools required for building code.

SDK - a set of files which technically not to required to build code if you
targeting baremetal. It is however required to build code for target OS and
with standard libraries.

Goal of these scripts is to reliably build a bunch of **universal** toolchains
which will be able to cross-compile software for any target platform (one
toolchain per host platform) and a bunch of SDKs which could be paired with
that toolchain to build software. Those toolchains/SDKs should be packed,
signed and cached in the s3 or other storage where they could be easily
accessed. That allows in any moment for any project to fetch from cache and
unpack toolchain for current host platform and SDK for all needed target
platforms and work on projects without wasting time on setting up tools.

I might also consider building additional tools for use with this sdk.
For example:
 - python distribution for windows;
 - ninja;

# Components

Toolchain will consist of:
 - llvm tools (ar, nm, objcopy, etc.);
 - clang & tools;

SDK will consist of:
 - libc++

Platform-dependent parts of SDK:

 - Linux: musl;
 - Windows: Windows SDK;
 - Apple OSes: $OSName.sdk from xcode;

# Platforms

I'm considering this set of target platforms:

 * MacOS (amd64, aarch64);
 * MacOS Catalyst (amd64, aarch64);
 * iOS (armv7, aarch64);
 * iOSSim (amd64, aarch64);
 * tvOS (armv7, aarch64);
 * tvOSSim (amd64, aarch64);
 * watchOS (armv7, aarch64);
 * watchOSSim (amd64, aarch64);
 * Linux (x86, amd64, armv7, aarch64, more to add);
 * Windows (x86, amd64, armv7, aarch64);

And this set of host platforms:

 * MacOS (amd64, aarch64);
 * Linux (x86, amd64, armv7, aarch64);
 * Windows (x86, amd64);

# TODOs

 - Sources downloader
 - Sources unpacker
 - Build bootstrap toolchain
 - Build bootstrap SDKs
 - Build universal toolchain
 - Build final SDKs
 - Package everything
 - Sign packages
 - Cache packages
 - fs cache backend
 - s3 cache backend
 - Fetch packages from cache
 - Generate per-platform configurations
 - Sandbox the build of each part to make sure it's hermetic
