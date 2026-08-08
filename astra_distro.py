# Astra-Distro
# AstraSage Project
#
# Özgün Linux userspace / RootFS yöneticisi
#
# Komutlar:
#
#   astra-distro list
#   astra-distro search <distro>
#   astra-distro install <distro>
#   astra-distro join <distro>
#   astra-distro remove <distro>
#   astra-distro info <distro>
#   astra-distro default <distro>
#   astra-distro doctor
#   astra-distro version
#
# Astra-Distro:
#
#   - proot-distro kullanmaz
#   - Termux proot kullanmaz
#   - kendi metadata sistemini kullanır
#   - kendi RootFS dizinlerini yönetir
#   - Astra-Proot executable'ını kullanır
#
# NOT:
# Repository adresi Astra-Distro'nun kendi repository'si olacak şekilde
# tasarlanmıştır. Henüz yayınlanmamış bir sunucu adresi uydurulmamıştır.


import os
import sys
import json
import shutil
import platform
import subprocess
import hashlib
import tarfile
import urllib.request
import urllib.error
import tempfile
import time
from datetime import datetime


# ============================================================
# ASTRA-DISTRO KÖKÜ
# ============================================================

ASTRA_DISTRO_FILE = os.path.abspath(__file__)

ASTRASAGE_ROOT = os.path.dirname(
    ASTRA_DISTRO_FILE
)

ASTRA_DISTRO_ROOT = os.path.join(
    ASTRASAGE_ROOT,
    "astra-distro"
)

ROOTFS_DIR = os.path.join(
    ASTRA_DISTRO_ROOT,
    "rootfs"
)

DOWNLOAD_DIR = os.path.join(
    ASTRA_DISTRO_ROOT,
    "downloads"
)

LOG_DIR = os.path.join(
    ASTRA_DISTRO_ROOT,
    "logs"
)

CACHE_DIR = os.path.join(
    ASTRA_DISTRO_ROOT,
    "cache"
)

CONFIG_FILE = os.path.join(
    ASTRA_DISTRO_ROOT,
    "config.json"
)

ASTRA_PROOT = os.path.join(
    ASTRA_DISTRO_ROOT,
    "astra-proot"
)


# ============================================================
# ASTRA REPOSITORY
# ============================================================

# Bu adresi kendi Astra-Distro repository'n yayınlandığında
# gerçek repository adresinle değiştir.
#
# Örnek yapı:
#
# repository/
# ├── index.json
# └── rootfs/
#     ├── debian/
#     │   └── aarch64/
#     │       ├── manifest.json
#     │       └── debian-aarch64.tar.xz
#     ├── ubuntu/
#     └── alpine/
#
# Burada Termux/proot-distro repository'si kullanılmaz.

ASTRA_REPOSITORY = (
    "https://raw.githubusercontent.com/"
    "EnderAstra7744/Astra-Distro/main/"
)


# ============================================================
# SÜRÜM
# ============================================================

ASTRA_DISTRO_VERSION = "0.1.0"


# ============================================================
# RENKLER
# ============================================================

class Renk:

    YESIL = "\033[92m"
    KOYU_YESIL = "\033[32m"
    KIRMIZI = "\033[91m"
    SARI = "\033[93m"
    MAVI = "\033[94m"
    MOR = "\033[95m"
    TURKUAZ = "\033[96m"
    BEYAZ = "\033[97m"

    RESET = "\033[0m"
    BOLD = "\033[1m"


# ============================================================
# KLASÖRLER
# ============================================================

def setup_directories():

    os.makedirs(
        ASTRA_DISTRO_ROOT,
        exist_ok=True
    )

    os.makedirs(
        ROOTFS_DIR,
        exist_ok=True
    )

    os.makedirs(
        DOWNLOAD_DIR,
        exist_ok=True
    )

    os.makedirs(
        LOG_DIR,
        exist_ok=True
    )

    os.makedirs(
        CACHE_DIR,
        exist_ok=True
    )


# ============================================================
# CONFIG
# ============================================================

def default_config():

    return {

        "astra_distro_version":
            ASTRA_DISTRO_VERSION,

        "repository":
            ASTRA_REPOSITORY,

        "installed": [],

        "default_distro":
            None,

        "architecture":
            get_architecture()
    }


def load_config():

    setup_directories()

    if not os.path.exists(
        CONFIG_FILE
    ):

        config = default_config()

        save_config(
            config
        )

        return config

    try:

        with open(
            CONFIG_FILE,
            "r",
            encoding="utf-8"
        ) as dosya:

            config = json.load(
                dosya
            )

        return config

    except Exception:

        return default_config()


def save_config(config):

    setup_directories()

    with open(
        CONFIG_FILE,
        "w",
        encoding="utf-8"
    ) as dosya:

        json.dump(
            config,
            dosya,
            indent=4,
            ensure_ascii=False
        )


# ============================================================
# LOG
# ============================================================

def log_yaz(mesaj):

    setup_directories()

    tarih = datetime.now().strftime(
        "%Y-%m-%d"
    )

    saat = datetime.now().strftime(
        "%H:%M:%S"
    )

    log_file = os.path.join(
        LOG_DIR,
        f"astra-distro-{tarih}.log"
    )

    with open(
        log_file,
        "a",
        encoding="utf-8"
    ) as dosya:

        dosya.write(
            f"[{saat}] {mesaj}\n"
        )


# ============================================================
# MİMARİ
# ============================================================

def get_architecture():

    machine = (
        platform.machine()
        .lower()
    )

    if machine in (
        "aarch64",
        "arm64"
    ):

        return "aarch64"

    if machine in (
        "arm",
        "armv7",
        "armv7l"
    ):

        return "arm"

    if machine in (
        "x86_64",
        "amd64"
    ):

        return "x86_64"

    if machine in (
        "x86",
        "i386",
        "i686"
    ):

        return "x86"

    return machine


# ============================================================
# ASTRA-PROOT
# ============================================================

def check_astra_proot():

    if not os.path.exists(
        ASTRA_PROOT
    ):

        print(
            f"{Renk.KIRMIZI}"
            "[!] Astra-Proot bulunamadı."
            f"{Renk.RESET}"
        )

        print(
            f"[*] Aranan:"
        )

        print(
            f"    {ASTRA_PROOT}"
        )

        return False

    if not os.path.isfile(
        ASTRA_PROOT
    ):

        print(
            f"{Renk.KIRMIZI}"
            "[!] Astra-Proot geçerli bir dosya değil."
            f"{Renk.RESET}"
        )

        return False

    if not os.access(
        ASTRA_PROOT,
        os.X_OK
    ):

        try:

            mode = os.stat(
                ASTRA_PROOT
            ).st_mode

            os.chmod(
                ASTRA_PROOT,
                mode | 0o111
            )

        except Exception as hata:

            print(
                f"{Renk.KIRMIZI}"
                f"[!] Astra-Proot çalıştırılamıyor: "
                f"{hata}"
                f"{Renk.RESET}"
            )

            return False

    return True


# ============================================================
# DISTRO YOLLARI
# ============================================================

def distro_yolu(distro):

    return os.path.join(
        ROOTFS_DIR,
        distro
    )


def metadata_yolu(distro):

    return os.path.join(
        distro_yolu(distro),
        ".astra-distro.json"
    )


# ============================================================
# REPOSITORY URL
# ============================================================

def repository_url(path):

    base = ASTRA_REPOSITORY.rstrip(
        "/"
    )

    path = path.lstrip(
        "/"
    )

    return (
        f"{base}/{path}"
    )


# ============================================================
# REPOSITORY'DEN DOSYA İNDİR
# ============================================================

def download_file(
    url,
    hedef
):

    print()

    print(
        f"{Renk.TURKUAZ}"
        "[*] İndiriliyor..."
        f"{Renk.RESET}"
    )

    print(
        f"    {url}"
    )

    try:

        request = urllib.request.Request(
            url,
            headers={
                "User-Agent":
                    "Astra-Distro/"
                    + ASTRA_DISTRO_VERSION
            }
        )

        with urllib.request.urlopen(
            request,
            timeout=30
        ) as response:

            total = response.headers.get(
                "Content-Length"
            )

            if total:

                total = int(
                    total
                )

            else:

                total = 0

            downloaded = 0

            with open(
                hedef,
                "wb"
            ) as dosya:

                while True:

                    data = response.read(
                        1024 * 128
                    )

                    if not data:
                        break

                    dosya.write(
                        data
                    )

                    downloaded += len(
                        data
                    )

                    if total:

                        percent = (
                            downloaded
                            * 100
                            / total
                        )

                        print(
                            f"\r[*] "
                            f"%{percent:.1f}",
                            end="",
                            flush=True
                        )

        print()

        print(
            f"{Renk.YESIL}"
            "[✓] İndirme tamamlandı."
            f"{Renk.RESET}"
        )

        return True

    except Exception as hata:

        print()

        print(
            f"{Renk.KIRMIZI}"
            f"[!] İndirme hatası: {hata}"
            f"{Renk.RESET}"
        )

        log_yaz(
            f"Download error: {url} | {hata}"
        )

        return False


# ============================================================
# SHA256
# ============================================================

def sha256_file(
    dosya
):

    sha256 = hashlib.sha256()

    with open(
        dosya,
        "rb"
    ) as f:

        while True:

            data = f.read(
                1024 * 1024
            )

            if not data:
                break

            sha256.update(
                data
            )

    return sha256.hexdigest()


def verify_sha256(
    dosya,
    expected
):

    if not expected:

        print(
            f"{Renk.SARI}"
            "[!] SHA256 manifestte belirtilmemiş."
            f"{Renk.RESET}"
        )

        return False

    print(
        "[*] SHA256 doğrulanıyor..."
    )

    actual = sha256_file(
        dosya
    )

    print(
        f"    Beklenen: {expected}"
    )

    print(
        f"    Gerçek   : {actual}"
    )

    if actual.lower() != expected.lower():

        print(
            f"{Renk.KIRMIZI}"
            "[X] SHA256 doğrulaması başarısız."
            f"{Renk.RESET}"
        )

        return False

    print(
        f"{Renk.YESIL}"
        "[✓] SHA256 doğrulandı."
        f"{Renk.RESET}"
    )

    return True


# ============================================================
# JSON DOWNLOAD
# ============================================================

def download_json(
    url
):

    try:

        request = urllib.request.Request(
            url,
            headers={
                "User-Agent":
                    "Astra-Distro/"
                    + ASTRA_DISTRO_VERSION
            }
        )

        with urllib.request.urlopen(
            request,
            timeout=30
        ) as response:

            raw = response.read()

        return json.loads(
            raw.decode(
                "utf-8"
            )
        )

    except Exception as hata:

        print(
            f"{Renk.KIRMIZI}"
            f"[!] Repository metadata alınamadı: "
            f"{hata}"
            f"{Renk.RESET}"
        )

        log_yaz(
            f"Repository error: {url} | {hata}"
        )

        return None


# ============================================================
# REPOSITORY INDEX
# ============================================================

def repository_index():

    url = repository_url(
        "index.json"
    )

    print(
        f"[*] Astra Repository:"
    )

    print(
        f"    {url}"
    )

    return download_json(
        url
    )


# ============================================================
# DISTRO BİLGİSİ
# ============================================================

def get_distro_info(
    distro
):

    index = repository_index()

    if not index:

        return None

    distros = index.get(
        "distros",
        {}
    )

    return distros.get(
        distro
    )


# ============================================================
# KURULU MU?
# ============================================================

def distro_kurulu_mu(
    distro
):

    config = load_config()

    if distro in config.get(
        "installed",
        []
    ):

        return True

    return os.path.isdir(
        distro_yolu(
            distro
        )
    )


# ============================================================
# METADATA
# ============================================================

def create_metadata(
    distro,
    repository_info
):

    metadata = {

        "id":
            distro,

        "name":
            repository_info.get(
                "name",
                distro
            ),

        "description":
            repository_info.get(
                "description",
                ""
            ),

        "architecture":
            get_architecture(),

        "version":
            repository_info.get(
                "version",
                "unknown"
            ),

        "repository":
            ASTRA_REPOSITORY,

        "installed_at":
            datetime.now().isoformat(),

        "manager":
            "Astra-Distro",

        "manager_version":
            ASTRA_DISTRO_VERSION
    }

    with open(
        metadata_yolu(
            distro
        ),
        "w",
        encoding="utf-8"
    ) as dosya:

        json.dump(
            metadata,
            dosya,
            indent=4,
            ensure_ascii=False
        )


# ============================================================
# SAFE TAR EXTRACTION
# ============================================================

def safe_extract(
    archive,
    hedef
):

    hedef_real = os.path.realpath(
        hedef
    )

    with tarfile.open(
        archive,
        "r:*"
    ) as tar:

        members = tar.getmembers()

        total = len(
            members
        )

        for index, member in enumerate(
            members,
            1
        ):

            member_path = os.path.realpath(
                os.path.join(
                    hedef,
                    member.name
                )
            )

            if not (
                member_path == hedef_real
                or member_path.startswith(
                    hedef_real + os.sep
                )
            ):

                raise RuntimeError(
                    "Güvensiz RootFS arşiv yolu: "
                    + member.name
                )

            tar.extract(
                member,
                hedef
            )

            if total:

                percent = (
                    index
                    * 100
                    / total
                )

                print(
                    f"\r[*] RootFS çıkarılıyor: "
                    f"%{percent:.1f}",
                    end="",
                    flush=True
                )

    print()


# ============================================================
# ROOTFS KUR
# ============================================================

def install_distro(
    distro
):

    distro = distro.lower()

    print()

    print(
        f"{Renk.YESIL}"
        "[ ASTRA-DISTRO INSTALL ]"
        f"{Renk.RESET}"
    )

    print()

    info = get_distro_info(
        distro
    )

    if info is None:

        print(
            f"{Renk.KIRMIZI}"
            f"[!] '{distro}' Astra Repository'de "
            "bulunamadı."
            f"{Renk.RESET}"
        )

        return

    architecture = get_architecture()

    architectures = info.get(
        "architectures",
        {}
    )

    arch_info = architectures.get(
        architecture
    )

    if arch_info is None:

        print(
            f"{Renk.KIRMIZI}"
            f"[!] {distro} için "
            f"{architecture} RootFS bulunamadı."
            f"{Renk.RESET}"
        )

        return

    if distro_kurulu_mu(
        distro
    ):

        print(
            f"{Renk.SARI}"
            f"[!] {distro} zaten kurulu."
            f"{Renk.RESET}"
        )

        return

    archive_url = arch_info.get(
        "url"
    )

    checksum = arch_info.get(
        "sha256"
    )

    if not archive_url:

        print(
            f"{Renk.KIRMIZI}"
            "[!] Repository manifestinde RootFS "
            "URL'si bulunamadı."
            f"{Renk.RESET}"
        )

        return

    filename = os.path.basename(
        archive_url
    )

    archive = os.path.join(
        DOWNLOAD_DIR,
        filename
    )

    hedef = distro_yolu(
        distro
    )

    print(
        f"[*] Distro       : "
        f"{info.get('name', distro)}"
    )

    print(
        f"[*] Version      : "
        f"{info.get('version', 'unknown')}"
    )

    print(
        f"[*] Architecture : "
        f"{architecture}"
    )

    print(
        f"[*] RootFS       : "
        f"{hedef}"
    )

    print()

    # --------------------------------------------------------
    # DOWNLOAD
    # --------------------------------------------------------

    if not os.path.exists(
        archive
    ):

        if not download_file(
            archive_url,
            archive
        ):

            return

    else:

        print(
            "[*] Arşiv cache'de bulundu."
        )

    # --------------------------------------------------------
    # CHECKSUM
    # --------------------------------------------------------

    if not verify_sha256(
        archive,
        checksum
    ):

        print(
            f"{Renk.KIRMIZI}"
            "[!] Güvenlik doğrulaması başarısız."
            f"{Renk.RESET}"
        )

        try:
            os.remove(
                archive
            )
        except Exception:
            pass

        return

    # --------------------------------------------------------
    # TEMP ROOTFS
    # --------------------------------------------------------

    temporary = os.path.join(
        ROOTFS_DIR,
        f".{distro}.installing"
    )

    if os.path.exists(
        temporary
    ):

        shutil.rmtree(
            temporary
        )

    os.makedirs(
        temporary,
        exist_ok=True
    )

    try:

        print()

        print(
            "[*] RootFS hazırlanıyor..."
        )

        safe_extract(
            archive,
            temporary
        )

        # ----------------------------------------------------
        # ROOTFS VALIDATION
        # ----------------------------------------------------

        required = [
            "bin",
            "etc",
            "usr"
        ]

        missing = []

        for item in required:

            path = os.path.join(
                temporary,
                item
            )

            if not os.path.exists(
                path
            ):

                missing.append(
                    item
                )

        if missing:

            raise RuntimeError(
                "Geçersiz RootFS. Eksik: "
                + ", ".join(
                    missing
                )
            )

        # ----------------------------------------------------
        # FINAL MOVE
        # ----------------------------------------------------

        if os.path.exists(
            hedef
        ):

            shutil.rmtree(
                hedef
            )

        os.rename(
            temporary,
            hedef
        )

        # ----------------------------------------------------
        # METADATA
        # ----------------------------------------------------

        create_metadata(
            distro,
            info
        )

        config = load_config()

        if distro not in config.get(
            "installed",
            []
        ):

            config.setdefault(
                "installed",
                []
            ).append(
                distro
            )

        if not config.get(
            "default_distro"
        ):

            config["default_distro"] = (
                distro
            )

        save_config(
            config
        )

        log_yaz(
            f"{distro} {architecture} "
            "RootFS başarıyla kuruldu."
        )

        print()

        print(
            f"{Renk.YESIL}"
            "[✓] RootFS başarıyla kuruldu."
            f"{Renk.RESET}"
        )

        print()

        print(
            f"Başlatmak için:"
        )

        print(
            f"  astra-distro join {distro}"
        )

    except Exception as hata:

        print()

        print(
            f"{Renk.KIRMIZI}"
            f"[X] RootFS kurulumu başarısız: "
            f"{hata}"
            f"{Renk.RESET}"
        )

        log_yaz(
            f"Install error: {distro} | {hata}"
        )

        if os.path.exists(
            temporary
        ):

            try:

                shutil.rmtree(
                    temporary
                )

            except Exception:
                pass


# ============================================================
# JOIN
# ============================================================

def join_distro(
    distro,
    command=None
):

    distro = distro.lower()

    if not distro_kurulu_mu(
        distro
    ):

        print(
            f"{Renk.KIRMIZI}"
            f"[!] {distro} kurulu değil."
            f"{Renk.RESET}"
        )

        print()

        print(
            f"Kurmak için:"
        )

        print(
            f"  astra-distro install {distro}"
        )

        return

    if not check_astra_proot():

        return

    rootfs = distro_yolu(
        distro
    )

    if command is None:

        command = "/bin/sh"

    print()

    print(
        f"{Renk.TURKUAZ}"
        "[ ASTRA-PROOT SESSION ]"
        f"{Renk.RESET}"
    )

    print()

    print(
        f"[*] Distro : {distro}"
    )

    print(
        f"[*] RootFS : {rootfs}"
    )

    print(
        f"[*] Engine : Astra-Proot"
    )

    print()

    komut = [
        ASTRA_PROOT,
        rootfs,
        command
    ]

    try:

        result = subprocess.run(
            komut
        )

        return result.returncode

    except Exception as hata:

        print(
            f"{Renk.KIRMIZI}"
            f"[!] Astra-Proot çalıştırılamadı: "
            f"{hata}"
            f"{Renk.RESET}"
        )

        log_yaz(
            f"Join error: {distro} | {hata}"
        )

        return 1


# ============================================================
# LIST
# ============================================================

def list_distro():

    config = load_config()

    installed = config.get(
        "installed",
        []
    )

    print()

    print(
        f"{Renk.YESIL}"
        "[ ASTRA-DISTRO ]"
        f"{Renk.RESET}"
    )

    print()

    if not installed:

        print(
            "Kurulu distro bulunmuyor."
        )

        return

    for distro in installed:

        metadata = read_metadata(
            distro
        )

        if metadata:

            name = metadata.get(
                "name",
                distro
            )

            version = metadata.get(
                "version",
                "?"
            )

            print(
                f"{Renk.YESIL}"
                "✓"
                f"{Renk.RESET} "
                f"{distro:<12} "
                f"{name:<18} "
                f"{version}"
            )

        else:

            print(
                f"{Renk.YESIL}"
                "✓"
                f"{Renk.RESET} "
                f"{distro}"
            )

    print()


# ============================================================
# INFO
# ============================================================

def distro_info(
    distro
):

    distro = distro.lower()

    path = distro_yolu(
        distro
    )

    metadata = read_metadata(
        distro
    )

    print()

    print(
        f"{Renk.YESIL}"
        "[ ASTRA-DISTRO INFO ]"
        f"{Renk.RESET}"
    )

    print()

    if metadata:

        print(
            f"Name          : "
            f"{metadata.get('name', distro)}"
        )

        print(
            f"Version       : "
            f"{metadata.get('version', '?')}"
        )

        print(
            f"Architecture  : "
            f"{metadata.get('architecture', '?')}"
        )

        print(
            f"RootFS        : "
            f"{path}"
        )

        print(
            f"Installed     : "
            f"{metadata.get('installed_at', '?')}"
        )

        print(
            f"Manager       : "
            f"{metadata.get('manager', 'Astra-Distro')}"
        )

    else:

        print(
            f"Distro        : {distro}"
        )

        print(
            f"RootFS        : {path}"
        )

        print(
            "Durum         : "
            + (
                "Kurulu"
                if distro_kurulu_mu(
                    distro
                )
                else "Kurulu değil"
            )
        )

    print()


# ============================================================
# REMOVE
# ============================================================

def remove_distro(
    distro
):

    distro = distro.lower()

    if not distro_kurulu_mu(
        distro
    ):

        print(
            f"{Renk.SARI}"
            f"[!] {distro} kurulu değil."
            f"{Renk.RESET}"
        )

        return

    print()

    print(
        f"{Renk.SARI}"
        f"[!] {distro} kaldırılacak."
        f"{Renk.RESET}"
    )

    cevap = input(
        "Devam etmek için 'yes' yaz: "
    ).strip().lower()

    if cevap != "yes":

        print(
            "[*] İşlem iptal edildi."
        )

        return

    try:

        shutil.rmtree(
            distro_yolu(
                distro
            )
        )

        config = load_config()

        if distro in config.get(
            "installed",
            []
        ):

            config["installed"].remove(
                distro
            )

        if config.get(
            "default_distro"
        ) == distro:

            config["default_distro"] = (
                config["installed"][0]
                if config["installed"]
                else None
            )

        save_config(
            config
        )

        log_yaz(
            f"{distro} kaldırıldı."
        )

        print(
            f"{Renk.YESIL}"
            "[✓] Distro kaldırıldı."
            f"{Renk.RESET}"
        )

    except Exception as hata:

        print(
            f"{Renk.KIRMIZI}"
            f"[!] Kaldırma hatası: {hata}"
            f"{Renk.RESET}"
        )


# ============================================================
# DEFAULT
# ============================================================

def default_distro(
    distro=None
):

    config = load_config()

    if distro is None:

        current = config.get(
            "default_distro"
        )

        if current:

            print(
                f"Varsayılan distro: "
                f"{current}"
            )

        else:

            print(
                "Varsayılan distro ayarlanmadı."
            )

        return

    distro = distro.lower()

    if not distro_kurulu_mu(
        distro
    ):

        print(
            f"{Renk.KIRMIZI}"
            f"[!] {distro} kurulu değil."
            f"{Renk.RESET}"
        )

        return

    config["default_distro"] = distro

    save_config(
        config
    )

    print(
        f"{Renk.YESIL}"
        f"[✓] Varsayılan distro: {distro}"
        f"{Renk.RESET}"
    )


# ============================================================
# DOCTOR
# ============================================================

def doctor():

    print()

    print(
        f"{Renk.YESIL}"
        "[ ASTRA-DISTRO DOCTOR ]"
        f"{Renk.RESET}"
    )

    print()

    problems = 0

    # --------------------------------------------------------
    # ROOT
    # --------------------------------------------------------

    print(
        "[*] Astra-Distro klasörü kontrol ediliyor..."
    )

    if os.path.isdir(
        ASTRA_DISTRO_ROOT
    ):

        print(
            f"{Renk.YESIL}"
            "[✓] Tamam"
            f"{Renk.RESET}"
        )

    else:

        print(
            f"{Renk.KIRMIZI}"
            "[X] Eksik"
            f"{Renk.RESET}"
        )

        problems += 1

    # --------------------------------------------------------
    # ASTRA-PROOT
    # --------------------------------------------------------

    print(
        "[*] Astra-Proot kontrol ediliyor..."
    )

    if check_astra_proot():

        print(
            f"{Renk.YESIL}"
            "[✓] Astra-Proot hazır."
            f"{Renk.RESET}"
        )

    else:

        problems += 1

    # --------------------------------------------------------
    # CONFIG
    # --------------------------------------------------------

    print(
        "[*] Config kontrol ediliyor..."
    )

    if os.path.isfile(
        CONFIG_FILE
    ):

        print(
            f"{Renk.YESIL}"
            "[✓] Config mevcut."
            f"{Renk.RESET}"
        )

    else:

        print(
            f"{Renk.SARI}"
            "[!] Config oluşturulacak."
            f"{Renk.RESET}"
        )

        save_config(
            default_config()
        )

    # --------------------------------------------------------
    # ROOTFS
    # --------------------------------------------------------

    config = load_config()

    for distro in config.get(
        "installed",
        []
    ):

        print(
            f"[*] {distro} RootFS kontrol ediliyor..."
        )

        path = distro_yolu(
            distro
        )

        if os.path.isdir(
            path
        ):

            print(
                f"{Renk.YESIL}"
                f"[✓] {distro}"
                f"{Renk.RESET}"
            )

        else:

            print(
                f"{Renk.KIRMIZI}"
                f"[X] {distro} RootFS eksik."
                f"{Renk.RESET}"
            )

            problems += 1

    print()

    if problems == 0:

        print(
            f"{Renk.YESIL}"
            "[✓] Astra-Distro'da sorun bulunamadı."
            f"{Renk.RESET}"
        )

    else:

        print(
            f"{Renk.SARI}"
            f"[!] {problems} sorun bulundu."
            f"{Renk.RESET}"
        )


# ============================================================
# SEARCH
# ============================================================

def search_distro(
    isim
):

    index = repository_index()

    if not index:

        return

    distros = index.get(
        "distros",
        {}
    )

    isim = isim.lower()

    bulundu = False

    print()

    for distro_id, info in distros.items():

        name = info.get(
            "name",
            distro_id
        )

        description = info.get(
            "description",
            ""
        )

        if (
            isim in distro_id.lower()
            or isim in name.lower()
            or isim in description.lower()
        ):

            bulundu = True

            print(
                f"{Renk.YESIL}"
                f"{distro_id}"
                f"{Renk.RESET}"
            )

            print(
                f"  {name}"
            )

            print(
                f"  {description}"
            )

            print()

    if not bulundu:

        print(
            f"{Renk.SARI}"
            "Sonuç bulunamadı."
            f"{Renk.RESET}"
        )


# ============================================================
# HELP
# ============================================================

def help_menu():

    print()

    print(
        f"{Renk.YESIL}"
        "[ ASTRA-DISTRO ]"
        f"{Renk.RESET}"
    )

    print()

    print(
        "astra-distro list"
    )

    print(
        "astra-distro search <isim>"
    )

    print(
        "astra-distro install <distro>"
    )

    print(
        "astra-distro join <distro>"
    )

    print(
        "astra-distro remove <distro>"
    )

    print(
        "astra-distro info <distro>"
    )

    print(
        "astra-distro default [distro]"
    )

    print(
        "astra-distro doctor"
    )

    print(
        "astra-distro version"
    )

    print(
        "astra-distro help"
    )

    print()


# ============================================================
# ANA ASTRA-DISTRO
# ============================================================

def astra_distro(
    args
):

    setup_directories()

    if not args:

        help_menu()

        return

    komut = args[0].lower()


    if komut in (
        "help",
        "--help",
        "-h"
    ):

        help_menu()

        return


    if komut in (
        "version",
        "--version",
        "-v"
    ):

        print(
            f"Astra-Distro "
            f"{ASTRA_DISTRO_VERSION}"
        )

        return


    if komut == "list":

        list_distro()

        return


    if komut == "search":

        if len(args) < 2:

            print(
                "[!] Arama adı belirtmelisin."
            )

            return

        search_distro(
            args[1]
        )

        return


    if komut == "install":

        if len(args) < 2:

            print(
                "[!] Distro adı belirtmelisin."
            )

            return

        install_distro(
            args[1]
        )

        return


    if komut == "join":

        if len(args) < 2:

            print(
                "[!] Distro adı belirtmelisin."
            )

            return

        join_distro(
            args[1]
        )

        return


    if komut == "remove":

        if len(args) < 2:

            print(
                "[!] Distro adı belirtmelisin."
            )

            return

        remove_distro(
            args[1]
        )

        return


    if komut == "info":

        if len(args) < 2:

            print(
                "[!] Distro adı belirtmelisin."
            )

            return

        distro_info(
            args[1]
        )

        return


    if komut == "default":

        if len(args) >= 2:

            default_distro(
                args[1]
            )

        else:

            default_distro()

        return


    if komut == "doctor":

        doctor()

        return


    print(
        f"{Renk.KIRMIZI}"
        f"[!] Bilinmeyen Astra-Distro komutu: "
        f"{komut}"
        f"{Renk.RESET}"
    )


# ============================================================
# DOĞRUDAN ÇALIŞTIRMA
# ============================================================

if __name__ == "__main__":

    try:

        astra_distro(
            sys.argv[1:]
        )

    except KeyboardInterrupt:

        print()

        print(
            f"{Renk.SARI}"
            "[*] İşlem iptal edildi."
            f"{Renk.RESET}"
        )

    except Exception as hata:

        print()

        print(
            f"{Renk.KIRMIZI}"
            "[X] Astra-Distro kritik hata:"
            f"{Renk.RESET}"
        )

        print(
            hata
        )

        raise