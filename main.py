import os
import calendar
from datetime import datetime
from git_utils import get_commit_diff, get_user_commits
from loading import start_loading, stop_loading
from os_utils import (
    remove_folder,
    create_folder,
    create_file,
    create_folder_if_not_exists,
)
from print_utils import (
    clear_text_from_ansi,
    color_text,
    print_with_blank_line_in_front,
    text_percentage,
)
from dotenv import load_dotenv
from io import StringIO
import sys
from colorama import Fore


load_dotenv()

BASE_REPOSITORIES_FOLDER = os.getenv("BASE_REPOSITORIES_FOLDER")
FROM_YEAR = os.getenv("FROM_YEAR")
UNIT_YEAR = os.getenv("UNIT_YEAR")
AUTHOR = os.getenv("AUTHOR")

REPORT_BASE_FOLDER = "reports"


def create_folder_structure(repository_name, date):
    day, month, year = date.split("-")
    month_name = calendar.month_name[int(month)]
    year_folder = f"{REPORT_BASE_FOLDER}/{year}"
    create_folder_if_not_exists(year_folder)
    month_folder = f"{REPORT_BASE_FOLDER}/{year}/{month_name}"
    create_folder_if_not_exists(month_folder)
    day_folder = f"{REPORT_BASE_FOLDER}/{year}/{month_name}/{day}"
    create_folder_if_not_exists(day_folder)
    report_repository_folder = (
        f"{REPORT_BASE_FOLDER}/{year}/{month_name}/{day}/{repository_name}"
    )
    create_folder_if_not_exists(report_repository_folder)

    return report_repository_folder


def get_working_days(year, month):
    _, num_days = calendar.monthrange(year, month)

    working_days = sum(
        [
            1
            for day in range(1, num_days + 1)
            if datetime(year, month, day).weekday() < 5
        ]
    )

    return working_days


def write_commit_to_file(commit, repository_path, repository_name):
    commit_hash, date = commit.split(" ", 1)

    commit_file_base_path = create_folder_structure(repository_name, date)

    commit_file_name = f"{commit_hash}.txt"
    create_file(commit_file_name, commit_file_base_path)

    diff = get_commit_diff(commit_hash, repository_path)
    if diff:
        with open(f"{commit_file_base_path}/{commit_file_name}", "w") as file:
            file.write(diff)


def create_repository_report(repository_path):
    repository_name = repository_path.split("/")[-1]
    print(color_text(f"Processing repository: {repository_name}", Fore.YELLOW))

    commits = get_user_commits(
        repository_path, author=AUTHOR, from_year=FROM_YEAR, until_year=UNIT_YEAR
    )
    if commits is None or len(commits) == 0:
        return

    print(color_text(f"Found: {len(commits)} commits", Fore.GREEN))

    start_loading()
    for commit in commits:
        write_commit_to_file(commit, repository_path, repository_name)
    stop_loading()


def calculate_completed_days(month, year):
    completed_days = len(os.listdir(f"{REPORT_BASE_FOLDER}/{year}/{month}"))

    return completed_days


def calculate_average_completed_days(month, year):
    month_number = list(calendar.month_name).index(month)
    total_working_days = get_working_days(int(year), month_number)

    completed_days = calculate_completed_days(month, year)
    completion_percentage = (completed_days / total_working_days) * 100

    return completion_percentage


def month_summary(month, year):
    month_number = list(calendar.month_name).index(month)
    total_working_days = get_working_days(int(year), month_number)
    completed_days = calculate_completed_days(month, year)
    completion_percentage = calculate_average_completed_days(month, year)

    return f"{color_text(month, Fore.BLUE)}: \n - Total working days in a month: {total_working_days}\n - Number of days with pushed commits: {completed_days} {text_percentage(completion_percentage)}"


def prepare_summary(year):
    average_completed_days = [
        calculate_average_completed_days(month, year)
        for month in os.listdir(f"{REPORT_BASE_FOLDER}/{year}")
    ]
    overall_average = (
        sum(average_completed_days) / len(average_completed_days)
        if average_completed_days
        else 0
    )
    months_text = [
        month_summary(month, year)
        for month in os.listdir(f"{REPORT_BASE_FOLDER}/{year}")
    ]

    print_with_blank_line_in_front(
        color_text(f"--- Summary Report for {year} ---", Fore.BLUE)
    )
    print_with_blank_line_in_front("\n".join(months_text))
    print_with_blank_line_in_front(
        color_text(
            f"Total average completed days: {text_percentage(overall_average)}",
            Fore.BLUE,
        )
    )
    print_with_blank_line_in_front(
        color_text(f"--- End of Summary Report for {year} ---", Fore.BLUE)
    )
    disclaimer_text()


def disclaimer_text():
    print_with_blank_line_in_front(
        color_text(
            "Disclaimer: Bank holidays are not included into calculation of working days",
            Fore.RED,
        )
    )


def store_summary_text(year):
    sys.stdout = StringIO()

    prepare_summary(year)

    summary_text = clear_text_from_ansi(sys.stdout.getvalue())

    summary_file_path = f"{REPORT_BASE_FOLDER}/{year}/summary.txt"
    create_file("summary.txt", f"{REPORT_BASE_FOLDER}/{year}")
    with open(summary_file_path, "w") as summary_file:
        summary_file.write(summary_text)

    sys.stdout = sys.__stdout__


def main():
    try:
        print("Welcome to the Report Generator")
        print(
            color_text(
                f"Running report for {AUTHOR} from {FROM_YEAR} until {UNIT_YEAR} year \n",
                Fore.BLUE,
            )
        )

        remove_folder(REPORT_BASE_FOLDER)
        create_folder(REPORT_BASE_FOLDER)

        for repository_name in os.listdir(BASE_REPOSITORIES_FOLDER):
            repository_path = os.path.join(BASE_REPOSITORIES_FOLDER, repository_name)
            if os.path.isdir(repository_path):
                create_repository_report(repository_path)

        for year in range(int(FROM_YEAR), int(UNIT_YEAR) + 1):
            prepare_summary(year)
            store_summary_text(year)

        stop_loading()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
