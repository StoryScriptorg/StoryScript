# `install_packages.py`
# This will install all dependencies required by StoryScript.
# Note: This script is used for People who wanted to Test StoryScript
# from main branch to test experimental features
# or people who wanted to run from source.

import sys
import platform

platform_check = bool(
    platform.system() == "Windows" and platform.version().startswith("10")
) or (platform.system() != "Windows")
bold = "\u001B[1m" if platform_check else ""
reset = "\u001B[0m" if platform_check else ""
red = "\u001B[31m" if platform_check else ""
green = "\u001B[32m" if platform_check else ""

print(f"{bold}Welcome to StoryScript dependencies installer.{reset}")

print("Required Python version: >3.6")
if sys.version_info.major < 3 or sys.version_info.minor < 6:
    print(
        f"You have: {red}{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}{reset}"
    )
    print("Version requirements not met. Requires Python 3.6 or greater. Exiting...")
    raise SystemExit
print(
    f"You have: {green}{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}{reset}"
)


def dependencies():
    print(
        """These dependencies will be installed:
 - NumPy (1.21.1)
 - Colorama (0.4.4)
Optional dependencies:
 - PyInstrument"""
    )
    while True:
        choice = (
            input(
                "Please select which package you'd like to install (all/required/optional): "
            )
        ).lower()
        if choice not in {"all", "required", "optional"}:
            print("Invalid choice.")
        else:
            break

    while True:
        inst = (
            input("Would you like to install with conda or pip? (default: pip): ")
        ).lower()
        if not inst:
            inst = "pip"
        if inst not in {"pip", "conda"}:
            print("Invalid choice.")
        else:
            break

    print("Begin installing process...")
    import subprocess

    if inst == "pip":
        if choice in {"optional", "all"}:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "pyinstrument"]
            )
            if choice == "optional":
                raise SystemExit
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "colorama==0.4.4"]
        )
        subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy==1.21.1"])
    elif inst == "conda":
        conda = input("Please type your conda path (default: conda):")
        if not conda:
            conda = "conda"
        if choice in {"optional", "all"}:
            subprocess.check_call([conda, "install", "-c", "pyc0d3r", "pyinstrument"])
            if choice == "optional":
                raise SystemExit
        subprocess.check_call([conda, "install", "numpy"])
        subprocess.check_call([conda, "install", "-c", "anaconda", "colorama"])
    raise SystemExit


dependencies()
