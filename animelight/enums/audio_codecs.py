from enum import StrEnum

class AudioCodecs(StrEnum):
    AAC = "aac"
    AC3 = "ac3"
    EAC3 = "eac3"
    MP3 = "mp3"
    OPUS = "opus"
    LIBOPUS = "libopus"
    VORBIS = "vorbis"
    LIBVORBIS = "libvorbis"
    LIBFDK_AAC = "libfaac"
    FLAC = "flac"
    LIBFLAC = "libflac"

    def __str__(self):
        return self.value