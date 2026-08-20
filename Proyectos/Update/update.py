#!/usr/bin/env python3
import os
import shutil
import subprocess
import sys


class Colors:
    GREEN = "\033[32m"
    BLUE = "\033[34m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    RESET = "\033[0m"


def log(msg: str):
    print(f"\n{Colors.BLUE}[*] {msg}{Colors.RESET}")


def success(msg: str):
    print(f"{Colors.GREEN}[✓] {msg}{Colors.RESET}")


def warn(msg: str):
    print(f"{Colors.YELLOW}[!] {msg}{Colors.RESET}")


def run_command(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    """Ejecuta un comando interactivo redirigiendo stdout/stderr."""
    return subprocess.run(cmd, check=check)


def update_mirrors():
    if shutil.which("reflector"):
        log("Actualizando y optimizando la lista de mirrors con Reflector...")
        # Selecciona los 5 mirrors más rápidos ordenados por tasa de transferencia
        run_command([
            "sudo", "reflector",
            "--latest", "5",
            "--sort", "rate",
            "--save", "/etc/pacman.d/mirrorlist",
        ])
        success("Mirrors actualizados y optimizados correctamente.")
    else:
        warn("Reflector no encontrado. Saltando optimización de mirrors.")


def update_packages():
    log("Actualizando paquetes oficiales y AUR...")
    if shutil.which("paru"):
        run_command(["paru", "-Syu"])
    elif shutil.which("yay"):
        run_command(["yay", "-Syu"])
    else:
        run_command(["sudo", "pacman", "-Syu"])
    success("Paquetes actualizados.")


def remove_orphans():
    log("Buscando paquetes huérfanos...")
    result = subprocess.run(
        ["pacman", "-Qtdq"],
        capture_output=True,
        text=True,
    )
    orphans = result.stdout.strip().splitlines()

    if orphans:
        run_command(["sudo", "pacman", "-Rns", *orphans])
        success(f"Eliminados {len(orphans)} paquete(s) huérfano(s).")
    else:
        success("No se encontraron paquetes huérfanos.")


def clean_cache():
    log("Limpiando caché de paquetes...")
    if shutil.which("paccache"):
        run_command(["sudo", "paccache", "-r"])
        run_command(["sudo", "paccache", "-ruk0"])
        success("Caché optimizada (conservadas últimas 3 versiones).")
    else:
        warn("paccache no disponible. Limpiando con pacman -Sc...")
        run_command(["sudo", "pacman", "-Sc", "--noconfirm"])


def check_kernel_reboot():
    try:
        running_kernel = os.uname().release.split("-")[0]
        result = subprocess.run(
            ["pacman", "-Q", "linux"],
            capture_output=True,
            text=True,
            check=True,
        )
        installed_kernel = result.stdout.strip().split()[1]

        if running_kernel not in installed_kernel:
            print(f"\n{Colors.RED}" + "-" * 50)
            print("[!] El Kernel fue actualizado. Se recomienda reiniciar.")
            print("-" * 50 + f"{Colors.RESET}")
    except subprocess.CalledProcessError:
        pass


def main():
    try:
        update_mirrors()
        update_packages()
        remove_orphans()
        clean_cache()
        check_kernel_reboot()
        success("¡Mantenimiento del sistema completado con éxito!")
    except subprocess.CalledProcessError as e:
        print(f"\n{Colors.RED}[X] Error al ejecutar: {' '.join(e.cmd)}{Colors.RESET}")
        sys.exit(e.returncode)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[!] Operación cancelada por el usuario.{Colors.RESET}")
        sys.exit(130)


if __name__ == "__main__":
    main()
