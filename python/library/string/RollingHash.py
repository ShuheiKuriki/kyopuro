# 1-dimension Rolling Hash
import random

class RH:    
    mask30 = (1 << 30) - 1
    mask31 = (1 << 31) - 1
    MOD = (1 << 61) - 1
    Base = None
    power = [1]
    
    def __init__(self, S):
        if RH.Base is None:
            RH.Base = random.randrange(129, 1 << 30)
        for i in range(len(RH.power), len(S) + 1):
            RH.power.append(RH.calcMod(RH.mul(RH.power[i - 1], self.__class__.Base)))
        
        self.hash = [0] * (len(S) + 1)
        for i, s in enumerate(S, 1):
            self.hash[i] = RH.calcMod(RH.mul(self.hash[i - 1], RH.Base) + ord(s))

    def get(self, l, r):
        return RH.calcMod(self.hash[r] - RH.mul(self.hash[l], RH.power[r - l]))

    def mul(l, r):
        lu = l >> 31
        ld = l & RH.mask31
        ru = r >> 31
        rd = r & RH.mask31
        middlebit = ld * ru + lu * rd
        return ((lu * ru) << 1) + ld * rd + ((middlebit & RH.mask30) << 31) + (middlebit >> 30)

    def calcMod(val):
        if val < 0:
            val %= RH.MOD
        val = (val & RH.MOD) + (val >> 61)
        if val > RH.MOD:
            val -= RH.MOD
        return val

N = int(input())
S = input()
RHS = RH(S)