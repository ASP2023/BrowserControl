from abc import ABC, abstractmethod


class AbstractWebpageControl(ABC):
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



def bfs():
    q = []
    ans = 0
    while q:
        now = q.pop(0)
        ans += len(q)
        xxxx
    return ans 
