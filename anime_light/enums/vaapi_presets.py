from enum import StrEnum

class VaapiQuality(StrEnum):
    SPEED = "speed"
    BALANCED = "balanced"
    QUALITY = "quality"

    def __str__(self):
        return self.value