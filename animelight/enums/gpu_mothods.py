from enum import StrEnum

class GPUMethods(StrEnum):
    NVIDIA = "cuda"
    INTEL = "qsv"
    LINUX_AMD = "vaapi"

    def __str__(self):
        return self.value
