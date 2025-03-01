from functions import *


def config(de_name: str, distro_version: str, verbose_var: bool) -> None:
    # set verbose var
    global verbose
    verbose = verbose_var

    print("\033[96m" + "Configuring Fedora" + "\033[0m")
    print("Installing packages")
    chroot("dnf update -y")
    chroot("dnf install linux-firmware -y")
    chroot("dnf group install 'Minimal Install' -y; dnf install NetworkManager-tui ncurses cloud-utils -y")
    print("Add nonfree repos")
    chroot(f"dnf install https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-{distro_version}"
           f".noarch.rpm -y")
    print("Disabling plymouth")  # may fail sometimes without error
    chroot("plymouth-set-default-theme details -R &> /dev/null")
    # TODO: Perhaps zram works with mainline?
    chroot("dnf remove zram-generator-defaults -y")  # remove zram as it fails for some reason
    chroot("systemctl disable systemd-zram-setup@zram0.service")  # disable zram service
    print("\033[96m" + "Downloading and installing DE, might take a while" + "\033[0m")
    match de_name:
        case "gnome":
            print("Installing gnome")
            # As gnome is not preinstalled on the cloud version, we need to install it "manually"
            chroot(
                "dnf install -y @base-x gnome-shell gnome-terminal nautilus firefox chrome-gnome-shell gnome-tweaks " +
                "@development-tools gnome-terminal-nautilus xdg-user-dirs xdg-user-dirs-gtk gnome-calculator " +
                "gnome-system-monitor gedit file-roller gdm gnome-initial-setup")
            chroot("systemctl enable gdm.service")
        case "kde":
            print("Installing kde")
            chroot("dnf group install -y 'KDE Plasma Workspaces'")
        case "mate":
            print("Installing mate")
            chroot("dnf group install -y 'MATE Desktop'")
        case "xfce" | "minimal":
            print("Installing xfce")
            chroot("dnf group install -y 'Xfce Desktop'")
        case "lxqt":
            print("Installing lxqt")
            chroot("dnf group install -y 'LXQt Desktop'")
        case "deepin":
            print("Installing deepin")
            chroot("dnf group install -y 'Deepin Desktop'")
        case "budgie":
            print("\033[91m" + "Budgie is not available for Fedora" + "\033[91m")
            exit(1)
        case "minimal":
            # TODO: Add minimal
            print("\033[91m" + "Minimal is not available YET for Fedora" + "\033[91m")
        case "cli":
            print("Installing nothing")
        case _:
            print("\033[91m" + "Invalid desktop environment!!! Remove all files and retry." + "\033[0m")
            exit(1)
    print("Set SELinux to permissive")
    chroot("sed -i 's/SELINUX=enforcing/SELINUX=permissive/g' /etc/sysconfig/selinux")
    # print("Fix permissions")  # maybe not needed?
    # chroot("chmod -R 750 /root")


def chroot(command: str) -> None:
    if verbose:
        bash(f'chroot /mnt/eupnea /bin/sh -c "{command}"')
    else:
        bash(f'chroot /mnt/eupnea /bin/sh -c "{command}" 2>/dev/null 1>/dev/null')  # supress all output


if __name__ == "__main__":
    print("Do not run this file. Use build.py")
