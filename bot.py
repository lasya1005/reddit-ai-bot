import os
import schedule
import time
import logging
from dotenv import load_dotenv
import praw
from groq import Groq  

# Load environment variables from .env file
load_dotenv()

# Reddit API credentials
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")

# Groq API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Default subreddit and post time
DEFAULT_SUBREDDIT = os.getenv("DEFAULT_SUBREDDIT", "test")
POST_TIME = os.getenv("POST_TIME", "10:00")

# Logging setup
if not os.path.exists("logs"):
    os.makedirs("logs")
logging.basicConfig(
    filename="logs/bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Initialize Reddit API
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT,
    username=REDDIT_USERNAME,
    password=REDDIT_PASSWORD
)

# Initialize Groq API client
client = Groq(api_key=GROQ_API_KEY)

def generate_content(prompt="Write an engaging Reddit post about AI trends."):
    """Generate content using Groq API."""
    try:
        # Generate content using Groq's chat API
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",  
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        logging.error(f"Error generating content: {e}")
        return "Error generating content."

def post_to_reddit(subreddit_name, title, body):
    """Post content to Reddit."""
    try:
        subreddit = reddit.subreddit(subreddit_name)
        subreddit.submit(title, selftext=body)
        logging.info(f"Successfully posted to {subreddit_name}: {title}")
    except Exception as e:
        logging.error(f"Error posting to Reddit: {e}")

def daily_post():
    """Job to generate content and post to Reddit daily."""
    content = generate_content()
    post_to_reddit(DEFAULT_SUBREDDIT, "Daily AI Trends", content)

# Schedule the job
schedule.every().day.at(POST_TIME).do(daily_post)

# Run the scheduler
if __name__ == "__main__":
    logging.info("Starting Reddit bot...")
    while True:
        schedule.run_pending()
        time.sleep(60)
