from enum import StrEnum

class NvencPresets(StrEnum):
    P1 = "p1"
    P2 = "p2"
    P3 = "p3"
    P4 = "p4"
    P5 = "p5"
    P6 = "p6"
    P7 = "p7"
    
    def __str__(self):
        return self.value