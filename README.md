# Automated File Organizer

A Python script that monitors a directory and automatically sorts files into folders according to extension name.

## Features

-   **Real-time Monitoring:** Uses `watchdog` to instantly react to new files.
-   **Duplicate Handling:** Automatically renames files if a duplicate exists in the target folder.
-   **Error Resilient:** Includes retry logic for handling locked files and permission errors.
-   **Customizable:** Easily configure which file types go where by editing the `fileTypes` dictionary.

## How It Works

1. The script runs and begins monitoring a specified folder (e.g., the Downloads folder).
2. When a new file is detected, it checks its extension against a set of rules.
3. The file is then moved to the corresponding category folder (e.g., `.pdf` files go to `Document/`).
4. If a file with the same name already exists, the new file is renamed with a number (e.g., `(0) file.txt`).
5. All actions are logged to a `work.log` file for transparency.

## Installation & Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/Bao6879/automated-file-sorter.git
    ```

2.  **Install the required dependencies:**

    ```bash
    pip install watchdog
    ```

3.  **Run the script:**
    ```bash
    python sorter.py
    ```

## Project Structure

├── sorter.py # The main script
├── README.md # This file
└── config.json # Configuration file

## License

This project is licensed under the MIT License.
