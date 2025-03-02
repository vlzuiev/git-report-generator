import subprocess

from colorama import Fore

from print_utils import color_text


def get_user_commits(repository_path, author, from_year, until_year):
    result = subprocess.run(
        [
            "git",
            "log",
            "--author",
            author,
            "--pretty=format:%H %ad",
            "--date=format:%d-%m-%Y",
            "--since",
            f"01-01-{from_year}",
            "--until",
            f"31-12-{until_year}",
        ],
        capture_output=True,
        text=True,
        cwd=repository_path,
    )

    if result.stderr:
        print(color_text(result.stderr, Fore.RED))
        return

    commits = [commit for commit in result.stdout.strip().split("\n") if commit.strip()]

    return commits


def get_commit_diff(commit_hash, path):
    result = subprocess.run(
        ["git", "show", commit_hash],
        capture_output=True,
        text=True,
        cwd=path,
    )

    if result.stderr:
        print(color_text(result.stderr, Fore.RED))
        return

    return result.stdout
