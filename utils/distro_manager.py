# ============================================================
# DISTRO MANAGER
# ============================================================

class Distro:
    def __init__(self, name="Unknown"):
        self.name = name


class DistroManager:

    def __init__(self):
        self.distro = Distro()

    def load(self, module):
        """
        Verilen distro modülündeki DISTRO değişkenini okur.
        """

        name = getattr(module, "DISTRO", None)

        if not name:
            name = "Unknown"

        self.distro = Distro(name)

        return self.distro


distro_manager = DistroManager()