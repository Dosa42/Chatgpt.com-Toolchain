"""Configure real host SDKs, cross linkers, and request-specific native tools."""
from __future__ import annotations

import os
from pathlib import Path
import shutil
import sys
from .util import BuildError, RUST, read_json, run, within


def environment_key(triple):
    return triple.replace("-", "_").upper()


def android(context):
    options = context.request.get("platform", {})
    version = options.get("ndk_version", read_json(RUST / "toolchains/pins.json")["ndk"])
    sdk = context.env.get("ANDROID_SDK_ROOT") or context.env.get("ANDROID_HOME")
    if not sdk:
        raise BuildError("The Android SDK is required on the selected runner")
    ndk = Path(sdk) / "ndk" / version
    if not ndk.is_dir():
        manager = shutil.which("sdkmanager", path=context.env["PATH"])
        if not manager:
            candidates = sorted((Path(sdk) / "cmdline-tools").glob("*/bin/sdkmanager"))
            manager = str(candidates[-1]) if candidates else None
        if not manager:
            raise BuildError("sdkmanager was not found")
        run([manager, f"ndk;{version}"], env=context.env, log=context.log)
    api = options.get("android_api", 23)
    arch = context.target["android_clang"]
    tools = ndk / "toolchains/llvm/prebuilt/linux-x86_64/bin"
    clang = tools / f"{arch}{api}-clang"
    if not clang.is_file():
        raise BuildError("The configured Android NDK/API linker does not exist")
    key = environment_key(context.target["triple"])
    context.env[f"CARGO_TARGET_{key}_LINKER"] = str(clang)
    suffix = context.target["triple"].replace("-", "_")
    context.env[f"CC_{suffix}"] = str(clang)
    context.env[f"CXX_{suffix}"] = str(clang) + "++"
    context.env[f"AR_{suffix}"] = str(tools / "llvm-ar")
    context.env["ANDROID_NDK_HOME"] = str(ndk)
    context.env["ANDROID_NDK_ROOT"] = str(ndk)
    context.versions["android_ndk"] = version
    context.versions["android_api"] = api


def windows(context):
    if context.target["family"] != "windows-msvc":
        return
    installer = Path(context.env.get("ProgramFiles(x86)", "C:/Program Files (x86)")) / "Microsoft Visual Studio/Installer/vswhere.exe"
    if not installer.is_file():
        raise BuildError("Visual Studio vswhere is required for MSVC builds")
    location = run([str(installer), "-latest", "-products", "*", "-requires",
                    "Microsoft.VisualStudio.Component.VC.Tools.x86.x64", "-property", "installationPath"],
                   env=context.env, log=context.log).stdout.strip()
    batch = Path(location) / "Common7/Tools/VsDevCmd.bat"
    if not batch.is_file():
        raise BuildError("Visual Studio developer environment was not found")
    architecture = "arm64" if context.target["triple"].startswith("aarch64") else "x86" if context.target["triple"].startswith("i686") else "x64"
    # This is a fixed vendor environment initialization command; no request text is interpolated.
    script = context.work / "msvc-environment.cmd"
    script.write_text(
        f'@echo off\ncall "{batch}" -no_logo -arch={architecture} -host_arch=x64 >nul\n'
        'if errorlevel 1 exit /b %errorlevel%\nset\n', encoding="utf-8")
    response = run(["cmd.exe", "/d", "/c", "call", str(script)],
                   env=context.env, log=context.log)
    for line in response.stdout.splitlines():
        if "=" in line and not line.startswith("="):
            name, value = line.split("=", 1)
            context.env[name] = value
    for key in list(context.env):
        if key.lower() == "path" and key != "PATH":
            context.env["PATH"] = context.env.pop(key)
    context.versions["msvc_installation"] = location


def setup(context):
    runner = context.target["runner"]
    if runner.startswith("ubuntu") and not sys.platform.startswith("linux"):
        raise BuildError("This target requires a Linux runner")
    if runner.startswith("windows") and os.name != "nt":
        raise BuildError("This target requires a Windows runner")
    if runner.startswith("macos") and sys.platform != "darwin":
        raise BuildError("This target requires a macOS runner")
    packages = sorted(set(context.target.get("apt_packages", [])) |
                      set(context.request.get("platform", {}).get("apt_packages", [])))
    if packages:
        if not sys.platform.startswith("linux"):
            raise BuildError("apt_packages require a Linux runner")
        run(["sudo", "apt-get", "update"], env=context.env, log=context.log)
        run(["sudo", "apt-get", "install", "-y", "--no-install-recommends", *packages],
            env=context.env, log=context.log)
        context.versions["apt_packages"] = run(["dpkg-query", "-W", *packages],
                                               env=context.env, log=context.log).stdout.strip()
    for argv in context.request.get("platform", {}).get("setup_commands", []):
        run(argv, cwd=context.project, env=context.env, log=context.log)
    if context.target["family"] == "android":
        android(context)
    if context.target["family"] == "windows-msvc":
        windows(context)
    if context.target["family"] in ("macos", "apple-mobile"):
        developer = context.request.get("platform", {}).get("xcode_path")
        if developer:
            path = Path(developer)
            if not path.is_dir():
                raise BuildError("Requested Xcode installation does not exist")
            context.env["DEVELOPER_DIR"] = str(path)
        context.versions["xcode"] = run(["xcodebuild", "-version"], env=context.env,
                                         log=context.log).stdout.strip()
        if context.target.get("sdk"):
            context.env["SDKROOT"] = run(["xcrun", "--sdk", context.target["sdk"], "--show-sdk-path"],
                                          env=context.env, log=context.log).stdout.strip()
    options = context.request.get("platform", {})
    linker = options.get("linker") or context.target.get("linker")
    if linker:
        if not Path(linker).is_file() and not shutil.which(linker, path=context.env["PATH"]):
            raise BuildError(f"Configured linker is unavailable: {linker}")
        context.env[f"CARGO_TARGET_{environment_key(context.target['triple'])}_LINKER"] = linker
    if options.get("custom_target"):
        custom = within(context.project, options["custom_target"])
        if not custom.is_file():
            raise BuildError("Custom target JSON does not exist")
        read_json(custom)
        context.target_argument = str(custom)
    else:
        context.target_argument = context.target["triple"]
    context.env.update(context.request.get("environment", {}))
