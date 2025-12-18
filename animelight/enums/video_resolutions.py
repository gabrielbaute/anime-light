from enum import StrEnum

class VideoResolution(StrEnum):
    P_360 = "640:360"
    P_480 = "854:480"
    P_720 = "1280:720"
    P_1080 = "1920:1080"
    P_2160 = "3840:2160"
    P_4320 = "7680:4320"

    def __str__(self):
        return self.value
       
    def to_height(self) -> int:
        """
        Returns the height of the resolution.
        """
        return int(self.value.split(":")[1])
    
    def to_width(self)-> int:
        """
        Returns the width of the resolution.
        """
        return int(self.value.split(":")[0])