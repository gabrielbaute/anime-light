import sys
from pathlib import Path
from animelight.cli.parser import create_parser
from animelight.cli.commands import show_version, analyze_video, show_sysinfo, run_convert, CommandHelp


def main() -> None:
    parser = create_parser()
    
    if "--help" in sys.argv or "-h" in sys.argv:
        if len(sys.argv) > 1 and sys.argv[1] in ["convert", "analyze", "sysinfo", "version", "help"]:
            CommandHelp().print_command_help(sys.argv[1])
        else:
            CommandHelp().print_help()
        sys.exit(0)

    args = parser.parse_args()

    if args.command == "version":
        show_version()

    elif args.command == "analyze":
        analyze_video(Path(args.file))

    elif args.command == "sysinfo":
        show_sysinfo()

    elif args.command == "convert":
        run_convert(args)
    
    elif args.command == "help":
            CommandHelp().print_help()

    elif args.command is None:
        CommandHelp().print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
