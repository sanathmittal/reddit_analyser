import praw
import datetime
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

# Reddit API Setup
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
)

# OpenAI API Key
openai_api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1, openai_api_key=openai_api_key)

# Function to fetch trending meme data
def fetch_meme_trends():
    meme_subreddits = ["memes", "dankmemes", "funny", "AdviceAnimals", "MemeEconomy"]
    categories = ["hot", "rising", "top"]

    all_posts = []
    trending_subreddits = {}
    top_users = {}

    for subreddit_name in meme_subreddits:
        subreddit = reddit.subreddit(subreddit_name)

        for category in categories:
            posts = getattr(subreddit, category)(limit=30)

            for post in posts:
                post_data = {
                    "title": post.title,
                    "score": post.score,
                    "num_comments": post.num_comments,
                    "upvote_ratio": post.upvote_ratio,
                    "awards": post.total_awards_received,
                    "comment_velocity": post.num_comments / max((datetime.datetime.utcnow() - datetime.datetime.utcfromtimestamp(post.created_utc)).total_seconds(), 1),
                    "gilded": post.gilded,
                    "stickied": post.stickied,
                    "is_video": post.is_video,
                    "over_18": post.over_18,
                    "self_text": post.selftext,
                    "flair": post.link_flair_text,
                    "subreddit": subreddit_name,
                    "author": str(post.author),
                    "created_utc": post.created_utc
                }

                all_posts.append(post_data)

                # Track trending subreddits
                if subreddit_name not in trending_subreddits:
                    trending_subreddits[subreddit_name] = {"total_posts": 0, "total_upvotes": 0}

                trending_subreddits[subreddit_name]["total_posts"] += 1
                trending_subreddits[subreddit_name]["total_upvotes"] += post.score

                # Track top users
                if post.author:
                    username = str(post.author)
                    if username not in top_users:
                        top_users[username] = {"total_posts": 0, "total_upvotes": 0}

                    top_users[username]["total_posts"] += 1
                    top_users[username]["total_upvotes"] += post.score

    return {
        "trending_posts": all_posts,
        "trending_subreddits": trending_subreddits,
        "top_users": top_users,
    }

# Function to analyze trends with GPT
def analyze_meme_trends():
    meme_data = fetch_meme_trends()

    # Format posts into a structured string
    formatted_posts = "\n\n".join(
        [
            f"Title: {post['title']}\n"
            f"Subreddit: {post['subreddit']}\n"
            f"Author: {post['author']}\n"
            f"Score: {post['score']}\n"
            f"Num Comments: {post['num_comments']}\n"
            f"Upvote Ratio: {post['upvote_ratio']}\n"
            f"Awards: {post['awards']}\n"
            f"Comment Velocity: {post['comment_velocity']:.2f} comments/sec\n"
            f"Gilded: {post['gilded']}\n"
            f"Stickied: {post['stickied']}\n"
            f"Is Video: {post['is_video']}\n"
            f"Over 18: {post['over_18']}\n"
            f"Flair: {post['flair']}\n"
            f"Self Text: {post['self_text'][:500]}..."  # Limit self-text for brevity
            for post in meme_data["trending_posts"]
        ]
    )

    formatted_subreddits = "\n".join(
        [f"- {sub} (Posts: {data['total_posts']}, Upvotes: {data['total_upvotes']})" for sub, data in meme_data["trending_subreddits"].items()]
    )

    formatted_users = "\n".join(
        [f"- {user} (Posts: {data['total_posts']}, Upvotes: {data['total_upvotes']})" for user, data in meme_data["top_users"].items()]
    )

    # LangChain PromptTemplate
    prompt_template = PromptTemplate(
        input_variables=["num_posts", "post_data", "trending_subreddits", "top_users"],
        template="""
        Analyze the following trending memes on Reddit:

        **Number of Trending Memes Analyzed:** {num_posts}

        **Full Post Data (Including Metadata):**
        {post_data}

        **Trending Meme Subreddits:**
        {trending_subreddits}

        **Top Meme Creators:**
        {top_users}

        **Questions to Answer:**
        - What meme formats/styles are gaining popularity?
        - Which subreddits are growing in meme engagement?
        - Who are the top meme creators?
        - Predict upcoming meme trends.
        """
    )

    # Generate final prompt
    final_prompt = prompt_template.format(
        num_posts=len(meme_data["trending_posts"]),
        post_data=formatted_posts,
        trending_subreddits=formatted_subreddits,
        top_users=formatted_users
    )

    # Send to LLM
    response = llm.invoke(final_prompt)
    
    return response.content
