# Reddit AI Bot

## Description
This bot uses the Groq API to generate AI-related content and posts it automatically to Reddit at a scheduled time each day. The bot posts to a specific subreddit, comments on recent posts, and logs any errors that occur during the process.

## Setup Instructions
1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/lasya1005/reddit-ai-bot.git
   cd reddit-ai-bot
   ```
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```
3. Create a .env file in the root directory and add the following environment variables:
```bash
REDDIT_CLIENT_ID=<your-reddit-client-id>
REDDIT_CLIENT_SECRET=<your-reddit-client-secret>
REDDIT_USER_AGENT=<your-reddit-user-agent>
REDDIT_USERNAME=<your-reddit-username>
REDDIT_PASSWORD=<your-reddit-password>
GROQ_API_KEY=<your-groq-api-key>
DEFAULT_SUBREDDIT=<subreddit-name>
POST_TIME=<time-for-daily-posts>
```
4. Run the bot:
```bash
python bot.py
```
## Libraries
- praw: Python Reddit API Wrapper
- requests: HTTP library to make requests to the Groq API
- groq: Python client to interact with the Groq API
- schedule: A simple job scheduling library

## Usage
The bot will automatically:

- Post AI-related content to the specified subreddit at the time specified in the .env file.
- Comment on recent posts in the subreddit, providing relevant comments.
- Errors and logs will be recorded in the logs directory.

## License
This project is licensed under the MIT License.

