from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
OUTPUTS = ROOT / "outputs"
OUTPUTS.mkdir(exist_ok=True)


def run(args: list[str]) -> None:
    print("\n> " + " ".join(args))
    subprocess.run([sys.executable, "main.py", *args], cwd=ROOT, check=False)


def menu() -> str:
    print("\nBANG IT UP MUSIC — YouTube AI Agent")
    print("1. Σύνδεση / έλεγχος YouTube")
    print("2. Δες στοιχεία καναλιού")
    print("3. Δες πρόσφατα βίντεο")
    print("4. Φτιάξε full growth report")
    print("5. Φτιάξε campaign για νέο τραγούδι")
    print("6. Analytics recommendations")
    print("0. Έξοδος")
    return input("\nΔιάλεξε αριθμό: ").strip()


def campaign() -> None:
    title = input("Τίτλος τραγουδιού/video: ").strip() or "New Music Release"
    genre = input("Genre π.χ. trap, drill, afrobeat, dance: ").strip() or "music"
    mood = input("Mood π.χ. high energy, dark, emotional: ").strip() or "high energy"
    audience = input("Κοινό π.χ. DJs, Greek rap fans, club listeners: ").strip() or "music listeners, DJs, creators"
    run(["campaign", "--title", title, "--genre", genre, "--mood", mood, "--audience", audience])
    print(f"\nΤο campaign σώθηκε στον φάκελο: {OUTPUTS}")


def main() -> None:
    while True:
        choice = menu()
        if choice == "1":
            run(["setup"])
        elif choice == "2":
            run(["channel"])
        elif choice == "3":
            run(["videos", "--max", "10"])
        elif choice == "4":
            run(["report", "--days", "28"])
            print(f"\nΆνοιξε το αρχείο: {OUTPUTS / 'growth_report.md'}")
        elif choice == "5":
            campaign()
        elif choice == "6":
            run(["analytics", "--days", "28"])
        elif choice == "0":
            print("Τέλος.")
            break
        else:
            print("Λάθος επιλογή.")


if __name__ == "__main__":
    main()
