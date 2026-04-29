import os
import subprocess
import sys


def main():
    configure_options = os.environ.get(
        "PETSC_CONFIGURE_OPTIONS",
        "--download-f2cblaslapack --with-debugging=0"
    )
    os.environ["PETSC_CONFIGURE_OPTIONS"] = configure_options

    subprocess.check_call([sys.executable, "-m", "pip", "install", "petsc", "petsc4py"])

    import petsc
    petsc_dir = petsc.get_petsc_dir()
    print(f"PETSC_DIR={petsc_dir}")

    subprocess.check_call([sys.executable, "-m", "pip", "install", "slepc", "slepc4py"], env={
        **os.environ,
        "PETSC_DIR": petsc_dir,
        "PETSC_ARCH": "",
    })

    import slepc
    slepc_dir = slepc.get_slepc_dir()
    print(f"SLEPC_DIR={slepc_dir}")

    github_env = os.environ.get("GITHUB_ENV")
    if github_env:
        with open(github_env, "a") as f:
            f.write(f"PETSC_DIR={petsc_dir}\n")
            f.write(f"PETSC_ARCH=\n")
            f.write(f"SLEPC_DIR={slepc_dir}\n")
        print("Written to GITHUB_ENV")


if __name__ == "__main__":
    main()