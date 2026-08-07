# AstraSage Pip Manager
# python/pip/pip.py
#
# AstraSage'in pip yönetim modülü.
#
# Desteklenen işlemler:
#   - pip tespiti
#   - pip sürümü
#   - paket kurma
#   - paket kaldırma
#   - paket güncelleme
#   - paket listesi
#   - paket bilgisi
#   - pip kontrolü
#   - hata kayıt sistemi
#
# Hata kayıtları:
#
#   python/pip/logs/error_log[TARİH].json
#
# Örnek:
#
#   python/pip/logs/error_log[2026-08-06_14-32-51].json
#
# NOT:
# Bu modül sistemdeki gerçek pip executable'ını kullanır.
# AstraSage kendi pip'ini yeniden uygulamaya çalışmaz.


import os
import sys
import json
import shutil
import subprocess
import platform
from datetime import datetime


# ============================================================
# AstraSage Pip ayarları
# ============================================================

PIP_MODULE_NAME = "AstraSage Pip"


# ============================================================
# Klasörler
# ============================================================

CURRENT_FILE = os.path.abspath(__file__)

PIP_ROOT = os.path.dirname(
    CURRENT_FILE
)

LOG_FOLDER = os.path.join(
    PIP_ROOT,
    "logs"
)


# ============================================================
# Renkler
# ============================================================

class Colors:
    RESET = "\033[0m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    WHITE = "\033[97m"
    BOLD = "\033[1m"


# ============================================================
# Yazdırma yardımcıları
# ============================================================

def _ok(message):
    print(
        f"{Colors.GREEN}[✓]{Colors.RESET} {message}"
    )


def _warning(message):
    print(
        f"{Colors.YELLOW}[!]{Colors.RESET} {message}"
    )


def _error(message):
    print(
        f"{Colors.RED}[✗]{Colors.RESET} {message}"
    )


def _checking(message):
    print(
        f"{Colors.CYAN}[*]{Colors.RESET} {message}"
    )


def _info(label, value):
    print(
        f"    {label:<15}: {value}"
    )


# ============================================================
# Log klasörü
# ============================================================

def ensure_log_folder():
    """
    Pip log klasörünü oluşturur.
    """

    try:

        os.makedirs(
            LOG_FOLDER,
            exist_ok=True
        )

        return True

    except OSError as exc:

        _error(
            f"Could not create pip log folder: {exc}"
        )

        return False


# ============================================================
# Hata logu
# ============================================================

def log_error(
    operation,
    error=None,
    command=None,
    returncode=None,
    stdout=None,
    stderr=None,
    package=None,
    extra=None
):
    """
    Pip hatasını JSON dosyasına kaydeder.

    Dosya formatı:

        error_log[YYYY-MM-DD_HH-MM-SS].json
    """

    ensure_log_folder()

    now = datetime.now()

    timestamp = now.strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    filename = (
        f"error_log[{timestamp}].json"
    )

    log_path = os.path.join(
        LOG_FOLDER,
        filename
    )

    log_data = {
        "astra_sage": {
            "module": PIP_MODULE_NAME,
            "timestamp": now.isoformat(),
        },

        "system": {
            "platform": platform.system(),
            "platform_release": platform.release(),
            "machine": platform.machine(),
            "architecture": platform.architecture()[0],
            "python_version": platform.python_version(),
        },

        "operation": operation,

        "package": package,

        "command": command,

        "returncode": returncode,

        "error": error,

        "stdout": stdout,

        "stderr": stderr,

        "extra": extra,
    }

    try:

        with open(
            log_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                log_data,
                file,
                indent=4,
                ensure_ascii=False
            )

        print(
            f"{Colors.YELLOW}[log]{Colors.RESET} "
            f"Error saved: {log_path}"
        )

        return log_path

    except Exception as exc:

        _error(
            f"Could not save pip error log: {exc}"
        )

        return None


# ============================================================
# Pip executable bulma
# ============================================================

def find_pip():
    """
    Sistemdeki pip executable'ını bulur.

    Öncelik:

        1. Python -m pip
        2. pip3
        3. pip
    """

    # --------------------------------------------------------
    # Python ile pip
    # --------------------------------------------------------

    python_path = sys.executable

    if python_path:

        try:

            result = subprocess.run(
                [
                    python_path,
                    "-m",
                    "pip",
                    "--version"
                ],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:

                return {
                    "type": "python_module",
                    "executable": python_path,
                    "command": [
                        python_path,
                        "-m",
                        "pip"
                    ]
                }

        except Exception:
            pass

    # --------------------------------------------------------
    # pip3
    # --------------------------------------------------------

    pip3 = shutil.which(
        "pip3"
    )

    if pip3:

        return {
            "type": "executable",
            "executable": pip3,
            "command": [
                pip3
            ]
        }

    # --------------------------------------------------------
    # pip
    # --------------------------------------------------------

    pip = shutil.which(
        "pip"
    )

    if pip:

        return {
            "type": "executable",
            "executable": pip,
            "command": [
                pip
            ]
        }

    return None


# ============================================================
# Pip mevcut mu?
# ============================================================

def is_pip_available():
    """
    Pip kullanılabilir mi?
    """

    return find_pip() is not None


# ============================================================
# Pip sürümü
# ============================================================

def get_pip_version():
    """
    Pip sürümünü döndürür.
    """

    pip = find_pip()

    if pip is None:
        return None

    command = pip["command"] + [
        "--version"
    ]

    try:

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:

            log_error(
                operation="version",
                command=command,
                returncode=result.returncode,
                stdout=result.stdout,
                stderr=result.stderr
            )

            return None

        output = (
            result.stdout.strip()
            or result.stderr.strip()
        )

        return output

    except Exception as exc:

        log_error(
            operation="version",
            command=command,
            error=str(exc)
        )

        return None


# ============================================================
# Pip komutu çalıştırma
# ============================================================

def run_pip(
    arguments,
    operation="unknown",
    package=None
):
    """
    Genel pip komut çalıştırıcısı.

    Bütün pip işlemleri mümkün olduğunca bu fonksiyondan
    geçirilir.

    Hata olursa otomatik olarak JSON log oluşturulur.
    """

    pip = find_pip()

    if pip is None:

        error_message = (
            "pip executable was not found."
        )

        _error(
            error_message
        )

        log_error(
            operation=operation,
            error=error_message,
            package=package
        )

        return {
            "success": False,
            "returncode": None,
            "stdout": "",
            "stderr": error_message,
        }

    if isinstance(
        arguments,
        str
    ):

        arguments = [
            arguments
        ]

    command = (
        pip["command"]
        + list(arguments)
    )

    _checking(
        "Running pip command..."
    )

    try:

        result = subprocess.run(
            command,
            text=True
        )

        success = (
            result.returncode == 0
        )

        if success:

            _ok(
                "Pip command completed."
            )

        else:

            _error(
                "Pip command failed."
            )

            log_error(
                operation=operation,
                command=command,
                returncode=result.returncode,
                package=package
            )

        return {
            "success": success,
            "returncode": result.returncode,
        }

    except KeyboardInterrupt:

        error_message = (
            "Pip operation interrupted."
        )

        _warning(
            error_message
        )

        log_error(
            operation=operation,
            command=command,
            error=error_message,
            package=package,
            extra={
                "reason": "KeyboardInterrupt"
            }
        )

        return {
            "success": False,
            "returncode": 130,
            "error": error_message,
        }

    except Exception as exc:

        _error(
            f"Pip execution error: {exc}"
        )

        log_error(
            operation=operation,
            command=command,
            error=str(exc),
            package=package
        )

        return {
            "success": False,
            "returncode": None,
            "error": str(exc),
        }


# ============================================================
# Paket kurma
# ============================================================

def install(
    package,
    upgrade=False
):
    """
    Python paketi kurar.

    Örnek:

        install("requests")

    veya:

        install("requests", upgrade=True)
    """

    if not package:

        _error(
            "Package name is required."
        )

        return {
            "success": False
        }

    arguments = [
        "install"
    ]

    if upgrade:

        arguments.append(
            "--upgrade"
        )

    arguments.append(
        package
    )

    return run_pip(
        arguments,
        operation="install",
        package=package
    )


# ============================================================
# Paket kaldırma
# ============================================================

def uninstall(package):
    """
    Python paketini kaldırır.
    """

    if not package:

        _error(
            "Package name is required."
        )

        return {
            "success": False
        }

    return run_pip(
        [
            "uninstall",
            "-y",
            package
        ],
        operation="uninstall",
        package=package
    )


# ============================================================
# Paket güncelleme
# ============================================================

def upgrade(package):
    """
    Python paketini günceller.
    """

    if not package:

        _error(
            "Package name is required."
        )

        return {
            "success": False
        }

    return install(
        package,
        upgrade=True
    )


# ============================================================
# Tüm paketleri güncelleme
# ============================================================

def upgrade_all():
    """
    Sistemdeki pip paketlerini günceller.

    NOT:
    Paketlerin tek tek güncellenmesi pip tarafından
    gerçekleştirilir.
    """

    return run_pip(
        [
            "install",
            "--upgrade",
            "-r",
            "requirements.txt"
        ],
        operation="upgrade_all"
    )


# ============================================================
# Paket listesi
# ============================================================

def list_packages():
    """
    Kurulu Python paketlerini listeler.
    """

    return run_pip(
        [
            "list"
        ],
        operation="list"
    )


# ============================================================
# Paket bilgisi
# ============================================================

def package_info(package):
    """
    Paket hakkında bilgi gösterir.
    """

    if not package:

        _error(
            "Package name is required."
        )

        return {
            "success": False
        }

    return run_pip(
        [
            "show",
            package
        ],
        operation="show",
        package=package
    )


# ============================================================
# Paket kontrolü
# ============================================================

def check_packages():
    """
    Paket bağımlılıklarında problem olup olmadığını kontrol eder.

    pip check kullanılır.
    """

    return run_pip(
        [
            "check"
        ],
        operation="check"
    )


# ============================================================
# Requirements oluşturma
# ============================================================

def freeze(output_file=None):
    """
    Kurulu paketleri requirements formatında alır.

    output_file verilirse dosyaya kaydeder.
    """

    pip = find_pip()

    if pip is None:

        error_message = (
            "pip executable was not found."
        )

        _error(
            error_message
        )

        log_error(
            operation="freeze",
            error=error_message
        )

        return {
            "success": False
        }

    command = (
        pip["command"]
        + [
            "freeze"
        ]
    )

    try:

        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:

            _error(
                "pip freeze failed."
            )

            log_error(
                operation="freeze",
                command=command,
                returncode=result.returncode,
                stdout=result.stdout,
                stderr=result.stderr
            )

            return {
                "success": False,
                "returncode": result.returncode,
            }

        output = result.stdout

        if output_file:

            output_file = os.path.abspath(
                os.path.expanduser(
                    output_file
                )
            )

            try:

                os.makedirs(
                    os.path.dirname(
                        output_file
                    ),
                    exist_ok=True
                )

                with open(
                    output_file,
                    "w",
                    encoding="utf-8"
                ) as file:

                    file.write(
                        output
                    )

                _ok(
                    f"Requirements saved: "
                    f"{output_file}"
                )

            except Exception as exc:

                _error(
                    f"Could not save requirements: "
                    f"{exc}"
                )

                log_error(
                    operation="freeze",
                    command=command,
                    error=str(exc),
                    extra={
                        "output_file": output_file
                    }
                )

                return {
                    "success": False,
                    "returncode": 0,
                }

        else:

            print(
                output,
                end=""
            )

        return {
            "success": True,
            "returncode": 0,
            "output": output,
        }

    except Exception as exc:

        _error(
            f"pip freeze error: {exc}"
        )

        log_error(
            operation="freeze",
            command=command,
            error=str(exc)
        )

        return {
            "success": False,
            "error": str(exc),
        }


# ============================================================
# Pip Doctor
# ============================================================

def doctor():
    """
    Pip ortamını kontrol eder.
    """

    print()

    print(
        f"{Colors.BOLD}{Colors.CYAN}"
        "╭──────── AstraSage Pip Doctor ────────╮"
        f"{Colors.RESET}"
    )

    # --------------------------------------------------------
    # Pip
    # --------------------------------------------------------

    pip = find_pip()

    if pip is None:

        _error(
            "pip was not found."
        )

        log_error(
            operation="doctor",
            error="pip was not found."
        )

        print(
            f"{Colors.BOLD}{Colors.CYAN}"
            "╰──────────────────────────────────────╯"
            f"{Colors.RESET}"
        )

        return False

    _ok(
        "pip detected."
    )

    _info(
        "Executable",
        pip["executable"]
    )

    _info(
        "Type",
        pip["type"]
    )

    # --------------------------------------------------------
    # Version
    # --------------------------------------------------------

    version = get_pip_version()

    if version:

        _ok(
            "pip version detected."
        )

        _info(
            "Version",
            version
        )

    else:

        _warning(
            "Could not determine pip version."
        )

    # --------------------------------------------------------
    # pip check
    # --------------------------------------------------------

    print()

    _checking(
        "Checking installed package dependencies..."
    )

    result = check_packages()

    if result.get(
        "success"
    ):

        _ok(
            "Package dependency check passed."
        )

    else:

        _warning(
            "Package dependency check reported a problem."
        )

    print(
        f"{Colors.BOLD}{Colors.CYAN}"
        "╰──────────────────────────────────────╯"
        f"{Colors.RESET}"
    )

    return (
        result.get(
            "success",
            False
        )
    )


# ============================================================
# Pip bilgi paneli
# ============================================================

def pip_info():
    """
    AstraSage Pip bilgi panelini gösterir.
    """

    print()

    print(
        f"{Colors.BOLD}{Colors.MAGENTA}"
        "╭────────── AstraSage Pip ───────────╮"
        f"{Colors.RESET}"
    )

    pip = find_pip()

    if pip is None:

        _error(
            "pip not found."
        )

        print(
            f"{Colors.BOLD}{Colors.MAGENTA}"
            "╰───────────────────────────────────╯"
            f"{Colors.RESET}"
        )

        return {
            "available": False
        }

    _ok(
        "pip detected."
    )

    _info(
        "Executable",
        pip["executable"]
    )

    _info(
        "Type",
        pip["type"]
    )

    version = get_pip_version()

    if version:

        _info(
            "Version",
            version
        )

    _info(
        "Log folder",
        LOG_FOLDER
    )

    print(
        f"{Colors.BOLD}{Colors.MAGENTA}"
        "╰───────────────────────────────────╯"
        f"{Colors.RESET}"
    )

    return {
        "available": True,
        "executable": pip["executable"],
        "type": pip["type"],
        "version": version,
        "log_folder": LOG_FOLDER,
    }


# ============================================================
# Pip komut yöneticisi
# ============================================================

def run_pip_command(
    subcommand=None,
    args=None
):
    """
    AstraSage pip komut yöneticisi.

    Örnek:

        as pip
        as pip info
        as pip --version
        as pip doctor
        as pip install requests
        as pip uninstall requests
        as pip upgrade requests
        as pip list
        as pip show requests
        as pip check
        as pip freeze
    """

    if subcommand is None:

        subcommand = "info"

    subcommand = str(
        subcommand
    ).lower()

    args = args or []

    # ========================================================
    # info
    # ========================================================

    if subcommand == "info":

        return pip_info()

    # ========================================================
    # version
    # ========================================================

    if subcommand in (
        "version",
        "--version",
        "-v"
    ):

        version = get_pip_version()

        if version:

            print(
                version
            )

            return version

        _error(
            "pip was not found."
        )

        return None

    # ========================================================
    # doctor
    # ========================================================

    if subcommand == "doctor":

        return doctor()

    # ========================================================
    # install
    # ========================================================

    if subcommand == "install":

        if not args:

            _error(
                "Usage: as pip install <package>"
            )

            return None

        package = args[0]

        return install(
            package
        )

    # ========================================================
    # uninstall
    # ========================================================

    if subcommand in (
        "uninstall",
        "remove"
    ):

        if not args:

            _error(
                "Usage: as pip uninstall <package>"
            )

            return None

        package = args[0]

        return uninstall(
            package
        )

    # ========================================================
    # upgrade
    # ========================================================

    if subcommand in (
        "upgrade",
        "update"
    ):

        if not args:

            _error(
                "Usage: as pip upgrade <package>"
            )

            return None

        package = args[0]

        return upgrade(
            package
        )

    # ========================================================
    # list
    # ========================================================

    if subcommand == "list":

        return list_packages()

    # ========================================================
    # show
    # ========================================================

    if subcommand in (
        "show",
        "info-package"
    ):

        if not args:

            _error(
                "Usage: as pip show <package>"
            )

            return None

        package = args[0]

        return package_info(
            package
        )

    # ========================================================
    # check
    # ========================================================

    if subcommand == "check":

        return check_packages()

    # ========================================================
    # freeze
    # ========================================================

    if subcommand == "freeze":

        if args:

            return freeze(
                args[0]
            )

        return freeze()

    # ========================================================
    # Unknown
    # ========================================================

    _error(
        f"Unknown pip command: {subcommand}"
    )

    print()

    print(
        "Available commands:"
    )

    print(
        "  as pip info"
    )

    print(
        "  as pip --version"
    )

    print(
        "  as pip doctor"
    )

    print(
        "  as pip install <package>"
    )

    print(
        "  as pip uninstall <package>"
    )

    print(
        "  as pip upgrade <package>"
    )

    print(
        "  as pip list"
    )

    print(
        "  as pip show <package>"
    )

    print(
        "  as pip check"
    )

    print(
        "  as pip freeze"
    )

    return None


# ============================================================
# Test
# ============================================================

if __name__ == "__main__":

    arguments = sys.argv[1:]

    if not arguments:

        run_pip_command(
            "info"
        )

    else:

        run_pip_command(
            arguments[0],
            arguments[1:]
        )