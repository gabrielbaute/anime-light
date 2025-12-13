from anime_light.enums import VideoResolution, VideoCodecs, AudioCodecs, AudioBitrates, FfmpegPresets

class ConversionProfilesService:
    @staticmethod
    def anime_low_size():
        return dict(
            crf=25,
            preset=FfmpegPresets.SLOW,
            scale=VideoResolution.P_480,
            video_codec=VideoCodecs.H264,
            audio_codec=AudioCodecs.AAC,
            audio_bitrate=AudioBitrates.B_96K
        )

    @staticmethod
    def movie_high_quality():
        return dict(
            crf=20,
            preset=FfmpegPresets.VERYSLOW,
            scale=VideoResolution.P_1080,
            video_codec=VideoCodecs.HEVC,
            audio_codec=AudioCodecs.EAC3,
            audio_bitrate=AudioBitrates.B_320K
        )

    @staticmethod
    def screencast_fast():
        return dict(
            crf=28,
            preset=FfmpegPresets.FAST,
            scale=VideoResolution.P_720,
            video_codec=VideoCodecs.VP9,
            audio_codec=AudioCodecs.OPUS,
            audio_bitrate=AudioBitrates.B_128K
        )
