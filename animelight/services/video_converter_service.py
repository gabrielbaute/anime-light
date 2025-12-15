import re
import subprocess
import shutil
import logging
from pathlib import Path
from typing import Optional, List
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn

from animelight.models.video_file import VideoFileInfo
from animelight.models.conversion_result import ConversionResult
from animelight.enums import VideoResolution, GPUMethods, AudioBitrates, VideoCodecs, AudioCodecs, FfmpegPresets

class VideoConverterService:
    def __init__(self, video_info: VideoFileInfo, output_dir: Path = Path("output"), temp_dir: Path = Path("temp")):
        self.video_info = video_info
        self.output_dir = output_dir
        self.temp_dir = temp_dir
        self.logger = logging.getLogger(self.__class__.__name__)

        self.output_dir.mkdir(exist_ok=True)
        self.temp_dir.mkdir(exist_ok=True)

    def _build_gpu_params(self, gpu_method: GPUMethods, crf: int, video_codec: VideoCodecs) -> List[str]:
        """
        Build the GPU parameters for the ffmpeg command.

        Args:
            gpu_method (GPUMethods): The GPU method to use.
            crf (int): The Constant Rate Factor (CRF) value.
            video_codec (VideoCodecs): The video codec to use.

        Returns:
            List[str]: The list of GPU parameters
        """
        gpu_params = []
        if gpu_method == GPUMethods.INTEL:
            self.logger.debug("Using Intel GPU")
            gpu_params.extend([
                "-hwaccel", "qsv",
                "-hwaccel_output_format", "qsv",
                "-c:v", "h264_qsv" if video_codec == VideoCodecs.H264 else video_codec.value,
                "-global_quality", str(crf),
                "-preset", "fast"
            ])
        elif gpu_method == GPUMethods.NVIDIA:
            self.logger.debug("Using NVIDIA GPU")
            gpu_params.extend([
                "-hwaccel", "cuda",
                "-hwaccel_output_format", "cuda",
                "-c:v", "h264_nvenc" if video_codec == VideoCodecs.H264 else video_codec.value,
                "-cq", str(crf),
                "-preset", "p4"
            ])
        elif gpu_method == GPUMethods.LINUX_AMD:
            self.logger.debug("Using Linux AMD GPU")
            gpu_params.extend([
                "-hwaccel", "vaapi",
                "-hwaccel_output_format", "vaapi",
                "-c:v", "h264_vaapi" if video_codec == VideoCodecs.H264 else video_codec.value,
                "-qp", str(crf),
                "-quality", "speed"
            ])
        return gpu_params

    def _ffmpeg_command(
        self,
        crf: int,
        preset: FfmpegPresets,
        scale: VideoResolution,
        gpu_method: Optional[GPUMethods],
        audio_bitrate: AudioBitrates,
        video_codec: VideoCodecs,
        audio_codec: AudioCodecs,
        threads: int = 1
    ) -> List[str]:
        """
        Build the ffmpeg command for video conversion.

        Args:
            crf (int): The Constant Rate Factor (CRF) value.
            preset (FfmpegPresets): The ffmpeg preset to use.
            scale (VideoResolution): The video resolution to use.
            gpu_method (Optional[GPUMethods]): The GPU method to use.
            audio_bitrate (AudioBitrates): The audio bitrate to use.
            video_codec (VideoCodecs): The video codec to use.
            audio_codec (AudioCodecs): The audio codec to use.
            threads (int): The number of threads to use.

        Returns:
            List[str]: The list of ffmpeg command
        """
        self.logger.debug(f"Building ffmpeg command for {self.video_info.path}")
        temp_file = self.temp_dir / f"{self.video_info.path.stem}_temp.mp4"
        cmd = ["ffmpeg", "-i", str(self.video_info.path)]

        if gpu_method:
            cmd.extend(self._build_gpu_params(gpu_method, crf, video_codec))
            # Specific scale for GPU model
            if gpu_method == GPUMethods.INTEL:
                cmd.extend(["-vf", f"scale_qsv={scale.value}"])
            elif gpu_method == GPUMethods.NVIDIA:
                cmd.extend(["-vf", f"scale_cuda={scale.value}"])
            elif gpu_method == GPUMethods.LINUX_AMD:
                cmd.extend(["-vf", f"scale_vaapi={scale.value}"])
        else:
            cmd.extend([
                "-c:v", video_codec.value,
                "-crf", str(crf),
                "-preset", preset.value,
                "-vf", f"scale={scale.value}",
                "-threads", str(threads)
            ])

        cmd.extend([
            "-tune", "animation",
            "-pix_fmt", "yuv420p",
            "-c:a", audio_codec.value,
            "-b:a", audio_bitrate.value,
            "-y",
            str(temp_file)
        ])
        return cmd, temp_file

    def convert(
        self,
        crf: int,
        preset: FfmpegPresets,
        scale: VideoResolution,
        gpu_method: Optional[GPUMethods] = None,
        audio_bitrate: AudioBitrates = AudioBitrates.B_128K,
        video_codec: VideoCodecs = VideoCodecs.H264,
        audio_codec: AudioCodecs = AudioCodecs.AAC,
        threads: int = 1
    ) -> ConversionResult:
        """
        Convert the video file.

        Args:
            crf (int): The Constant Rate Factor (CRF) value.
            preset (FfmpegPresets): The ffmpeg preset to use.
            scale (VideoResolution): The video resolution to use.
            gpu_method (Optional[GPUMethods]): The GPU method to use.
            audio_bitrate (AudioBitrates): The audio bitrate to use.
            video_codec (VideoCodecs): The video codec to use.
            audio_codec (AudioCodecs): The audio codec to use.
            threads (int): The number of threads to use.

        Returns:
            ConversionResult: The conversion result.
        """
        cmd, temp_file = self._ffmpeg_command(crf, preset, scale, gpu_method, audio_bitrate, video_codec, audio_codec, threads)
        self.logger.debug(f"Running ffmpeg command: {' '.join(cmd)}")

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            success = result.returncode == 0
            output_file = self.output_dir / f"{self.video_info.path.stem}_converted.mp4"

            if success and temp_file.exists():
                self.logger.debug(f"Moving temp file to {output_file}")
                shutil.move(temp_file, output_file)

            if temp_file.exists():
                self.logger.debug(f"Deleting temp file {temp_file}")
                temp_file.unlink()

            result = ConversionResult(
                success=success,
                input_file=self.video_info.path,
                output_file=output_file if success else None,
                command=cmd,
                log=result.stderr,
                duration_seconds=self.video_info.duration_seconds,
                error_message=None if success else "Conversion failed"
            )
            self.logger.info(f"Conversion result: {result.model_dump_json(indent=4, exclude_none=True)}")
            return result
        except Exception as e:
            self.logger.error(f"Conversion failed: {e}")
            return ConversionResult(
                success=False,
                input_file=self.video_info.path,
                output_file=None,
                command=cmd,
                log=None,
                duration_seconds=self.video_info.duration_seconds,
                error_message=str(e)
            )

    def convert_with_progress_bar(
        self,
        crf: int,
        preset: FfmpegPresets,
        scale: VideoResolution,
        console: Console,
        gpu_method: Optional[GPUMethods] = None,
        audio_bitrate: AudioBitrates = AudioBitrates.B_128K,
        video_codec: VideoCodecs = VideoCodecs.H264,
        audio_codec: AudioCodecs = AudioCodecs.AAC,
        threads: int = 1,
    ) -> ConversionResult:
        """
        Convert the video file showing a progress bar in real time.
        """
        cmd, temp_file = self._ffmpeg_command(
            crf, preset, scale, gpu_method,
            audio_bitrate, video_codec, audio_codec, threads
        )
        self.logger.debug(f"Running ffmpeg command with progress: {' '.join(cmd)}")

        duration = self.video_info.duration_seconds
        process = subprocess.Popen(cmd, stderr=subprocess.PIPE, text=True)

        time_pattern = re.compile(r"time=(\d+):(\d+):(\d+\.\d+)")

        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            console=console,
        ) as progress:
            task = progress.add_task("Converting...", total=duration)

            for line in process.stderr:
                match = time_pattern.search(line)
                if match:
                    h, m, s = match.groups()
                    current_time = int(h) * 3600 + int(m) * 60 + float(s)
                    progress.update(task, completed=current_time)

            process.wait()

        success = process.returncode == 0
        output_file = self.output_dir / f"{self.video_info.path.stem}_converted.mp4"

        if success and temp_file.exists():
            shutil.move(temp_file, output_file)
        if temp_file.exists():
            temp_file.unlink()

        result = ConversionResult(
            success=success,
            input_file=self.video_info.path,
            output_file=output_file if success else None,
            command=cmd,
            log=None,
            duration_seconds=duration,
            error_message=None if success else "Conversion failed",
        )
        return result