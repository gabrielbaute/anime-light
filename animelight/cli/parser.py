import argparse

def create_parser() -> argparse.ArgumentParser:
    """
    Commands input configurations

    Returns:
        argparse.ArgumentParser: Parser object for argeparser cli.
    """
    parser = argparse.ArgumentParser(
        prog="anime-light",
        
        usage="Convert video files to lightweight mp4 using ffmpeg.",
        description="Anime Light Video Converter CLI.",
        epilog="Example: anime-light input.mkv -r 720p --crf 23 --preset slow --output-dir ./output",
        add_help=True,
        allow_abbrev=True,
        exit_on_error=True,)
    
    subparsers = parser.add_subparsers(dest="command", help="Commands available")

    # -------------------------------------------
    # Subcommand: version
    # -------------------------------------------
    subparsers.add_parser("version", help="Shows CLI version")

    # -------------------------------------------
    # Subcommand: help
    # -------------------------------------------
    subparsers.add_parser("help", help="Shows help")

    # -------------------------------------------
    # Subcommand: analyze
    # -------------------------------------------
    analyze_parser = subparsers.add_parser("analyze", help="Analyze a video file")
    analyze_parser.add_argument("file", type=str, help="Path to the video file to analyze")
    
    # -------------------------------------------
    # Subcommand: sysinfo
    # -------------------------------------------
    subparsers.add_parser("sysinfo", help="Shows system information and requirements")

    # -------------------------------------------
    # Subcommand: settings
    # -------------------------------------------
    subparsers.add_parser("settings", help="Shows actual Anime Light settings")

    # -------------------------------------------
    # Subcommand: convert
    # -------------------------------------------
    convert_parser = subparsers.add_parser("convert", help="Convert a video file")
    convert_parser.add_argument("input", type=str, help="Input file")
    convert_parser.add_argument("output", type=str, nargs="?", help="Output file (default: ./output/<filename>_converted.mp4)")
    convert_parser.add_argument("-r", "--resolution", type=int, choices=[360,480,720,1080], help="Video output resolution (360p, 480p, 720p, 1080p)")
    convert_parser.add_argument("-c", "--crf", type=int, choices=range(18,29), help="CRF (18-28), example: --crf 23")
    convert_parser.add_argument("-p", "--preset", type=str, choices=["ultrafast","fast","medium","slow"], help="Convert preset for ffmpeg, example: --preset slow")
    convert_parser.add_argument("-t", "--threads", type=int, help="Threads number to use, example: --threads 4")
    convert_parser.add_argument("-g", "--use-gpu", action="store_true", help="Use GPU acceleration if its available, example: --use-gpu intel")
    convert_parser.add_argument("--cool-mode", action="store_true", help="Forzar un único hilo")
    convert_parser.add_argument("-b", "--batch", "--recursive", action="store_true", help="Procesar subcarpetas o batch")

    # -------------------------------------------
    # Subcommand: init
    # -------------------------------------------
    init_parser = subparsers.add_parser("init", help="Initialize application settings")
    init_parser.add_argument("--host", type=str, default="127.0.0.1", help="API host (default: 127.0.0.1)")
    init_parser.add_argument("--port", type=int, default=8000, help="API port (default: 8000)")
    init_parser.add_argument("--level", type=str, default="INFO", help="Log level (default: INFO)")
    init_parser.add_argument("--env", action="store_true", help="Optional: write .env if requested")

    # -------------------------------------------
    # Subcomando: clean
    # -------------------------------------------
    clean_parser = subparsers.add_parser("clean", help="Clean the app directories")
    clean_parser.add_argument("--all", action="store_true", help="Clean all directories")
    clean_parser.add_argument("--temp", action="store_true", help="Clean temp directory")
    clean_parser.add_argument("--output", action="store_true", help="Clean output directory")
    clean_parser.add_argument("--logs", action="store_true", help="Clean logs directory")
    clean_parser.add_argument("--uploads", action="store_true", help="Clean uploads directory")
    clean_parser.add_argument("--settings", action="store_true", help="Remove the .env and .yaml files with the app settings")

    return parser