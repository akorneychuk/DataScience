import matplotlib.pyplot as plt
import abc

from celluloid import Camera


class ICamera:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def snap(self):
        return

    @abc.abstractmethod
    def save(self, file_name):
        return


class RealCamera(ICamera):
    def __init__(self, fig):
        self.camera = Camera(fig)

    def snap(self):
        self.camera.snap()

    def save(self, file_name):
        anim = self.camera.animate()
        anim.save('../render_outputs/' + file_name + '.mp4')


class FakeCamera(ICamera):
    def __init__(self, fig):
        print("ICamera - Construct")

    def snap(self):
        print("ICamera - Capture")

    def save(self, file_name):
        print("ICamera - Save: " + file_name)
