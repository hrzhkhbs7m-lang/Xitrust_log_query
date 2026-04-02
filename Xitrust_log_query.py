import sys
from pathlib import Path


def load_exceptions(exception_file: Path):
    """
    Lädt alle Ausnahme-Strings aus einer Datei
    (eine Ausnahme pro Zeile)
    """
    exceptions = set()

    if not exception_file.exists():
        print(f"[WARN] Ausnahme-Datei nicht gefunden: {exception_file}")
        return exceptions

    with exception_file.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if line:
                exceptions.add(line)

    return exceptions


def process_log(log_path: Path, exceptions, result_file: Path):
    """
    Liest Logfile und schreibt gültige ERROR-Zeilen in result_file
    """
    found_errors = []

    with log_path.open("r", encoding="utf-8", errors="ignore") as logfile:
        for line in logfile:
            if "ERROR" in line:
                if not any(exc in line for exc in exceptions):
                    found_errors.append(line.rstrip())

    # Zielordner automatisch erstellen
    result_file.parent.mkdir(parents=True, exist_ok=True)

    with result_file.open("w", encoding="utf-8") as out:
        for entry in found_errors:
            out.write(entry + "\n")

    print(f"[INFO] {len(found_errors)} ERROR-Einträge gespeichert in {result_file}")


def main():
    if len(sys.argv) < 4:
        print(
            "Usage: python LogFile_query.py "
            "<logfile_path> <result_path> <exception_path>"
        )
        sys.exit(1)

    log_path = Path(sys.argv[1])
    result_file = Path(sys.argv[2])
    exception_file = Path(sys.argv[3])

    if not log_path.exists():
        print(f"[ERROR] Logfile nicht gefunden: {log_path}")
        sys.exit(1)

    if not exception_file.exists():
        print(f"[ERROR] Ausnahme-Datei nicht gefunden: {exception_file}")
        sys.exit(1)

    exceptions = load_exceptions(exception_file)
    process_log(log_path, exceptions, result_file)


if __name__ == "__main__":
    main()