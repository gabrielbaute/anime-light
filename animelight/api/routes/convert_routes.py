from fastapi import APIRouter, UploadFile, File, HTTPException, Form, Request
from fastapi.responses import FileResponse

from animelight.settings import Settings
from animelight.models import ConversionResponse, ConversionResult, VideoFileInfo
from animelight.services import VideoAnalyzerService, VideoConverterService, ConversionArgsParser
from animelight.enums import GPUMethods

router = APIRouter(prefix="/convert", tags=["Conversion"])

settings = Settings()

@router.post("", summary="Upload and convert a video file", response_model=ConversionResponse)
async def convert_video(
    file: UploadFile = File(...),
    resolution: int = Form(720),
    preset: str = Form("slow"),
    crf: int = Form(23),
    threads: int = Form(1),
    gpu: str = Form(None),
    audio_bitrate: int = Form(128),
    audio_codec: str = Form("aac"),
    video_codec: str = Form("h264"),
    request: Request = None
):
    logger = request.app.state.logger
    try:
        if logger:
            logger.info(f"Received file {file.filename} for conversion")

        # Guardar archivo
        upload_path = settings.app_settings.uploads_dir / file.filename
        with open(upload_path, "wb") as f:
            f.write(await file.read())

        # Analizar
        analyzer = VideoAnalyzerService(upload_path, logger=logger)
        video_info = analyzer.analyze()
        if not video_info:
            raise HTTPException(status_code=400, detail="Could not analyze video file")

        # Mapear enums
        scale = ConversionArgsParser.parse_resolution(resolution)
        if scale is None:
            raise HTTPException(status_code=400, detail=f"Invalid resolution {resolution}")
        
        try:
            preset_enum = ConversionArgsParser.parse_ffmpeg_preset(preset)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid preset {preset}")
        
        gpu_method_enum = None
        if gpu:
            try:
                gpu_method_enum = ConversionArgsParser.parse_gpu_method(gpu.lower())
            except Exception:
                raise HTTPException(status_code=400, detail=f"Invalid GPU method: {gpu}")

        audio_bitrate_enum = ConversionArgsParser.parse_audio_bitrate(audio_bitrate)
        if audio_bitrate_enum is None:
            raise HTTPException(status_code=400, detail=f"Invalid audio bitrate: {audio_bitrate}")

        try:
            audio_codec_enum = ConversionArgsParser.parse_audio_codec(audio_codec)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid audio codec: {audio_codec}")

        try:
            video_codec_enum = ConversionArgsParser.parse_video_codec(video_codec)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid video codec: {video_codec}")
        
        # Convertir
        service = VideoConverterService(video_info, output_dir=settings.app_settings.output_dir, settings=settings, logger=logger)
        result = service.convert(
            crf=crf,
            preset=preset_enum,
            scale=scale,
            threads=threads,
            video_codec=video_codec_enum,
            audio_codec=audio_codec_enum,
            audio_bitrate=audio_bitrate_enum,
            gpu_method=gpu_method_enum
        )

        if not result.success:
            return ConversionResponse(
                success=False,
                error_message=result.error_message,
                command=result.command
            )

        video_output_info = VideoAnalyzerService(result.output_file, logger=logger).analyze()
        efficiency = video_output_info.size_bytes / video_info.size_bytes * 100 if video_info.size_bytes else None
        
        return ConversionResponse(
            success=True,
            filename=result.output_file.name,
            video_input_info=video_info,
            video_output_info=video_output_info,
            convert_result=result,
            efficiency=efficiency,
            download_url=f"{request.base_url}api/v1/convert/download/{result.output_file.name}"
        )

    except HTTPException:
        # Re-lanzamos excepciones de validación para que FastAPI responda correctamente
        raise
    except Exception as e:
        if logger:
            logger.exception(f"Unhandled error in convert endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/download/{filename}", summary="Download converted video")
async def download_file(filename: str):
    file_path = settings.app_settings.output_dir / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, media_type="video/mp4", filename=filename)