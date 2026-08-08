/*
 * Astra-Proot
 * AstraSage Project
 *
 * Özgün userspace/rootfs çalışma motoru - Prototype v0.1
 *
 * Derleme:
 *     clang astra-proot.c -o astra-proot
 *
 * Kullanım:
 *     ./astra-proot ./rootfs /bin/sh
 *
 * NOT:
 * Bu sürüm tam PRoot değildir.
 * Gerçek syscall/path/mount emülasyonu sonraki sürümlerde
 * ayrı native katmanlar olarak geliştirilecektir.
 */

#define _GNU_SOURCE

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <errno.h>
#include <string.h>
#include <limits.h>


/* ============================================================
 * SABİTLER
 * ============================================================ */

#define ASTRA_PROOT_VERSION "0.1.0"

#define ASTRA_OK     0
#define ASTRA_ERROR  1


/* ============================================================
 * RENKLER
 * ============================================================ */

#define GREEN   "\033[92m"
#define RED     "\033[91m"
#define YELLOW  "\033[93m"
#define CYAN    "\033[96m"
#define RESET   "\033[0m"


/* ============================================================
 * GLOBAL
 * ============================================================ */

static char rootfs_path[PATH_MAX];


/* ============================================================
 * YARDIM
 * ============================================================ */

static void print_help(void)
{
    printf(
        "\n"
        "Astra-Proot %s\n"
        "\n"
        "Kullanim:\n"
        "  astra-proot <rootfs> <command> [args...]\n"
        "\n"
        "Ornek:\n"
        "  astra-proot ./rootfs /bin/sh\n"
        "\n"
        "Secenekler:\n"
        "  --help       Yardim\n"
        "  --version    Surum\n"
        "\n",
        ASTRA_PROOT_VERSION
    );
}


static void print_version(void)
{
    printf(
        "Astra-Proot %s\n",
        ASTRA_PROOT_VERSION
    );
}


/* ============================================================
 * ROOTFS KONTROLÜ
 * ============================================================ */

static int check_rootfs(const char *path)
{
    struct stat st;

    if (stat(path, &st) != 0)
    {
        fprintf(
            stderr,
            RED "[Astra-Proot] RootFS bulunamadi: %s\n" RESET,
            path
        );

        return ASTRA_ERROR;
    }

    if (!S_ISDIR(st.st_mode))
    {
        fprintf(
            stderr,
            RED "[Astra-Proot] RootFS bir klasor degil.\n" RESET
        );

        return ASTRA_ERROR;
    }

    return ASTRA_OK;
}


/* ============================================================
 * ROOTFS YOLU
 * ============================================================ */

static int prepare_rootfs(const char *path)
{
    char real_path[PATH_MAX];

    if (realpath(path, real_path) == NULL)
    {
        fprintf(
            stderr,
            RED "[Astra-Proot] RootFS yolu cozumlenemedi: %s\n" RESET,
            strerror(errno)
        );

        return ASTRA_ERROR;
    }

    strncpy(
        rootfs_path,
        real_path,
        sizeof(rootfs_path) - 1
    );

    rootfs_path[
        sizeof(rootfs_path) - 1
    ] = '\0';

    return ASTRA_OK;
}


/* ============================================================
 * ROOTFS ICINDE KOMUT YOLU
 * ============================================================ */

static int build_command_path(
    const char *command,
    char *output,
    size_t output_size
)
{
    if (command == NULL)
        return ASTRA_ERROR;

    if (command[0] != '/')
    {
        /*
         * Relative komutlar:
         *
         * sh
         * bash
         * ls
         *
         * -> /bin/sh
         * -> /bin/bash
         * -> /bin/ls
         *
         * seklinde aranacak.
         */

        snprintf(
            output,
            output_size,
            "%s/bin/%s",
            rootfs_path,
            command
        );
    }
    else
    {
        snprintf(
            output,
            output_size,
            "%s%s",
            rootfs_path,
            command
        );
    }

    return ASTRA_OK;
}


/* ============================================================
 * ORTAM DEĞİŞKENLERİ
 * ============================================================ */

static void setup_environment(void)
{
    char path_value[PATH_MAX * 2];

    /*
     * RootFS icindeki PATH.
     */

    snprintf(
        path_value,
        sizeof(path_value),
        "/usr/local/sbin:"
        "/usr/local/bin:"
        "/usr/sbin:"
        "/usr/bin:"
        "/sbin:"
        "/bin"
    );

    setenv(
        "PATH",
        path_value,
        1
    );

    setenv(
        "HOME",
        "/root",
        1
    );

    setenv(
        "USER",
        "root",
        1
    );

    setenv(
        "SHELL",
        "/bin/sh",
        1
    );

    setenv(
        "ASTRA_PROOT",
        "1",
        1
    );

    setenv(
        "ASTRA_PROOT_VERSION",
        ASTRA_PROOT_VERSION,
        1
    );
}


/* ============================================================
 * PROCESS
 * ============================================================ */

static pid_t create_process(void)
{
    pid_t pid;

    pid = fork();

    if (pid < 0)
    {
        fprintf(
            stderr,
            RED "[Astra-Proot] fork() basarisiz: %s\n" RESET,
            strerror(errno)
        );

        return -1;
    }

    return pid;
}


/* ============================================================
 * CHILD PROCESS
 * ============================================================ */

static void child_process(
    int argc,
    char **argv
)
{
    char command_path[PATH_MAX];

    /*
     * RootFS'e gec.
     *
     * Bu ilk prototipte gerçek chroot kullanıyoruz.
     * Android'de root yetkisi gerektirebilir.
     *
     * Sonraki Astra-Proot sürümlerinde burada
     * gerçek userspace path/sycall mekanizması olacak.
     */

    if (chroot(rootfs_path) != 0)
    {
        fprintf(
            stderr,
            RED "[Astra-Proot] chroot basarisiz: %s\n" RESET,
            strerror(errno)
        );

        _exit(127);
    }

    if (chdir("/") != 0)
    {
        fprintf(
            stderr,
            RED "[Astra-Proot] chdir basarisiz: %s\n" RESET,
            strerror(errno)
        );

        _exit(127);
    }

    setup_environment();

    /*
     * Komut yolunu hazırla.
     */

    if (build_command_path(
        argv[2],
        command_path,
        sizeof(command_path)
    ) != ASTRA_OK)
    {
        _exit(127);
    }

    /*
     * Gerçek rootfs içindeki binary.
     */

    execv(
        command_path,
        &argv[2]
    );

    /*
     * exec başarısız.
     */

    fprintf(
        stderr,
        RED "[Astra-Proot] Komut calistirilamadi: %s\n" RESET,
        strerror(errno)
    );

    fprintf(
        stderr,
        YELLOW
        "[Astra-Proot] Aranan dosya: %s\n"
        RESET,
        command_path
    );

    _exit(127);
}


/* ============================================================
 * PROCESS BEKLEME
 * ============================================================ */

static int wait_process(pid_t pid)
{
    int status;

    while (1)
    {
        pid_t result = waitpid(
            pid,
            &status,
            0
        );

        if (result < 0)
        {
            if (errno == EINTR)
                continue;

            fprintf(
                stderr,
                RED
                "[Astra-Proot] waitpid() basarisiz: %s\n"
                RESET,
                strerror(errno)
            );

            return ASTRA_ERROR;
        }

        break;
    }

    if (WIFEXITED(status))
    {
        return WEXITSTATUS(status);
    }

    if (WIFSIGNALED(status))
    {
        return 128 + WTERMSIG(status);
    }

    return ASTRA_ERROR;
}


/* ============================================================
 * ANA MOTOR
 * ============================================================ */

static int astra_proot_run(
    int argc,
    char **argv
)
{
    pid_t pid;

    /*
     * RootFS kontrolü.
     */

    if (check_rootfs(argv[1]) != ASTRA_OK)
    {
        return ASTRA_ERROR;
    }

    /*
     * RootFS yolunu hazırla.
     */

    if (prepare_rootfs(argv[1]) != ASTRA_OK)
    {
        return ASTRA_ERROR;
    }

    printf(
        CYAN
        "[Astra-Proot] RootFS: %s\n"
        RESET,
        rootfs_path
    );

    printf(
        GREEN
        "[Astra-Proot] Session baslatiliyor...\n"
        RESET
    );

    fflush(stdout);

    /*
     * Process oluştur.
     */

    pid = create_process();

    if (pid < 0)
    {
        return ASTRA_ERROR;
    }

    /*
     * CHILD
     */

    if (pid == 0)
    {
        child_process(
            argc,
            argv
        );

        return ASTRA_ERROR;
    }

    /*
     * PARENT
     */

    return wait_process(pid);
}


/* ============================================================
 * MAIN
 * ============================================================ */

int main(
    int argc,
    char **argv
)
{
    if (argc < 2)
    {
        print_help();
        return ASTRA_ERROR;
    }

    if (
        strcmp(argv[1], "--help") == 0 ||
        strcmp(argv[1], "-h") == 0
    )
    {
        print_help();
        return ASTRA_OK;
    }

    if (
        strcmp(argv[1], "--version") == 0 ||
        strcmp(argv[1], "-v") == 0
    )
    {
        print_version();
        return ASTRA_OK;
    }

    if (argc < 3)
    {
        fprintf(
            stderr,
            RED
            "[Astra-Proot] RootFS ve komut belirtilmeli.\n"
            RESET
        );

        print_help();

        return ASTRA_ERROR;
    }

    return astra_proot_run(
        argc,
        argv
    );
}