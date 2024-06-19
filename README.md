```markdown
# RedditCrawler

RedditCrawler is a Python script designed to download content from Reddit, either from specific subreddits or user profiles. It supports downloading various types of media and generates a report upon completion.

## Features

- Download content by subreddit name or username.
- Supports multiple file types including images, videos, and text.
- Generates a download report detailing the types of files downloaded.
- Customizable destination folder for downloads.
- Logging of errors and important events.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed on your system.
- `praw`, `requests`, `colorama`, `rich`, and `plyer` libraries installed. You can install these using `pip`.

## Installation

Clone the repository to your local machine:

```sh
git clone https://github.com/MrFlappy0/RedditCrawler.git
```

Navigate into the project directory:

```sh
cd RedditCrawler
```



## Usage

To start the script, run:

```sh
python RedditCrawler.py
```

Follow the on-screen prompts to choose between downloading subreddit content or user content, and then enter the respective subreddit name or username.

## Configuration

- **Logging Directory**: The default logging directory is set to `~/Documents/Codes/RedditCrawler/`. This can be changed in the `RedditCrawler.py` file.
- **Download Destination**: The default download destination is `~/Documents/Codes/RedditCrawler/`. This can be modified in the `RedditCrawler.py` file.

## Contributing

Contributions are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
