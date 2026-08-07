# AstraSage Repair
# utils/repair.py
#
# AstraSage sistem, klasör ve dosya onarım sistemi.
#
# Repair hiçbir dosyayı değiştirmeden önce yedek oluşturur.
#
# Kullanım:
#   repair_target(path)
#   repair_file(path)
#   repair_folder(path)
#
# NOT:
# Repair yalnızca güvenli şekilde doğrulanabilen onarımları yapar.
# Bilinmeyen Python kodlarını rastgele değiştirmez.


import os
import ast
import json
import shutil
import tempfile
from datetime import datetime


# ============================================================
# Doctor import
# ============================================================

try:
    from . import doctor
except ImportError:
    import doctor


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
    MAGENTA = "\033[95m"
    BOLD = "\033[1m"


# ============================================================
# Yazdırma yardımcıları
# ============================================================

def _ok(message):
    print(f"{Colors.GREEN}[✓]{Colors.RESET} {message}")


def _warning(message):
    print(f"{Colors.YELLOW}[!]{Colors.RESET} {message}")


def _error(message):
    print(f"{Colors.RED}[✗]{Colors.RESET} {message}")


def _checking(message):
    print(f"{Colors.CYAN}[*]{Colors.RESET} Checking {message}")


def _repairing(message):
    print(f"{Colors.MAGENTA}[+]{Colors.RESET} Repairing {message}")


def _info(label, value):
    print(f"    {label:<12}: {value}")


# ============================================================
# Repair ayarları
# ============================================================

BACKUP_FOLDER_NAME = ".repair_backup"


# ============================================================
# Backup sistemi
# ============================================================

def get_backup_root(target):
    """
    Hedefin bulunduğu AstraSage kökünde backup klasörü oluşturur.

    Eğer hedef bir dosyaysa dosyanın bulunduğu klasör kullanılır.
    """

    if os.path.isdir(target):
        root = target
    else:
        root = os.path.dirname(os.path.abspath(target))

    backup_root = os.path.join(
        root,
        BACKUP_FOLDER_NAME
    )

    os.makedirs(
        backup_root,
        exist_ok=True
    )

    return backup_root


def create_backup(path):
    """
    Dosyanın onarım öncesi yedeğini oluşturur.

    Yedek yolu döndürür.
    """

    path = os.path.abspath(path)

    if not os.path.isfile(path):
        return None

    backup_root = get_backup_root(path)

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S_%f"
    )

    filename = os.path.basename(path)

    backup_name = (
        f"{timestamp}_{filename}.bak"
    )

    backup_path = os.path.join(
        backup_root,
        backup_name
    )

    try:

        shutil.copy2(
            path,
            backup_path
        )

        print(
            f"{Colors.BLUE}[backup]{Colors.RESET} "
            f"{filename} -> {backup_path}"
        )

        return backup_path

    except OSError as exc:

        _error(
            f"Could not create backup for "
            f"{filename}: {exc}"
        )

        return None


# ============================================================
# Güvenli dosya yazma
# ============================================================

def safe_write_file(path, content):
    """
    Dosyayı doğrudan ezmek yerine geçici dosyaya yazar,
    sonra atomik şekilde hedefe taşımaya çalışır.

    Böylece yazma sırasında hata oluşursa orijinal dosyanın
    bozulma ihtimali azaltılır.
    """

    path = os.path.abspath(path)

    directory = os.path.dirname(path)

    try:

        os.makedirs(
            directory,
            exist_ok=True
        )

        fd, temp_path = tempfile.mkstemp(
            prefix=".as_repair_",
            dir=directory,
            text=True
        )

        try:

            with os.fdopen(
                fd,
                "w",
                encoding="utf-8"
            ) as temp_file:

                temp_file.write(content)

            os.replace(
                temp_path,
                path
            )

            return True

        except Exception:

            try:
                os.remove(temp_path)
            except OSError:
                pass

            raise

    except Exception as exc:

        _error(
            f"Could not write {path}: {exc}"
        )

        return False


# ============================================================
# Python syntax kontrolü
# ============================================================

def get_python_error(path):
    """
    Python syntax hatasını döndürür.
    """

    try:

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            source = file.read()

        ast.parse(
            source,
            filename=path
        )

        return None

    except SyntaxError as exc:

        return {
            "type": "SyntaxError",
            "message": str(exc),
            "line": exc.lineno,
            "column": exc.offset,
        }

    except Exception as exc:

        return {
            "type": type(exc).__name__,
            "message": str(exc),
            "line": None,
            "column": None,
        }


# ============================================================
# JSON kontrolü
# ============================================================

def get_json_error(path):
    """
    JSON hatasını döndürür.
    """

    try:

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            json.load(file)

        return None

    except json.JSONDecodeError as exc:

        return {
            "type": "JSONDecodeError",
            "message": str(exc),
            "line": exc.lineno,
            "column": exc.colno,
        }

    except Exception as exc:

        return {
            "type": type(exc).__name__,
            "message": str(exc),
            "line": None,
            "column": None,
        }


# ============================================================
# Python dosyası onarımı
# ============================================================

def repair_python_file(path):
    """
    Python dosyasını kontrol eder.

    ÖNEMLİ:
    Python kodunun nasıl düzeltilmesi gerektiği bilinmiyorsa
    otomatik olarak kod silmez veya değiştirmez.

    Bu fonksiyon güvenli onarım sistemi için temel oluşturur.
    """

    path = os.path.abspath(path)

    filename = os.path.basename(path)

    _repairing(filename)

    error = get_python_error(path)

    if error is None:

        _ok(
            f"{filename} does not need Python repair"
        )

        return {
            "success": True,
            "changed": False,
            "reason": "No syntax problem.",
        }

    _warning(
        f"Python problem detected in {filename}"
    )

    _info(
        "Error",
        error["message"]
    )

    if error["line"] is not None:

        _info(
            "Line",
            error["line"]
        )

    if error["column"] is not None:

        _info(
            "Column",
            error["column"]
        )

    print()

    _warning(
        "Automatic Python source repair was not "
        "performed because the correct source cannot "
        "be determined safely."
    )

    _info(
        "File",
        path
    )

    return {
        "success": False,
        "changed": False,
        "reason": "Manual source repair required.",
        "error": error,
    }


# ============================================================
# JSON dosyası onarımı
# ============================================================

def repair_json_file(path):
    """
    JSON dosyasını güvenli şekilde kontrol eder.

    JSON zaten doğruysa hiçbir değişiklik yapmaz.

    Geçerli JSON'u yeniden formatlamak gerekirse
    backup oluşturulduktan sonra düzenleyebilir.
    """

    path = os.path.abspath(path)

    filename = os.path.basename(path)

    _repairing(filename)

    try:

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            content = file.read()

    except Exception as exc:

        _error(
            f"Could not read {filename}: {exc}"
        )

        return {
            "success": False,
            "changed": False,
            "error": str(exc),
        }

    try:

        data = json.loads(content)

    except json.JSONDecodeError as exc:

        _warning(
            f"Invalid JSON detected in {filename}"
        )

        _info(
            "Line",
            exc.lineno
        )

        _info(
            "Column",
            exc.colno
        )

        _info(
            "Error",
            exc.msg
        )

        print()

        _warning(
            "Automatic JSON reconstruction was not "
            "performed because the original intended "
            "data cannot be safely determined."
        )

        return {
            "success": False,
            "changed": False,
            "reason": "Manual JSON repair required.",
            "error": str(exc),
        }

    except Exception as exc:

        _error(
            f"JSON read error: {exc}"
        )

        return {
            "success": False,
            "changed": False,
            "error": str(exc),
        }

    # JSON geçerli.
    #
    # Burada yalnızca güvenli bir formatting işlemi
    # uygulanabilir.

    try:

        formatted = json.dumps(
            data,
            indent=4,
            ensure_ascii=False
        ) + "\n"

    except Exception as exc:

        _error(
            f"Could not format {filename}: {exc}"
        )

        return {
            "success": False,
            "changed": False,
            "error": str(exc),
        }

    if formatted == content:

        _ok(
            f"{filename} JSON is already valid"
        )

        return {
            "success": True,
            "changed": False,
            "reason": "JSON already formatted.",
        }

    backup = create_backup(path)

    if backup is None:

        _error(
            f"Repair cancelled for {filename} "
            "because backup could not be created."
        )

        return {
            "success": False,
            "changed": False,
            "reason": "Backup failed.",
        }

    _repairing(
        f"{filename} JSON formatting"
    )

    if safe_write_file(
        path,
        formatted
    ):

        _ok(
            f"File repaired: {filename}"
        )

        _info(
            "Backup",
            backup
        )

        return {
            "success": True,
            "changed": True,
            "backup": backup,
        }

    return {
        "success": False,
        "changed": False,
        "reason": "Write failed.",
        "backup": backup,
    }


# ============================================================
# Tek dosya repair
# ============================================================

def repair_file(path):
    """
    Tek dosyayı kontrol eder ve mümkünse onarır.
    """

    path = os.path.abspath(
        os.path.expanduser(path)
    )

    print()

    _checking(
        f"{os.path.basename(path)} file"
    )

    if not os.path.exists(path):

        _error(
            f"Missing file: {path}"
        )

        return {
            "success": False,
            "exists": False,
            "changed": False,
            "reason": "File does not exist.",
        }

    if not os.path.isfile(path):

        _error(
            f"Target is not a file: {path}"
        )

        return {
            "success": False,
            "exists": False,
            "changed": False,
            "reason": "Target is not a file.",
        }

    extension = os.path.splitext(
        path
    )[1].lower()

    # --------------------------------------------------------
    # Önce Doctor kontrolü
    # --------------------------------------------------------

    print()

    doctor_result = doctor.check_file(
        path,
        verbose=True
    )

    if doctor_result["valid"]:

        _ok(
            f"{os.path.basename(path)} "
            "does not need repair"
        )

        return {
            "success": True,
            "changed": False,
            "doctor": doctor_result,
        }

    # --------------------------------------------------------
    # Python
    # --------------------------------------------------------

    if extension == ".py":

        return repair_python_file(
            path
        )

    # --------------------------------------------------------
    # JSON
    # --------------------------------------------------------

    if extension == ".json":

        return repair_json_file(
            path
        )

    # --------------------------------------------------------
    # Diğer dosyalar
    # --------------------------------------------------------

    _warning(
        f"{os.path.basename(path)} has a problem, "
        "but no automatic repair method exists."
    )

    _info(
        "File",
        path
    )

    return {
        "success": False,
        "changed": False,
        "reason": "No safe repair method available.",
    }


# ============================================================
# Klasör repair
# ============================================================

def repair_folder(path):
    """
    Klasördeki dosyaları tek tek kontrol eder ve
    güvenli şekilde onarılabilecek olanları onarır.
    """

    path = os.path.abspath(
        os.path.expanduser(path)
    )

    print()

    print(
        f"{Colors.BOLD}{Colors.MAGENTA}"
        "╭──────── AstraSage System Repair ────────╮"
        f"{Colors.RESET}"
    )

    _info(
        "Target",
        os.path.basename(path)
    )

    _info(
        "Path",
        path
    )

    _info(
        "Type",
        "Folder"
    )

    print(
        f"{Colors.BOLD}{Colors.MAGENTA}"
        "╰─────────────────────────────────────────╯"
        f"{Colors.RESET}"
    )

    print()

    if not os.path.exists(path):

        _error(
            f"Missing folder: {path}"
        )

        return {
            "success": False,
            "changed": False,
            "files_checked": 0,
            "files_repaired": 0,
            "problems": [
                "Folder does not exist."
            ],
        }

    if not os.path.isdir(path):

        _error(
            f"Target is not a folder: {path}"
        )

        return {
            "success": False,
            "changed": False,
            "files_checked": 0,
            "files_repaired": 0,
            "problems": [
                "Target is not a folder."
            ],
        }

    files_checked = 0
    files_repaired = 0
    problems = []

    # --------------------------------------------------------
    # Klasör bilgisi
    # --------------------------------------------------------

    folder_info = doctor.get_folder_info(
        path
    )

    if folder_info:

        _info(
            "Files",
            folder_info["files"]
        )

        _info(
            "Folders",
            folder_info["folders"]
        )

        _info(
            "Python",
            folder_info["python"]
        )

        _info(
            "JSON",
            folder_info["json"]
        )

        _info(
            "Other",
            folder_info["other"]
        )

    print()

    # --------------------------------------------------------
    # Dosyaları tara
    # --------------------------------------------------------

    for root, dirs, files in os.walk(path):

        # Backup klasörünü tekrar tarama.
        dirs[:] = [
            directory
            for directory in dirs
            if directory != BACKUP_FOLDER_NAME
        ]

        for directory in dirs:

            folder_path = os.path.join(
                root,
                directory
            )

            relative_folder = os.path.relpath(
                folder_path,
                path
            )

            _checking(
                f"{relative_folder} folder"
            )

            _info(
                "Path",
                folder_path
            )

            # Klasör bilgisi
            child_info = doctor.get_folder_info(
                folder_path
            )

            if child_info:

                _info(
                    "Files",
                    child_info["files"]
                )

                _info(
                    "Folders",
                    child_info["folders"]
                )

            print()

        for filename in files:

            file_path = os.path.join(
                root,
                filename
            )

            relative_file = os.path.relpath(
                file_path,
                path
            )

            files_checked += 1

            print()

            _checking(
                f"{relative_file} file"
            )

            repair_result = repair_file(
                file_path
            )

            if repair_result.get(
                "changed",
                False
            ):

                files_repaired += 1

            if not repair_result.get(
                "success",
                False
            ):

                if repair_result.get(
                    "reason"
                ):

                    problems.append({
                        "file": file_path,
                        "reason": repair_result[
                            "reason"
                        ],
                    })

    # --------------------------------------------------------
    # Sonuç
    # --------------------------------------------------------

    print()

    print(
        f"{Colors.BOLD}{Colors.MAGENTA}"
        "──────── Repair Summary ────────"
        f"{Colors.RESET}"
    )

    _info(
        "Files checked",
        files_checked
    )

    _info(
        "Files repaired",
        files_repaired
    )

    _info(
        "Problems",
        len(problems)
    )

    print()

    if len(problems) == 0:

        _ok(
            "Repair completed successfully"
        )

        return {
            "success": True,
            "changed": files_repaired > 0,
            "files_checked": files_checked,
            "files_repaired": files_repaired,
            "problems": [],
        }

    _warning(
        "Repair completed with unresolved problems"
    )

    for problem in problems:

        _error(
            f"{problem['file']}: "
            f"{problem['reason']}"
        )

    return {
        "success": False,
        "changed": files_repaired > 0,
        "files_checked": files_checked,
        "files_repaired": files_repaired,
        "problems": problems,
    }


# ============================================================
# Genel Repair hedefi
# ============================================================

def repair_target(path):
    """
    Hedef dosya mı klasör mü belirler ve uygun
    repair fonksiyonunu çalıştırır.
    """

    path = os.path.abspath(
        os.path.expanduser(path)
    )

    if os.path.isdir(path):

        return repair_folder(
            path
        )

    if os.path.isfile(path):

        return repair_file(
            path
        )

    print()

    _error(
        f"Target does not exist: {path}"
    )

    return {
        "success": False,
        "changed": False,
        "exists": False,
        "problems": [
            "Target does not exist."
        ],
    }


# ============================================================
# AstraSage --system
# ============================================================

def repair_system(astrasage_root):
    """
    AstraSage'in tamamını kontrol eder ve
    güvenli şekilde onarılabilen dosyaları onarır.

    --system parametresi için kullanılabilir.
    """

    if not astrasage_root:

        _error(
            "AstraSage root directory is not defined."
        )

        return None

    astrasage_root = os.path.abspath(
        os.path.expanduser(
            astrasage_root
        )
    )

    print()

    print(
        f"{Colors.BOLD}{Colors.MAGENTA}"
        "╭──────── AstraSage Full Repair ─────────╮"
        f"{Colors.RESET}"
    )

    _info(
        "Target",
        "AstraSage System"
    )

    _info(
        "Path",
        astrasage_root
    )

    _info(
        "Mode",
        "Full System"
    )

    print(
        f"{Colors.BOLD}{Colors.MAGENTA}"
        "╰─────────────────────────────────────────╯"
        f"{Colors.RESET}"
    )

    return repair_folder(
        astrasage_root
    )


# ============================================================
# Backup geri yükleme
# ============================================================

def restore_backup(backup_path, target_path):
    """
    Bir backup dosyasını hedef dosyaya geri yükler.

    Geri yüklemeden önce mevcut hedefin de yedeğini alır.
    """

    backup_path = os.path.abspath(
        os.path.expanduser(
            backup_path
        )
    )

    target_path = os.path.abspath(
        os.path.expanduser(
            target_path
        )
    )

    if not os.path.isfile(backup_path):

        _error(
            f"Backup file does not exist: "
            f"{backup_path}"
        )

        return False

    if os.path.isfile(target_path):

        current_backup = create_backup(
            target_path
        )

        if current_backup:

            _info(
                "Current backup",
                current_backup
            )

    try:

        shutil.copy2(
            backup_path,
            target_path
        )

        _ok(
            f"Backup restored: "
            f"{os.path.basename(target_path)}"
        )

        return True

    except OSError as exc:

        _error(
            f"Could not restore backup: {exc}"
        )

        return False


# ============================================================
# Son Repair işlemini geri alma
# ============================================================

def list_backups(target):
    """
    Hedef için mevcut backup dosyalarını listeler.
    """

    backup_root = get_backup_root(
        os.path.abspath(target)
    )

    if not os.path.isdir(backup_root):

        return []

    backups = []

    try:

        for filename in os.listdir(
            backup_root
        ):

            path = os.path.join(
                backup_root,
                filename
            )

            if os.path.isfile(path):

                backups.append(path)

    except OSError:

        return []

    backups.sort(
        reverse=True
    )

    return backups


# ============================================================
# CLI test
# ============================================================

if __name__ == "__main__":

    import sys

    if len(sys.argv) < 2:

        print(
            "Usage:"
        )

        print(
            "  python repair.py <file_or_folder>"
        )

        sys.exit(1)

    target = sys.argv[1]

    repair_target(
        target
    )