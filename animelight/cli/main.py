import sys
from pathlib import Path
from rich.console import Console

from animelight.settings.log_settings import AnimeLightLogger
from animelight.cli.parser import create_parser
from animelight.cli.commands import (
    show_version, 
    analyze_video, 
    show_sysinfo, 
    run_convert, 
    init_settings, 
    show_settings,
    clean_directories, 
    commands,
    CommandHelp
    )


def main() -> None:
    settings_logger = AnimeLightLogger()
    settings_logger.setup()
    parser = create_parser()
    console = Console()
    help = CommandHelp(console=console)
    
    if "--help" in sys.argv or "-h" in sys.argv:
        if len(sys.argv) > 1 and sys.argv[1] in commands:
            help.print_command_help(sys.argv[1])
        else:
            help.print_help()
        sys.exit(0)

    args = parser.parse_args()

    if args.command == "version":
        show_version(console=console)

    elif args.command == "analyze":
        analyze_video(Path(args.file), console=console)

    elif args.command == "sysinfo":
        show_sysinfo(console=console)

    elif args.command == "convert":
        run_convert(args, console=console)

    elif args.command == "init":
        init_settings(args, console=console)
    
    elif args.command == "settings":
        show_settings(console=console)
    
    elif args.command == "clean":
        clean_directories(args, console=console)

    elif args.command == "help":
        help.print_help()

    elif args.command is None:
        help.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
