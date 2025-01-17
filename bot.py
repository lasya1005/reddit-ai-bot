import os
import schedule
import time
import logging
from dotenv import load_dotenv
import praw
from groq import Groq
import random

# Load environment variables from .env file to keep sensitive data secure
load_dotenv()

# Reddit API credentials from the .env file
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")

# Groq API key to generate AI content
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Default subreddit and time for posting content
DEFAULT_SUBREDDIT = os.getenv("DEFAULT_SUBREDDIT", "test")
POST_TIME = os.getenv("POST_TIME", "10:00")

# Set up logging to track activity and errors
if not os.path.exists("logs"):
    os.makedirs("logs")
logging.basicConfig(
    filename="logs/bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Initialize Reddit API with credentials
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT,
    username=REDDIT_USERNAME,
    password=REDDIT_PASSWORD
)

# Initialize Groq API client to interact with the AI model
client = Groq(api_key=GROQ_API_KEY)

def generate_content(prompt="Write an engaging Reddit post about AI trends."):
    """Generate a new Reddit post using the Groq AI model."""
    try:
        # Using the Groq API to generate content based on the prompt
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",  
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        # In case something goes wrong, log the error and return a fallback message
        logging.error(f"Error generating content: {e}")
        return "Error generating content."

def generate_comment(prompt="Write a relevant comment on the latest AI post."):
    """Generate a comment for recent Reddit posts."""
    try:
        # Using Groq's API to generate a comment based on the prompt
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",  
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        # Handle errors by logging and returning a default message
        logging.error(f"Error generating comment: {e}")
        return "Error generating comment."

def post_to_reddit(subreddit_name, title, body):
    """Post the generated content to the given subreddit."""
    try:
        subreddit = reddit.subreddit(subreddit_name)
        subreddit.submit(title, selftext=body)
        logging.info(f"Successfully posted to {subreddit_name}: {title}")
    except Exception as e:
        # If posting fails, log the error
        logging.error(f"Error posting to Reddit: {e}")

def comment_on_posts(subreddit_name):
    """Comment on recent posts within the specified subreddit."""
    try:
        subreddit = reddit.subreddit(subreddit_name)
        # Fetch the latest 5 posts from the subreddit
        for post in subreddit.new(limit=5):
            # Generate a relevant comment based on the post's title
            comment = generate_comment(f"Comment on this post: {post.title}")
            post.reply(comment)
            logging.info(f"Successfully commented on post: {post.title}")
    except Exception as e:
        # Log any errors encountered during commenting
        logging.error(f"Error commenting on posts: {e}")

def daily_post():
    """Job to generate daily content and post it to Reddit."""
    content = generate_content()  # Generate the content
    post_to_reddit(DEFAULT_SUBREDDIT, "Daily AI Trends", content)  # Post the content

def daily_comment():
    """Job to comment on recent posts in Reddit daily."""
    comment_on_posts(DEFAULT_SUBREDDIT)  # Comment on the recent posts

# Schedule the jobs: one for posting content, another for commenting
schedule.every().day.at(POST_TIME).do(daily_post)
schedule.every().day.at("17:46").do(daily_comment)  # Time for commenting

# Main loop to keep the bot running and executing scheduled tasks
if __name__ == "__main__":
    logging.info("Starting Reddit bot...")  # Log when bot starts
    while True:
        # Run any pending scheduled jobs
        schedule.run_pending()
        # Sleep for a minute to keep the loop running
        time.sleep(60)
