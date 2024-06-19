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

MIT License

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

