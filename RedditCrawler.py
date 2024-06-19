import subprocess
import praw
import requests
import time
from datetime import datetime
import json
import os
import logging
from blessed import Terminal
from rich.console import Console
from rich.progress import Progress
from colorama import init, Fore
from plyer import notification
from collections import Counter

# Initialize colorama
init(autoreset=True)

import os
import logging
import subprocess

# Chemin du répertoire de journalisation
log_directory = os.path.expanduser('~/Documents/Codes/RedditCrawler/')
# Création du répertoire s'il n'existe pas
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Configuration de la journalisation après la création du répertoire
logging.basicConfig(filename=os.path.join(log_directory, 'reddit_crawler.log'), level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def install_required_modules():
    required_modules = ['praw', 'requests', 'rich', 'blessed', 'colorama', 'plyer']
    try:
        for module in required_modules:
            subprocess.check_call(['pip', 'install', module])
    except subprocess.CalledProcessError as e:
        logging.error(f"Error installing modules: {e}")

CONFIG_FILE_PATH = os.path.expanduser("~/Documents/Codes/RedditCrawler/config.json")
DESTINATION_FOLDER = os.path.expanduser("~/Documents/Codes/RedditCrawler/")
RESUME_FILE_PATH = os.path.join(DESTINATION_FOLDER, "resume.txt")
DOWNLOAD_REPORT_PATH = os.path.join(DESTINATION_FOLDER, "download_report.txt")


# File extensions and their corresponding content types
FILE_EXTENSIONS = {
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.png': 'image/png',
    '.gif': 'image/gif',
    '.mp4': 'video/mp4',
    '.txt': 'text/plain',
    '.csv': 'text/csv',
    '.html': 'text/html',
    '.xml': 'text/xml',
    '.json': 'application/json',
    '.zip': 'application/zip',
    '.tar': 'application/x-tar',
    '.gz': 'application/gzip',
    '.mp3': 'audio/mpeg',
    '.wav': 'audio/wav',
    '.ogg': 'audio/ogg'
}

class ConfigManager:
    @staticmethod
    def create_config_file():
        try:
            client_id = input(Fore.LIGHTBLUE_EX + "Enter client ID: " + Fore.RESET)
            client_secret = input(Fore.LIGHTBLUE_EX + "Enter client secret: " + Fore.RESET)
            user_agent = input(Fore.LIGHTBLUE_EX + "Enter user agent: " + Fore.RESET)

            data = {
                "client_id": client_id,
                "client_secret": client_secret,
                "user_agent": user_agent
            }

            with open(CONFIG_FILE_PATH, 'w') as file:
                json.dump(data, file)
        except IOError as e:
            logging.error(f"Error creating config file: {e}")
            return False

        return True

    @staticmethod
    def load_config():
        try:
            with open(CONFIG_FILE_PATH, 'r') as file:
                data = json.load(file)
                client_id = data["client_id"]
                client_secret = data["client_secret"]
                user_agent = data["user_agent"]
        except IOError as e:
            logging.error(f"Error loading config file: {e}")
            return None
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON config file: {e}")
            return None

        return client_id, client_secret, user_agent

class Downloader:
    @staticmethod
    def download_submission(submission, destination_folder):
        try:
            response = requests.get(submission.url)
            response.raise_for_status()
            file_extension = os.path.splitext(submission.url)[1]
            content_type = FILE_EXTENSIONS.get(file_extension.lower())
            if content_type is None:
                logging.error(f"Unsupported file extension: {file_extension}")
                return False
            file_name = f"{submission.id}{file_extension}"
            file_path = f"{destination_folder}/{file_name}"

            with open(file_path, 'wb') as file:
                file.write(response.content)

            return True
        except requests.exceptions.HTTPError as e:
            logging.error(f"Error downloading: {e}")
            return False
        except requests.exceptions.RequestException as e:
            logging.error(f"Error making HTTP request: {e}")
            return False

    @staticmethod
    def create_destination_folder(subreddit_name):
        destination_folder = f"{DESTINATION_FOLDER}/{subreddit_name}"
        if not os.path.exists(destination_folder):
            try:
                os.makedirs(destination_folder)
            except OSError as e:
                logging.error(f"Error creating destination folder: {e}")
                return None
        return destination_folder

    @staticmethod
    def download_content(subreddit_name=None, username=None):
        count = 0
        successful_downloads = 0
        failed_downloads = 0
        failure_reasons = []
        file_types = []

        # Check if the JSON file already exists
        if not os.path.exists(CONFIG_FILE_PATH):
            if not ConfigManager.create_config_file():
                return

        # Load information from the JSON file
        config = ConfigManager.load_config()
        if config is None:
            return
        client_id, client_secret, user_agent = config

        try:
            reddit = praw.Reddit(client_id=client_id,
                                 client_secret=client_secret,
                                 user_agent=user_agent)
        except praw.exceptions.PRAWException as e:
            logging.error(f"Error creating Reddit instance: {e}")
            return

        if subreddit_name:
            # Get the subreddit
            try:
                subreddit = reddit.subreddit(subreddit_name)
            except praw.exceptions.PRAWException as e:
                logging.error(f"Error getting subreddit: {e}")
                return

            # Convert the start date to a timestamp
            start_date = datetime(2020, 1, 1)
            start_time = int(start_date.timestamp())

            # Check and create the destination folder
            destination_folder = Downloader.create_destination_folder(subreddit_name)
            if destination_folder is None:
                return

            # Check if the resume file exists
            if os.path.exists(RESUME_FILE_PATH):
                try:
                    with open(RESUME_FILE_PATH, 'r') as file:
                        last_submission_id = file.read().strip()
                except IOError as e:
                    logging.error(f"Error reading resume file: {e}")
                    last_submission_id = None
            else:
                last_submission_id = None

            # Check if there was a previous interruption of the download
            if last_submission_id is not None:
                resume_option = input(Fore.LIGHTBLUE_EX + "The previous download was interrupted. Do you want to resume the download? (Yes/No) " + Fore.RESET)
                if resume_option.lower() == "yes":
                    resume_submission = None
                    for submission in subreddit.new(limit=None):
                        if submission.id == last_submission_id:
                            resume_submission = submission
                            break
                    if resume_submission is not None:
                        console.print("Resuming download...")
                        success = Downloader.download_submission(resume_submission, destination_folder)
                        if success:
                            successful_downloads += 1
                        else:
                            failed_downloads += 1
                            failure_reasons.append(f"Failed to resume download: {resume_submission.url}")
                        count += 1
                        console.print(f"Downloaded submissions: {count}")
                        # Update the ID of the last downloaded submission
                        try:
                            with open(RESUME_FILE_PATH, 'w') as file:
                                file.write(resume_submission.id)
                        except IOError as e:
                            logging.error(f"Error writing resume file: {e}")
                    else:
                        console.print("Unable to find the submission to resume the download.")
                else:
                    console.print("The previous download will not be resumed.")
            else:
                console.print("No previous download found.")

            # Iterate through the submissions in the subreddit from the start date until now
            total_submissions = 0
            for submission in subreddit.new(limit=None):
                submission_time = submission.created_utc
                if submission_time >= start_time:
                    if submission.url.endswith(tuple(FILE_EXTENSIONS.keys())):
                        if last_submission_id is not None and submission.id == last_submission_id:
                            # Ignore already downloaded submissions
                            continue
                        total_submissions += 1

            # Reset the counter for progress tracking
            count = 0

            # Amélioration du téléchargement des soumissions et affichage de la progression
            with Progress(console=console, auto_refresh=False) as progress:
                task = progress.add_task("[cyan]Téléchargement des soumissions...", total=total_submissions, completed=count, visible=False)
                for submission in subreddit.new(limit=None):
                    # Vérifie si la soumission est dans l'intervalle de temps désiré
                    if submission.created_utc < start_time:
                        continue

                    # Vérifie si l'URL de la soumission correspond à une extension de fichier prise en charge
                    if not submission.url.endswith(tuple(FILE_EXTENSIONS.keys())):
                        continue

                    # Ignore les soumissions déjà téléchargées
                    if last_submission_id is not None and submission.id == last_submission_id:
                        continue

                    # Télécharge la soumission et met à jour les compteurs de succès ou d'échec
                    success = Downloader.download_submission(submission, destination_folder)
                    if success:
                        successful_downloads += 1
                        file_extension = os.path.splitext(submission.url)[1]
                        file_types.append(file_extension)
                    else:
                        failed_downloads += 1
                        failure_reasons.append(f"Échec du téléchargement : {submission.url}")

                    # Met à jour la progression
                    count += 1
                    progress.update(task, completed=count)
                    remaining = total_submissions - count
                    console.print(f"Downloaded submissions: {count}/{total_submissions}")

                    # Met à jour l'ID de la dernière soumission téléchargée
                    with open(RESUME_FILE_PATH, 'w') as file:
                        file.write(submission.id)

            # Generate download report
            with open(DOWNLOAD_REPORT_PATH, 'w') as file:
                file.write(f"Download Report for subreddit: {subreddit_name}\n")
                file.write(f"Total Submissions: {total_submissions}\n")
                file.write(f"Successful Downloads: {successful_downloads}\n")
                file.write(f"Failed Downloads: {failed_downloads}\n")
                file.write("Failure Reasons:\n")
                for reason in failure_reasons:
                    file.write(f"- {reason}\n")
                file.write("\nFile Types:\n")
                for file_type, count in Counter(file_types).items():
                    file.write(f"- {file_type}: {count}\n")

            console.print("Download completed.")
            notification.notify(
                title="Download Completed",
                message=f"Download of subreddit '{subreddit_name}' completed successfully.",
                timeout=10
            )

        elif username:
            # Get the user
            try:
                user = reddit.redditor(username)
            except praw.exceptions.PRAWException as e:
                logging.error(f"Error getting user: {e}")
                return

            # Check and create the destination folder
            destination_folder = f"{DESTINATION_FOLDER}/{username}"
            if not os.path.exists(destination_folder):
                try:
                    os.makedirs(destination_folder)
                except OSError as e:
                    logging.error(f"Error creating destination folder: {e}")
                    return

            # Check if the resume file exists
            if os.path.exists(RESUME_FILE_PATH):
                try:
                    with open(RESUME_FILE_PATH, 'r') as file:
                        last_submission_id = file.read().strip()
                except IOError as e:
                    logging.error(f"Error reading resume file: {e}")
                    last_submission_id = None
            else:
                last_submission_id = None

            # Check if there was a previous interruption of the download
            if last_submission_id is not None:
                resume_option = input(Fore.LIGHTBLUE_EX + "The previous download was interrupted. Do you want to resume the download? (Yes/No) " + Fore.RESET)
                if resume_option.lower() == "yes":
                    resume_submission = None
                    for submission in user.submissions.new(limit=None):
                        if submission.id == last_submission_id:
                            resume_submission = submission
                            break
                    if resume_submission is not None:
                        console.print("Resuming download...")
                        success = Downloader.download_submission(resume_submission, destination_folder)
                        if success:
                            successful_downloads += 1
                            file_extension = os.path.splitext(resume_submission.url)[1]
                            file_types.append(file_extension)
                        else:
                            failed_downloads += 1
                            failure_reasons.append(f"Failed to resume download: {resume_submission.url}")
                        count += 1
                        console.print(f"Downloaded submissions: {count}")
                        # Update the ID of the last downloaded submission
                        try:
                            with open(RESUME_FILE_PATH, 'w') as file:
                                file.write(resume_submission.id)
                        except IOError as e:
                            logging.error(f"Error writing resume file: {e}")
                    else:
                        console.print("Unable to find the submission to resume the download.")
                else:
                    console.print("The previous download will not be resumed.")
            else:
                console.print("No previous download found.")

            # Download the user's submissions and display progress
            with Progress(console=console, auto_refresh=False) as progress:
                task = progress.add_task("[cyan]Downloading submissions...", total=None)
                for submission in user.submissions.new(limit=None):
                    if submission.url.endswith(tuple(FILE_EXTENSIONS.keys())):
                        if last_submission_id is not None and submission.id == last_submission_id:
                            # Ignore already downloaded submissions
                            continue
                        success = Downloader.download_submission(submission, destination_folder)
                        if success:
                            successful_downloads += 1
                            file_extension = os.path.splitext(submission.url)[1]
                            file_types.append(file_extension)
                        else:
                            failed_downloads += 1
                            failure_reasons.append(f"Failed to download: {submission.url}")
                        count += 1
                        progress.update(task, completed=count)
                        # Update the ID of the last downloaded submission
                        with open(RESUME_FILE_PATH, 'w') as file:
                            file.write(submission.id)

            # Generate download report
            with open(DOWNLOAD_REPORT_PATH, 'w') as file:
                file.write(f"Download Report for user: {username}\n")
                file.write(f"Total Submissions: {count}\n")
                file.write(f"Successful Downloads: {successful_downloads}\n")
                file.write(f"Failed Downloads: {failed_downloads}\n")
                file.write("Failure Reasons:\n")
                for reason in failure_reasons:
                    file.write(f"- {reason}\n")
                file.write("\nFile Types:\n")
                for file_type, count in Counter(file_types).items():
                    file.write(f"- {file_type}: {count}\n")
            console.print("Download completed.")
            notification.notify(
                title="Download Completed",
                message=f"Download of user '{username}' completed successfully.",
                timeout=10
            )

        else:
            console.print("Invalid option.")


def main():
    console = Console()
    option = input(Fore.LIGHTBLUE_EX + "Choose an option:\n1. Download a subreddit\n2. Download user content\n" + Fore.RESET)
    if option == "1":
        subreddit_name = input(Fore.LIGHTBLUE_EX + "Enter the subreddit name: " + Fore.RESET)
        Downloader.download_content(subreddit_name=subreddit_name)
    elif option == "2":
        username = input(Fore.LIGHTBLUE_EX + "Enter the username: " + Fore.RESET)
        Downloader.download_content(username=username)
    else:
        console.print("Invalid option.")

if __name__ == "__main__":
    install_required_modules()
    console = Console()
    main()
