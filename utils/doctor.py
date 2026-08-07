# AstraSage Doctor
# utils/doctor.py
#
# AstraSage sistem, klasör ve dosya sağlık kontrolü.
# Doctor hiçbir dosyayı değiştirmez veya silmez.
#
# Kullanım:
#   doctor_target(path)
#   check_file(path)
#   check_folder(path)

import os
import ast
import json


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
    WHITE = "\033[97m"
    BOLD = "\033[1m"


# ============================================================
# Yardımcı yazdırma fonksiyonları
# ============================================================

def _ok(message):
    print(f"{Colors.GREEN}[✓]{Colors.RESET} {message}")


def _warning(message):
    print(f"{Colors.YELLOW}[!]{Colors.RESET} {message}")


def _error(message):
    print(f"{Colors.RED}[✗]{Colors.RESET} {message}")


def _checking(message):
    print(f"{Colors.CYAN}[*]{Colors.RESET} Checking {message}")


def _info(label, value):
    print(f"    {label:<12}: {value}")


# ============================================================
# Dosya bilgileri
# ============================================================

def get_file_info(path):
    """
    Dosya hakkında temel bilgileri döndürür.
    """

    if not os.path.isfile(path):
        return None

    try:
        size = os.path.getsize(path)

        extension = os.path.splitext(path)[1]

        return {
            "name": os.path.basename(path),
            "path": os.path.abspath(path),
            "size": size,
            "extension": extension if extension else "none",
        }

    except OSError as exc:
        return {
            "name": os.path.basename(path),
            "path": os.path.abspath(path),
            "size": 0,
            "extension": "",
            "error": str(exc),
        }


def format_size(size):
    """
    Byte değerini okunabilir hale getirir.
    """

    if size < 1024:
        return f"{size} B"

    if size < 1024 * 1024:
        return f"{size / 1024:.2f} KB"

    if size < 1024 * 1024 * 1024:
        return f"{size / (1024 * 1024):.2f} MB"

    return f"{size / (1024 * 1024 * 1024):.2f} GB"


# ============================================================
# Klasör bilgileri
# ============================================================

def get_folder_info(path):
    """
    Klasördeki dosya ve klasör sayılarını hesaplar.
    """

    if not os.path.isdir(path):
        return None

    files = 0
    folders = 0
    python_files = 0
    json_files = 0
    other_files = 0

    try:
        for root, dirs, filenames in os.walk(path):

            folders += len(dirs)
            files += len(filenames)

            for filename in filenames:
                extension = os.path.splitext(filename)[1].lower()

                if extension == ".py":
                    python_files += 1

                elif extension == ".json":
                    json_files += 1

                else:
                    other_files += 1

        return {
            "name": os.path.basename(os.path.abspath(path)),
            "path": os.path.abspath(path),
            "files": files,
            "folders": folders,
            "python": python_files,
            "json": json_files,
            "other": other_files,
        }

    except OSError as exc:
        return {
            "name": os.path.basename(os.path.abspath(path)),
            "path": os.path.abspath(path),
            "files": files,
            "folders": folders,
            "python": python_files,
            "json": json_files,
            "other": other_files,
            "error": str(exc),
        }


# ============================================================
# Python kontrolü
# ============================================================

def check_python_file(path):
    """
    Python dosyasının syntax durumunu kontrol eder.

    Dosya değiştirilmez.
    """

    try:
        with open(path, "r", encoding="utf-8") as file:
            source = file.read()

        ast.parse(source, filename=path)

        return {
            "valid": True,
            "error": None,
            "line": None,
            "column": None,
        }

    except SyntaxError as exc:
        return {
            "valid": False,
            "error": str(exc),
            "line": exc.lineno,
            "column": exc.offset,
        }

    except UnicodeDecodeError as exc:
        return {
            "valid": False,
            "error": f"UTF-8 decode error: {exc}",
            "line": None,
            "column": None,
        }

    except OSError as exc:
        return {
            "valid": False,
            "error": str(exc),
            "line": None,
            "column": None,
        }


# ============================================================
# JSON kontrolü
# ============================================================

def check_json_file(path):
    """
    JSON dosyasının geçerli olup olmadığını kontrol eder.
    """

    try:
        with open(path, "r", encoding="utf-8") as file:
            json.load(file)

        return {
            "valid": True,
            "error": None,
        }

    except json.JSONDecodeError as exc:
        return {
            "valid": False,
            "error": str(exc),
            "line": exc.lineno,
            "column": exc.colno,
        }

    except (OSError, UnicodeDecodeError) as exc:
        return {
            "valid": False,
            "error": str(exc),
        }


# ============================================================
# Dosya kontrolü
# ============================================================

def check_file(path, verbose=True):
    """
    Tek bir dosyayı kontrol eder.

    Dönen değer:
        {
            "path": ...,
            "type": "file",
            "exists": True,
            "valid": True/False,
            "problems": [...]
        }
    """

    result = {
        "path": os.path.abspath(path),
        "type": "file",
        "exists": os.path.isfile(path),
        "valid": True,
        "problems": [],
    }

    if verbose:
        _checking(f"{os.path.basename(path)} file")

    if not os.path.exists(path):

        result["exists"] = False
        result["valid"] = False
        result["problems"].append("File does not exist.")

        _error(f"Missing file: {path}")

        return result

    if not os.path.isfile(path):

        result["valid"] = False
        result["problems"].append("Target is not a file.")

        _error(f"Target is not a file: {path}")

        return result

    info = get_file_info(path)

    if info:
        if verbose:
            _info("Path", info["path"])
            _info("Size", format_size(info["size"]))
            _info("Extension", info["extension"])

    extension = os.path.splitext(path)[1].lower()

    # --------------------------------------------------------
    # Python
    # --------------------------------------------------------

    if extension == ".py":

        python_result = check_python_file(path)

        if not python_result["valid"]:

            result["valid"] = False

            result["problems"].append({
                "type": "python_syntax",
                "error": python_result["error"],
                "line": python_result["line"],
                "column": python_result["column"],
            })

            _error("Python syntax problem detected.")

            if python_result["line"]:
                _info("Line", python_result["line"])

            if python_result["column"]:
                _info("Column", python_result["column"])

            _info("Error", python_result["error"])

        else:
            _ok(f"{os.path.basename(path)} syntax OK")

    # --------------------------------------------------------
    # JSON
    # --------------------------------------------------------

    elif extension == ".json":

        json_result = check_json_file(path)

        if not json_result["valid"]:

            result["valid"] = False

            result["problems"].append({
                "type": "json_error",
                "error": json_result["error"],
                "line": json_result.get("line"),
                "column": json_result.get("column"),
            })

            _error("JSON structure problem detected.")
            _info("Error", json_result["error"])

        else:
            _ok(f"{os.path.basename(path)} JSON OK")

    # --------------------------------------------------------
    # Diğer dosyalar
    # --------------------------------------------------------

    else:

        if verbose:
            _ok(f"{os.path.basename(path)} exists")

    return result


# ============================================================
# Klasör kontrolü
# ============================================================

def check_folder(path, recursive=True, verbose=True):
    """
    Klasörü kontrol eder.

    recursive=True ise alt klasörlerdeki bütün dosyaları
    kontrol eder.
    """

    result = {
        "path": os.path.abspath(path),
        "type": "folder",
        "exists": os.path.isdir(path),
        "valid": True,
        "files_checked": 0,
        "folders_checked": 0,
        "problems": [],
    }

    if verbose:
        _checking(f"{os.path.basename(os.path.abspath(path))} folder")

    if not os.path.exists(path):

        result["exists"] = False
        result["valid"] = False
        result["problems"].append("Folder does not exist.")

        _error(f"Missing folder: {path}")

        return result

    if not os.path.isdir(path):

        result["valid"] = False
        result["problems"].append("Target is not a folder.")

        _error(f"Target is not a folder: {path}")

        return result

    # --------------------------------------------------------
    # Klasör bilgileri
    # --------------------------------------------------------

    info = get_folder_info(path)

    if info:

        _info("Path", info["path"])
        _info("Files", info["files"])
        _info("Folders", info["folders"])
        _info("Python", info["python"])
        _info("JSON", info["json"])
        _info("Other", info["other"])

    print()

    # --------------------------------------------------------
    # Dosyaları tara
    # --------------------------------------------------------

    if recursive:

        for root, dirs, files in os.walk(path):

            for directory in dirs:

                folder_path = os.path.join(root, directory)

                result["folders_checked"] += 1

                if verbose:
                    _checking(
                        f"{os.path.relpath(folder_path, path)} folder"
                    )

                _ok(
                    f"{os.path.relpath(folder_path, path)} folder exists"
                )

            for filename in files:

                file_path = os.path.join(root, filename)

                result["files_checked"] += 1

                file_result = check_file(
                    file_path,
                    verbose=verbose
                )

                if not file_result["valid"]:

                    result["valid"] = False

                    result["problems"].extend(
                        file_result["problems"]
                    )

    else:

        try:

            entries = os.listdir(path)

            for entry in entries:

                full_path = os.path.join(path, entry)

                if os.path.isfile(full_path):

                    result["files_checked"] += 1

                    file_result = check_file(
                        full_path,
                        verbose=verbose
                    )

                    if not file_result["valid"]:

                        result["valid"] = False

                        result["problems"].extend(
                            file_result["problems"]
                        )

                elif os.path.isdir(full_path):

                    result["folders_checked"] += 1

        except OSError as exc:

            result["valid"] = False

            result["problems"].append(str(exc))

            _error(str(exc))

    return result


# ============================================================
# Genel hedef kontrolü
# ============================================================

def doctor_target(path, recursive=True):
    """
    Verilen hedefin dosya mı klasör mü olduğunu belirler
    ve uygun Doctor kontrolünü çalıştırır.
    """

    path = os.path.abspath(os.path.expanduser(path))

    print()

    print(
        f"{Colors.BOLD}{Colors.CYAN}"
        "╭──────── AstraSage System Doctor ────────╮"
        f"{Colors.RESET}"
    )

    _info("Target", os.path.basename(path))
    _info("Path", path)

    if os.path.isdir(path):

        _info("Type", "Folder")

        print(
            f"{Colors.BOLD}{Colors.CYAN}"
            "╰─────────────────────────────────────────╯"
            f"{Colors.RESET}"
        )

        print()

        result = check_folder(
            path,
            recursive=recursive,
            verbose=True
        )

    elif os.path.isfile(path):

        _info("Type", "File")

        print(
            f"{Colors.BOLD}{Colors.CYAN}"
            "╰─────────────────────────────────────────╯"
            f"{Colors.RESET}"
        )

        print()

        result = check_file(
            path,
            verbose=True
        )

    else:

        _info("Type", "Unknown")

        print(
            f"{Colors.BOLD}{Colors.CYAN}"
            "╰─────────────────────────────────────────╯"
            f"{Colors.RESET}"
        )

        print()

        _error(f"Target does not exist: {path}")

        return {
            "path": path,
            "type": "unknown",
            "exists": False,
            "valid": False,
            "problems": [
                "Target does not exist."
            ],
        }

    # ========================================================
    # Sonuç
    # ========================================================

    print()

    if result["valid"]:

        _ok("Doctor completed")

        if result["type"] == "folder":

            _info(
                "Files checked",
                result["files_checked"]
            )

            _info(
                "Folders checked",
                result["folders_checked"]
            )

        _ok("0 problems found")

    else:

        _warning("Doctor completed with problems")

        if result["type"] == "folder":

            _info(
                "Files checked",
                result["files_checked"]
            )

            _info(
                "Folders checked",
                result["folders_checked"]
            )

        _error(
            f"{len(result['problems'])} problem(s) found"
        )

    print()

    return result


# ============================================================
# Sistem kontrolü için yardımcı fonksiyon
# ============================================================

def doctor_system(astrasage_root):
    """
    AstraSage'in tamamını kontrol eder.

    --system parametresi için kullanılabilir.
    """

    if not astrasage_root:
        _error("AstraSage root directory is not defined.")
        return None

    astrasage_root = os.path.abspath(
        os.path.expanduser(astrasage_root)
    )

    return doctor_target(
        astrasage_root,
        recursive=True
    )


# ============================================================
# Test
# ============================================================

if __name__ == "__main__":

    import sys

    if len(sys.argv) < 2:

        print(
            "Usage: python doctor.py <file_or_folder>"
        )

        sys.exit(1)

    target = sys.argv[1]

    doctor_target(target)