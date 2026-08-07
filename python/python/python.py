# AstraSage Python Manager
# python/python.py
#
# AstraSage'in Python çalışma modülü.
#
# Görevleri:
#   - Python interpreter bulma
#   - Python sürümünü öğrenme
#   - Python dosyası çalıştırma
#   - Python kodu çalıştırma
#   - Python bilgilerini gösterme
#   - Python'un kullanılabilir olup olmadığını kontrol etme
#
# Bu modül pip işlemlerini yönetmez.
# Pip işlemleri python/pip/ altında tutulacaktır.


import os
import sys
import shutil
import subprocess
import platform


# ============================================================
# AstraSage Python bilgileri
# ============================================================

PYTHON_MODULE_NAME = "AstraSage Python"


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


def _info(label, value):
    print(
        f"    {label:<14}: {value}"
    )


# ============================================================
# Python executable bulma
# ============================================================

def find_python():
    """
    Sistemde kullanılabilecek Python executable'ını bulur.

    Öncelik:
        1. sys.executable
        2. python3
        3. python
    """

    # --------------------------------------------------------
    # AstraSage'in çalıştığı Python
    # --------------------------------------------------------

    if sys.executable:
        if os.path.isfile(sys.executable):
            return sys.executable

    # --------------------------------------------------------
    # python3
    # --------------------------------------------------------

    python3 = shutil.which("python3")

    if python3:
        return python3

    # --------------------------------------------------------
    # python
    # --------------------------------------------------------

    python = shutil.which("python")

    if python:
        return python

    return None


# ============================================================
# Python kontrolü
# ============================================================

def is_python_available():
    """
    Python interpreter kullanılabilir mi?
    """

    return find_python() is not None


# ============================================================
# Python sürümü
# ============================================================

def get_python_version(python_path=None):
    """
    Python sürümünü döndürür.

    Örnek:
        3.13.5
    """

    if python_path is None:
        python_path = find_python()

    if python_path is None:
        return None

    try:

        result = subprocess.run(
            [
                python_path,
                "--version"
            ],
            capture_output=True,
            text=True,
            timeout=10
        )

        output = (
            result.stdout.strip()
            or result.stderr.strip()
        )

        if output.startswith("Python "):
            return output[7:]

        return output

    except (
        OSError,
        subprocess.SubprocessError
    ):
        return None


# ============================================================
# Python executable bilgisi
# ============================================================

def get_python_executable():
    """
    Aktif Python executable yolunu döndürür.
    """

    return find_python()


# ============================================================
# Python platform bilgisi
# ============================================================

def get_python_platform():
    """
    Python'un çalıştığı platformu döndürür.
    """

    return {
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "architecture": platform.architecture()[0],
        "python_implementation": platform.python_implementation(),
    }


# ============================================================
# Python sys.path
# ============================================================

def get_python_paths():
    """
    Aktif Python import path listesini döndürür.

    subprocess kullanmadan AstraSage'in çalıştığı
    Python ortamını gösterir.
    """

    return list(sys.path)


# ============================================================
# Python modülü kontrolü
# ============================================================

def module_exists(
    module_name,
    python_path=None
):
    """
    Bir Python modülünün mevcut olup olmadığını kontrol eder.

    Örnek:
        module_exists("requests")
        module_exists("numpy")
    """

    if not module_name:
        return False

    if python_path is None:
        python_path = find_python()

    if python_path is None:
        return False

    try:

        result = subprocess.run(
            [
                python_path,
                "-c",
                (
                    "import importlib.util; "
                    f"print(importlib.util.find_spec("
                    f"{module_name!r}) is not None)"
                )
            ],
            capture_output=True,
            text=True,
            timeout=10
        )

        return (
            result.returncode == 0
            and result.stdout.strip() == "True"
        )

    except (
        OSError,
        subprocess.SubprocessError
    ):
        return False


# ============================================================
# Python kodu çalıştırma
# ============================================================

def execute_code(
    code,
    python_path=None,
    cwd=None
):
    """
    Verilen Python kodunu çalıştırır.

    Örnek:

        execute_code(
            "print('Hello AstraSage')"
        )
    """

    if python_path is None:
        python_path = find_python()

    if python_path is None:

        _error(
            "Python interpreter not found."
        )

        return {
            "success": False,
            "returncode": None,
            "stdout": "",
            "stderr": "",
        }

    if not isinstance(code, str):
        code = str(code)

    try:

        result = subprocess.run(
            [
                python_path,
                "-c",
                code
            ],
            cwd=cwd,
            text=True
        )

        return {
            "success": result.returncode == 0,
            "returncode": result.returncode,
        }

    except (
        OSError,
        subprocess.SubprocessError
    ) as exc:

        _error(
            f"Could not execute Python: {exc}"
        )

        return {
            "success": False,
            "returncode": None,
            "error": str(exc),
        }


# ============================================================
# Python dosyası çalıştırma
# ============================================================

def run_file(
    file_path,
    python_path=None,
    cwd=None,
    args=None
):
    """
    Python dosyasını çalıştırır.

    Örnek:

        run_file("main.py")

    Argüman:

        run_file(
            "main.py",
            args=["hello", "world"]
        )
    """

    if python_path is None:
        python_path = find_python()

    if python_path is None:

        _error(
            "Python interpreter not found."
        )

        return {
            "success": False,
            "returncode": None,
        }

    file_path = os.path.abspath(
        os.path.expanduser(file_path)
    )

    # --------------------------------------------------------
    # Dosya kontrolü
    # --------------------------------------------------------

    if not os.path.exists(file_path):

        _error(
            f"Python file does not exist: "
            f"{file_path}"
        )

        return {
            "success": False,
            "returncode": None,
            "reason": "File does not exist.",
        }

    if not os.path.isfile(file_path):

        _error(
            f"Target is not a file: "
            f"{file_path}"
        )

        return {
            "success": False,
            "returncode": None,
            "reason": "Target is not a file.",
        }

    # --------------------------------------------------------
    # Python uzantısı
    # --------------------------------------------------------

    if not file_path.lower().endswith(".py"):

        _warning(
            "Target does not have a .py extension."
        )

    command = [
        python_path,
        file_path
    ]

    # --------------------------------------------------------
    # Argümanlar
    # --------------------------------------------------------

    if args:

        if isinstance(args, str):
            args = [args]

        command.extend(
            str(argument)
            for argument in args
        )

    # --------------------------------------------------------
    # Çalıştır
    # --------------------------------------------------------

    try:

        result = subprocess.run(
            command,
            cwd=cwd
        )

        return {
            "success": result.returncode == 0,
            "returncode": result.returncode,
        }

    except KeyboardInterrupt:

        _warning(
            "Python process interrupted."
        )

        return {
            "success": False,
            "returncode": 130,
            "reason": "Interrupted.",
        }

    except (
        OSError,
        subprocess.SubprocessError
    ) as exc:

        _error(
            f"Could not run Python file: {exc}"
        )

        return {
            "success": False,
            "returncode": None,
            "error": str(exc),
        }


# ============================================================
# Python shell
# ============================================================

def start_python_shell(
    python_path=None,
    cwd=None
):
    """
    Etkileşimli Python shell başlatır.

    as python shell
    """

    if python_path is None:
        python_path = find_python()

    if python_path is None:

        _error(
            "Python interpreter not found."
        )

        return False

    try:

        result = subprocess.run(
            [
                python_path,
                "-i"
            ],
            cwd=cwd
        )

        return result.returncode == 0

    except KeyboardInterrupt:

        return True

    except (
        OSError,
        subprocess.SubprocessError
    ) as exc:

        _error(
            f"Could not start Python shell: {exc}"
        )

        return False


# ============================================================
# Python info
# ============================================================

def python_info():
    """
    AstraSage Python bilgi panelini gösterir.
    """

    python_path = find_python()

    print()

    print(
        f"{Colors.BOLD}{Colors.CYAN}"
        "╭──────── AstraSage Python ─────────╮"
        f"{Colors.RESET}"
    )

    # --------------------------------------------------------
    # Interpreter
    # --------------------------------------------------------

    if python_path:

        _ok(
            "Python interpreter detected"
        )

        _info(
            "Executable",
            python_path
        )

    else:

        _error(
            "Python interpreter not found"
        )

        print(
            f"{Colors.BOLD}{Colors.CYAN}"
            "╰───────────────────────────────────╯"
            f"{Colors.RESET}"
        )

        return {
            "available": False
        }

    # --------------------------------------------------------
    # Version
    # --------------------------------------------------------

    version = get_python_version(
        python_path
    )

    if version:

        _info(
            "Version",
            version
        )

    # --------------------------------------------------------
    # Platform
    # --------------------------------------------------------

    information = get_python_platform()

    _info(
        "System",
        information["system"]
    )

    _info(
        "Release",
        information["release"]
    )

    _info(
        "Machine",
        information["machine"]
    )

    _info(
        "Architecture",
        information["architecture"]
    )

    _info(
        "Implementation",
        information["python_implementation"]
    )

    # --------------------------------------------------------
    # Python root
    # --------------------------------------------------------

    _info(
        "Python root",
        sys.prefix
    )

    # --------------------------------------------------------
    # Pip detection
    #
    # Burada pip kurulumu yapılmaz.
    # Sadece mevcut pip kontrol edilir.
    # --------------------------------------------------------

    pip_path = shutil.which(
        "pip"
    )

    pip3_path = shutil.which(
        "pip3"
    )

    if pip3_path:

        _info(
            "Pip",
            pip3_path
        )

    elif pip_path:

        _info(
            "Pip",
            pip_path
        )

    else:

        _warning(
            "Pip executable not detected"
        )

    print(
        f"{Colors.BOLD}{Colors.CYAN}"
        "╰───────────────────────────────────╯"
        f"{Colors.RESET}"
    )

    return {
        "available": True,
        "executable": python_path,
        "version": version,
        "platform": information,
        "pip": pip3_path or pip_path,
    }


# ============================================================
# Python kontrolü
# ============================================================

def doctor():
    """
    Python çalışma ortamının temel sağlık kontrolünü yapar.
    """

    print()

    print(
        f"{Colors.BOLD}{Colors.CYAN}"
        "╭────── AstraSage Python Doctor ──────╮"
        f"{Colors.RESET}"
    )

    python_path = find_python()

    if python_path is None:

        _error(
            "Python interpreter not found."
        )

        print(
            f"{Colors.BOLD}{Colors.CYAN}"
            "╰─────────────────────────────────────╯"
            f"{Colors.RESET}"
        )

        return False

    _ok(
        f"Python found: {python_path}"
    )

    version = get_python_version(
        python_path
    )

    if version:

        _ok(
            f"Python version: {version}"
        )

    else:

        _warning(
            "Could not determine Python version."
        )

    # --------------------------------------------------------
    # Basit Python test
    # --------------------------------------------------------

    try:

        result = subprocess.run(
            [
                python_path,
                "-c",
                "print('AstraSage Python OK')"
            ],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:

            _ok(
                "Python execution test passed."
            )

        else:

            _error(
                "Python execution test failed."
            )

            return False

    except Exception as exc:

        _error(
            f"Python test failed: {exc}"
        )

        return False

    print(
        f"{Colors.BOLD}{Colors.CYAN}"
        "╰─────────────────────────────────────╯"
        f"{Colors.RESET}"
    )

    return True


# ============================================================
# Python komut yöneticisi
# ============================================================

def run_python_command(
    subcommand=None,
    args=None
):
    """
    AstraSage'in ana Python komut yöneticisi.

    Desteklenen temel komutlar:

        as python
        as python info
        as python --version
        as python version
        as python doctor
        as python shell
        as python run <file>
        as python exec <code>
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

        return python_info()

    # ========================================================
    # version
    # ========================================================

    if subcommand in (
        "version",
        "--version",
        "-v"
    ):

        version = get_python_version()

        if version:

            print(
                f"Python {version}"
            )

            return version

        _error(
            "Python interpreter not found."
        )

        return None

    # ========================================================
    # doctor
    # ========================================================

    if subcommand == "doctor":

        return doctor()

    # ========================================================
    # shell
    # ========================================================

    if subcommand in (
        "shell",
        "interactive"
    ):

        return start_python_shell()

    # ========================================================
    # run
    # ========================================================

    if subcommand == "run":

        if not args:

            _error(
                "Usage: as python run <file.py>"
            )

            return None

        file_path = args[0]

        file_args = args[1:]

        return run_file(
            file_path,
            args=file_args
        )

    # ========================================================
    # exec
    # ========================================================

    if subcommand in (
        "exec",
        "-c"
    ):

        if not args:

            _error(
                "Usage: as python exec "
                "\"<python code>\""
            )

            return None

        code = " ".join(
            str(item)
            for item in args
        )

        return execute_code(
            code
        )

    # ========================================================
    # module
    # ========================================================

    if subcommand == "module":

        if not args:

            _error(
                "Usage: as python module <name>"
            )

            return None

        module_name = args[0]

        exists = module_exists(
            module_name
        )

        if exists:

            _ok(
                f"Python module found: "
                f"{module_name}"
            )

        else:

            _warning(
                f"Python module not found: "
                f"{module_name}"
            )

        return exists

    # ========================================================
    # Unknown
    # ========================================================

    _error(
        f"Unknown Python command: "
        f"{subcommand}"
    )

    print()

    print(
        "Available commands:"
    )

    print(
        "  as python info"
    )

    print(
        "  as python --version"
    )

    print(
        "  as python doctor"
    )

    print(
        "  as python shell"
    )

    print(
        "  as python run <file.py>"
    )

    print(
        "  as python exec <code>"
    )

    print(
        "  as python module <name>"
    )

    return None


# ============================================================
# Test
# ============================================================

if __name__ == "__main__":

    import sys as _sys

    arguments = _sys.argv[1:]

    if not arguments:

        run_python_command(
            "info"
        )

    else:

        run_python_command(
            arguments[0],
            arguments[1:]
        )