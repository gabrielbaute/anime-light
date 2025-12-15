import subprocess
import platform
import psutil
from animelight.models import SystemInfo, GPUInfo

class SystemInspectorService:
    def __init__(self):
        pass

    def _check_ffmpeg(self):
        try:
            result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
            if result.returncode == 0:
                version_line = result.stdout.splitlines()[0]
                return True, version_line
        except FileNotFoundError:
            return False, None
        return False, None

    def _check_gpu(self):
        gpus = []
        try:
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=name,driver_version", "--format=csv,noheader"],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                for line in result.stdout.strip().splitlines():
                    name, driver = line.split(",")
                    gpus.append(GPUInfo(name=name.strip(), driver_version=driver.strip()))
        except FileNotFoundError:
            # No NVIDIA GPU
            pass
        return gpus

    def analyze(self) -> SystemInfo:
        os_name = platform.system()
        os_version = platform.version()
        cpu_threads = psutil.cpu_count(logical=True)
        cpu_cores = psutil.cpu_count(logical=False)

        ffmpeg_available, ffmpeg_version = self._check_ffmpeg()
        gpus = self._check_gpu()

        return SystemInfo(
            os_name=os_name,
            os_version=os_version,
            cpu_cores=cpu_cores,
            cpu_threads=cpu_threads,
            gpus=gpus,
            ffmpeg_available=ffmpeg_available,
            ffmpeg_version=ffmpeg_version
        )
