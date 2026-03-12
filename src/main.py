import argparse
import importlib


def main() -> None:
    parser = argparse.ArgumentParser(description="ScrapeCraft - Web scraper multi-job")
    parser.add_argument(
        "--job",
        required=True,
        metavar="JOB",
        help="Job a ejecutar (ej: viviendas_adonde)"
    )
    parser.add_argument(
        "--reprocess",
        metavar="SUFFIX",
        help="Reprocesar raw existente indicando su sufijo (ej: 20260312_143052)"
    )
    args = parser.parse_args()

    try:
        job_module = importlib.import_module(f"src.{args.job}.app_job")
    except ModuleNotFoundError:
        print(f"Error: job '{args.job}' no encontrado. Verifica que existe src/{args.job}/app_job.py")
        raise SystemExit(1)

    job_module.run(args)


if __name__ == "__main__":
    main()
