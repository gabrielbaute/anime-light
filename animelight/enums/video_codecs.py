from enum import StrEnum

class VideoCodecs(StrEnum):
    H264 = "libx264"
    HEVC = "libx265"
    VP9 = "libvpx-vp9"
    AV1 = "libaom-av1"

    def __str__(self):
        return self.value