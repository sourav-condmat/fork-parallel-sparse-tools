import os
import subprocess
import sys


def main():
    configure_options = os.environ.get(
        "PETSC_CONFIGURE_OPTIONS",
        "--download-f2cblaslapack --with-debugging=0"
    )
    os.environ["PETSC_CONFIGURE_OPTIONS"] = configure_options

    # Install PETSc
    subprocess.check_call([sys.executable, "-m", "pip", "install", "petsc", "petsc4py"])

    # Import and set PETSC_DIR in current process so subprocesses inherit it
    import petsc
    petsc_dir = petsc.get_petsc_dir()
    os.environ["PETSC_DIR"] = petsc_dir
    os.environ["PETSC_ARCH"] = ""
    print(f"PETSC_DIR={petsc_dir}")

    # Install SLEPc — inherits PETSC_DIR from os.environ above
    subprocess.check_call([sys.executable, "-m", "pip", "install", "slepc", "slepc4py"])

    # Import and set SLEPC_DIR
    import slepc
    slepc_dir = slepc.get_slepc_dir()
    os.environ["SLEPC_DIR"] = slepc_dir
    print(f"SLEPC_DIR={slepc_dir}")

    # Write to GITHUB_ENV if running in CI
    github_env = os.environ.get("GITHUB_ENV")
    if github_env:
        with open(github_env, "a") as f:
            f.write(f"PETSC_DIR={petsc_dir}\n")
            f.write(f"PETSC_ARCH=\n")
            f.write(f"SLEPC_DIR={slepc_dir}\n")
        print("Written to GITHUB_ENV")


if __name__ == "__main__":
    main()