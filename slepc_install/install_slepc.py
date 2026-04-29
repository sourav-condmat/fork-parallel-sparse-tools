import os
import subprocess
import sys


def main():
    configure_options = os.environ.get(
        "PETSC_CONFIGURE_OPTIONS",
        "--download-f2cblaslapack --with-debugging=0"
    )

    env = {**os.environ, "PETSC_CONFIGURE_OPTIONS": configure_options}

    subprocess.check_call([sys.executable, "-m", "pip", "install", "petsc", "petsc4py"], env=env)

    import petsc
    petsc_dir = petsc.get_petsc_dir()
    print(f"PETSC_DIR={petsc_dir}")

    env = {
        **env,
        "PETSC_DIR": petsc_dir,
        "PETSC_ARCH": "",
    }

    # Sanity check: verify petsc is visible before attempting slepc install
    check = subprocess.run(
        [sys.executable, "-c", "import petsc; print('petsc found at:', petsc.get_petsc_dir())"],
        env=env,
        capture_output=True,
        text=True
    )
    print("Sanity check stdout:", check.stdout)
    print("Sanity check stderr:", check.stderr)
    if check.returncode != 0:
        raise RuntimeError("petsc is not visible in the environment — aborting slepc install")

    subprocess.check_call([sys.executable, "-m", "pip", "install", "slepc", "slepc4py"], env=env)

    github_env = os.environ.get("GITHUB_ENV")
    if github_env:
        import slepc
        with open(github_env, "a") as f:
            f.write(f"PETSC_DIR={petsc_dir}\n")
            f.write(f"PETSC_ARCH=\n")
            f.write(f"SLEPC_DIR={slepc.get_slepc_dir()}\n")
        print("Written to GITHUB_ENV")


if __name__ == "__main__":
    main()