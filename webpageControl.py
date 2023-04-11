from abc import ABC, abstractmethod

class WebpageControl(ABC):
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