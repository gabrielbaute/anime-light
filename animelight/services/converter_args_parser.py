from animelight.enums import (
    VideoResolution, 
    VideoCodecs, 
    AudioCodecs, 
    AudioBitrates, 
    FfmpegPresets, 
    GPUMethods,
    VaapiQuality,
    NvencPresets
)

class ConversionArgsParser:
    """
    Parser for conversion arguments.
    """
    @staticmethod
    def parse_resolution(resolution: str) -> VideoResolution:
        """
        Parse a resolution string value to a VideoResolution enum.

        Args:
            resolution (str): The resolution string.

        Returns:
            VideoResolution: The corresponding VideoResolution enum.
        """
        RESOLUTION_MAP = {
            360: VideoResolution.P_360,
            480: VideoResolution.P_480,
            720: VideoResolution.P_720,
            1080: VideoResolution.P_1080,
            2160: VideoResolution.P_2160,
            4320: VideoResolution.P_4320
            }
        return RESOLUTION_MAP.get(resolution)
    
    @staticmethod
    def parse_audio_bitrate(bitrate: int) -> AudioBitrates:
        """
        Parse an audio bitrate value to an AudioBitrates enum.

        Args:
            bitrate (int): The audio bitrate value.

        Returns:
            AudioBitrates: The corresponding AudioBitrates enum.
        """
        AUDIO_BITRATE_MAP = {
            96: AudioBitrates.B_96K,
            128: AudioBitrates.B_128K,
            192: AudioBitrates.B_192K,
            256: AudioBitrates.B_256K,
            320: AudioBitrates.B_320K,
            }
        return AUDIO_BITRATE_MAP.get(bitrate)

    @staticmethod
    def parse_video_codec(codec: str) -> VideoCodecs:
        """
        Parse a video codec string value to a VideoCodecs enum.

        Args:
            codec (str): The video codec string.

        Returns:
            VideoCodecs: The corresponding VideoCodecs enum.
        """
        VIDEO_CODECS_MAP = {
            "h264": VideoCodecs.H264,
            "hevc": VideoCodecs.HEVC,
            "vp9": VideoCodecs.VP9,
            "avi": VideoCodecs.AV1
            }
        return VIDEO_CODECS_MAP.get(codec)

    @staticmethod
    def parse_audio_codec(codec: str) -> AudioCodecs:
        """
        Parse an audio codec string value to an AudioCodecs enum.

        Args:
            codec (str): The audio codec string.

        Returns:
            AudioCodecs: The corresponding AudioCodecs enum.
        """
        ADUIO_CODECS_MAP = {
            "aac": AudioCodecs.AAC,
            "ac3": AudioCodecs.AC3,
            "eac3": AudioCodecs.EAC3,
            "mp3": AudioCodecs.MP3,
            "opus": AudioCodecs.OPUS,
            "libopus": AudioCodecs.LIBOPUS,
            "vorbis": AudioCodecs.VORBIS,
            "libvorbis": AudioCodecs.LIBVORBIS,
            "libfaac": AudioCodecs.LIBFDK_AAC,
            "flac": AudioCodecs.FLAC,
            "libflac": AudioCodecs.LIBFLAC
            }
        return ADUIO_CODECS_MAP.get(codec)

    @staticmethod
    def parse_ffmpeg_preset(preset: str) -> FfmpegPresets:
        """
        Parse a ffmpeg preset string value to an FfmpegPresets enum.

        Args:
            preset (str): The ffmpeg preset string.

        Returns:
            FfmpegPresets: The corresponding FfmpegPresets enum.
        """
        FFMPEG_PRESETS_MAP = {
            "ultrafast": FfmpegPresets.ULTRAFAST,
            "superfast": FfmpegPresets.SUPERFAST,
            "veryfast": FfmpegPresets.VERYFAST,
            "faster": FfmpegPresets.FASTER,
            "fast": FfmpegPresets.FAST,
            "medium": FfmpegPresets.MEDIUM,
            "slow": FfmpegPresets.SLOW,
            "slower": FfmpegPresets.SLOWER,
            "veryslow": FfmpegPresets.VERYSLOW
            }
        return FFMPEG_PRESETS_MAP.get(preset)
    
    @staticmethod
    def parse_gpu_method(gpu_method: str) -> GPUMethods:
        """
        Parse a GPU method string value to a GPUMethods enum.

        Args:
            gpu_method (str): The GPU method string.

        Returns:
            GPUMethods: The corresponding GPUMethods enum.
        """
        GPU_METHODS_MAP = {
            "nvidia": GPUMethods.NVIDIA,
            "intel": GPUMethods.INTEL,
            "linux_amd": GPUMethods.LINUX_AMD
            }
        return GPU_METHODS_MAP.get(gpu_method)
    
    @staticmethod
    def parse_vaapi_quality(quality: str) -> VaapiQuality:
        """
        Parse a VAAPI quality string value to a VaapiQuality enum.

        Args:
            quality (str): The VAAPI quality string.

        Returns:
            VaapiQuality: The corresponding VaapiQuality enum.
        """
        VAAPI_QUALITY_MAP = {
            "speed": VaapiQuality.SPEED,
            "balanced": VaapiQuality.BALANCED,
            "quality": VaapiQuality.QUALITY
            }
        return VAAPI_QUALITY_MAP.get(quality)
    
    @staticmethod
    def parse_nvenc_preset(preset: str) -> NvencPresets:
        """
        Parse a NVENC preset string value to a NvencPresets enum.

        Args:
            preset (str): The NVENC preset string.

        Returns:
            NvencPresets: The corresponding NvencPresets enum.
        """
        NVENC_PRESETS_MAP = {
            "p1": NvencPresets.P1,
            "p2": NvencPresets.P2,
            "p3": NvencPresets.P3,
            "p4": NvencPresets.P4,
            "p5": NvencPresets.P5,
            "p6": NvencPresets.P6,
            "p7": NvencPresets.P7
            }
        return NVENC_PRESETS_MAP.get(preset)