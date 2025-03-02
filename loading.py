import sys
import threading
import time
from colorama import Fore


def progress_bar():
    while True:
        for i in range(0, 101, 5):
            yield f"[{Fore.CYAN}{'#' * (i // 5)}{'.' * (20 - i // 5)}] {i}%"
        for i in range(100, -1, -5):
            yield f"[{Fore.CYAN}{'#' * (i // 5)}{'.' * (20 - i // 5)}] {i}%"


def loading_indicator():
    bar = progress_bar()
    message = "Loading"
    spinner = ["|", "/", "-", "\\", "|", "/", "-", "\\"]
    spinner_index = 0
    start_time = time.time()
    while not loading:
        elapsed_time = time.time() - start_time
        sys.stdout.write(
            f"\r{next(bar)} {Fore.CYAN}{spinner[spinner_index]} {message} (Elapsed: {elapsed_time:.1f}s)"
        )
        spinner_index = (spinner_index + 1) % len(spinner)
        sys.stdout.flush()
        time.sleep(0.2)
    sys.stdout.write("\r" + " " * 80 + "\r")


def start_loading():
    global loading
    loading = False

    global loading_thread

    loading_thread = threading.Thread(target=loading_indicator)
    loading_thread.start()


def stop_loading():
    global loading
    loading = True
    loading_thread.join()
