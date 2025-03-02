# git-report-generator

This project is a script to generate reports from Git repositories. It processes commits and generates a summary report for a specified author and time period.

## Prerequisites

- Python 3.11 or higher
- Homebrew (for installing dependencies)

## Installation

1. Install **Homebrew** (if not already installed):

```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

1. Install UV

```sh
brew install uv
```

3. Create a `.env` file:

Copy the sample `.env.sample` file to `.env` and fill in the required values:

```sh
cp .env.sample .env
```

## Usage

Run `uv run python main.py`
