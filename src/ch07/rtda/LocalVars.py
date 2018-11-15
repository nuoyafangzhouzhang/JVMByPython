from ch07.rtda.Slot import Slot
import copy

class LocalVars():
    def __init__(self, maxLocals):
        self.slots = []
        if maxLocals > 0:
            self.slots = [Slot() for i in range(maxLocals)]

    def setNumeric(self, index, val):
        self.slots[index].num = val

    def getNumeric(self, index):
        return self.slots[index].num

    def setRef(self, index, ref):
        self.slots[index].ref = ref

    def getRef(self, index):
        return self.slots[index].ref

    def setSlot(self, index, slot):
        self.slots[index] = copy.deepcopy(slot)

    def __str__(self):
        return "slots:{0}".format([str(t) for t in self.slots])