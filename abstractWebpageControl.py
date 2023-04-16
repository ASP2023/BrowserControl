from abc import ABC, abstractmethod


class AbstractWebpageControl(ABC):
    @abstractmethod
    def slowScrollUp(self):
        pass

    @abstractmethod
    def slowScrollDown(self):
        pass

    @abstractmethod
    def quickSCrollUp(self):
        self.scrollUp()

    @abstractmethod
    def quickScrollDown(self):
        self.scrollDown()

    @abstractmethod
    def scrollUp(self):
        pass

    @abstractmethod
    def scrollDown(self):
        pass

    @abstractmethod
    def moveForward(self):
        pass

    @abstractmethod
    def moveBack(self):
        pass

    @abstractmethod
    def next(self):
        pass

    @abstractmethod
    def prev(self):
        pass

    @abstractmethod
    def playOrPause(self):
        pass
