# ============================================================
# AstraSage • as_tree
# AstraSage dosya sistemi ve komut ağacı görüntüleyicisi
# By: EnderAstra
# ============================================================

import os


# ============================================================
# RENKLER
# ============================================================

try:
    from utils.renk import Renk
except ImportError:
    class Renk:
        YESIL = "\033[92m"
        KOYU_YESIL = "\033[32m"
        SARI = "\033[93m"
        KIRMIZI = "\033[91m"
        RESET = "\033[0m"
        KALIN = "\033[1m"
        MAVI = "\033[34m"


# ============================================================
# DOSYA SİSTEMİ AĞACI
# ============================================================

def _print_file_system(path=None, prefix=""):
    """
    AstraSage'in bulunduğu klasörün dosya sistemini
    ağaç şeklinde gösterir.
    """

    if path is None:
        path = os.getcwd()

    path = os.path.abspath(path)

    if not os.path.exists(path):
        print(
            f"{Renk.KIRMIZI}"
            f"[!] Klasör bulunamadı: {path}"
            f"{Renk.RESET}"
        )
        return

    try:
        entries = sorted(
            os.listdir(path),
            key=lambda x: (
                not os.path.isdir(os.path.join(path, x)),
                x.lower()
            )
        )
    except PermissionError:
        print(
            f"{Renk.KIRMIZI}"
            f"[!] Bu klasöre erişim izni yok: {path}"
            f"{Renk.RESET}"
        )
        return

    for index, entry in enumerate(entries):

        full_path = os.path.join(path, entry)

        is_last = index == len(entries) - 1

        if is_last:
            branch = "└── "
            next_prefix = prefix + "    "
        else:
            branch = "├── "
            next_prefix = prefix + "│   "

        if os.path.isdir(full_path):

            print(
                f"{prefix}"
                f"{branch}"
                f"{Renk.MAVI}"
                f"{entry}/"
                f"{Renk.RESET}"
            )

            _print_file_system(
                full_path,
                next_prefix
            )

        else:

            print(
                f"{prefix}"
                f"{branch}"
                f"{Renk.RESET}"
                f"{entry}"
            )


def file_system_tree():
    """
    AstraSage'in mevcut çalışma dizinini ağaç olarak gösterir.
    """

    root = os.getcwd()

    print()
    print(
        f"{Renk.KALIN}"
        f"{Renk.YESIL}"
        f"AstraSage File System"
        f"{Renk.RESET}"
    )

    print(
        f"{Renk.KOYU_YESIL}"
        f"{os.path.basename(root) or root}/"
        f"{Renk.RESET}"
    )

    _print_file_system(root)

    print()


# ============================================================
# KOMUT AĞACI
# ============================================================

def _print_command_node(node, prefix="", is_last=True):
    """
    COMMAND_TREE içerisindeki bir düğümü recursive olarak
    terminal ağacına dönüştürür.
    """

    if not isinstance(node, dict):
        return

    items = list(node.items())

    for index, (name, value) in enumerate(items):

        last = index == len(items) - 1

        if last:
            branch = "└── "
            next_prefix = prefix + "    "
        else:
            branch = "├── "
            next_prefix = prefix + "│   "

        print(
            f"{prefix}"
            f"{branch}"
            f"{Renk.YESIL}"
            f"{name}"
            f"{Renk.RESET}"
        )

        if isinstance(value, dict):
            _print_command_node(
                value,
                next_prefix,
                last
            )


def command_tree():
    """
    AstraSage COMMAND_TREE yapısını ağaç halinde gösterir.
    """

    try:
        # main.py içerisindeki COMMAND_TREE
        from main import COMMAND_TREE

    except ImportError:
        print(
            f"{Renk.KIRMIZI}"
            "[!] COMMAND_TREE bulunamadı."
            f"{Renk.RESET}"
        )
        return

    print()

    print(
        f"{Renk.KALIN}"
        f"{Renk.YESIL}"
        "AstraSage Commands"
        f"{Renk.RESET}"
    )

    _print_command_node(COMMAND_TREE)

    print()


# ============================================================
# YARDIM
# ============================================================

def tree_help():
    print()

    print(
        f"{Renk.KALIN}"
        f"{Renk.YESIL}"
        "as tree"
        f"{Renk.RESET}"
    )

    print()

    print(
        f"{Renk.SARI}"
        "Kullanım:"
        f"{Renk.RESET}"
    )

    print("  as tree --file-system")
    print("      AstraSage dosya sistemini ağaç halinde gösterir.")

    print()

    print("  as tree --as-commands")
    print("      AstraSage komutlarını ağaç halinde gösterir.")

    print()

    print("  as tree --help")
    print("      as tree yardım menüsünü gösterir.")

    print()


# ============================================================
# ANA KOMUT
# ============================================================

def run_tree(args):
    """
    as tree komutunun ana çalıştırıcısı.

    Örnek:
        run_tree(["--file-system"])
        run_tree(["--as-commands"])
    """

    if not args:
        tree_help()
        return

    option = args[0].lower()

    if option == "--file-system":
        file_system_tree()

    elif option == "--as-commands":
        command_tree()

    elif option in ("--help", "-h", "help"):
        tree_help()

    else:
        print(
            f"{Renk.KIRMIZI}"
            f"[!] Geçersiz as tree seçeneği: {option}"
            f"{Renk.RESET}"
        )

        print(
            f"Kullanım için: "
            f"{Renk.SARI}"
            f"as tree --help"
            f"{Renk.RESET}"
        )