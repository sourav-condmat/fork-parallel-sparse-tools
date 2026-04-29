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

    # Sanity check: verify petsc is visible
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

    # Print PETSc lib contents to diagnose linker issues
    petsc_lib = os.path.join(petsc_dir, "lib")
    print("PETSc lib contents:")
    for f in os.listdir(petsc_lib):
        print(" ", f)

    # Attempt slepc install
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "slepc", "slepc4py"],
        env=env,
        capture_output=False,  # let output stream directly to CI logs
    )

    # If slepc install failed, find and print configure.log
    if result.returncode != 0:
        print("\n--- Searching for SLEPc configure.log ---")
        find = subprocess.run(
            ["find", "/tmp", "-name", "configure.log", "-path", "*/slepc/*"],
            capture_output=True,
            text=True
        )
        log_paths = find.stdout.strip().split("\n") if find.stdout.strip() else []
        if log_paths:
            for log_path in log_paths:
                print(f"\n--- Contents of {log_path} (last 3000 chars) ---")
                try:
                    with open(log_path) as f:
                        content = f.read()
                        print(content[-3000:])
                except Exception as e:
                    print(f"Could not read log: {e}")
        else:
            print("No configure.log found")
        raise RuntimeError("slepc/slepc4py install failed — see logs above")

    github_env = os.environ.get("GITHUB_ENV")
    if github_env:
        import slepc
        slepc_dir = slepc.get_slepc_dir()
        with open(github_env, "a") as f:
            f.write(f"PETSC_DIR={petsc_dir}\n")
            f.write(f"PETSC_ARCH=\n")
            f.write(f"SLEPC_DIR={slepc_dir}\n")
        print(f"SLEPC_DIR={slepc_dir}")
        print("Written to GITHUB_ENV")


if __name__ == "__main__":
    main()