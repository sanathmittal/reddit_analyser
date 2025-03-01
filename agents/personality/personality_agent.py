import praw
import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
import urllib.parse
import aiohttp
import asyncpraw

from langchain.chat_models import ChatOpenAI

from utils.clean_reddit_data import clean_reddit_data 
from utils.clean_gpt import clean_gpt_response

# Load environment variables
import asyncpraw
import os
from dotenv import load_dotenv

load_dotenv()


async def get_reddit_client(access_token: str = None, refresh_token: str = None):
    """
    Initialize async Reddit client using access token (or refresh token if access token is expired).
    """
    try:
        auth_kwargs = {
            "client_id": os.getenv("REDDIT_CLIENT_ID"),
            "client_secret": os.getenv("REDDIT_CLIENT_SECRET"),
            "user_agent": os.getenv("REDDIT_USER_AGENT"),
        }
        
        # Add the appropriate token
        if access_token:
            auth_kwargs["access_token"] = access_token
        if refresh_token:
            auth_kwargs["refresh_token"] = refresh_token
            
        reddit = asyncpraw.Reddit(**auth_kwargs)
        
        # Verify authentication
        me = await reddit.user.me()
        if me is None:
            raise ValueError("Authentication failed - could not get user info")
        print(f"Successfully authenticated as: {me.name}")
        
        return reddit
    except Exception as e:
        print(f"Error initializing Reddit client: {str(e)}")
        raise

async def fetch_user_data(username: str, access_token: str, refresh_token: str = None):
    """
    Fetch Reddit user data including subscribed subreddits and other user info
    """
    print("Starting fetch_user_data function")
    
    try:
        reddit = await get_reddit_client(access_token, refresh_token)
        print("Reddit client initialized successfully")
        
        # Initialize data structure
        user_data = {
            "user_info": {},
            "posts": [],
            "comments": [],
            "upvoted_posts": [],
            "subreddits": []
        }
        print("Data structure initialized with:", list(user_data.keys()))

        # Handle 'me' user case and fetch subscribed subreddits
        if username.lower() == "me":
            print("Fetching data for authenticated user 'me'")
            user = await reddit.user.me()
            if user is None:
                raise ValueError("Failed to fetch the logged-in user")
            username = user.name
            print(f"Authenticated username: {username}")
            
            # Fetch subscribed subreddits using subscriptions() instead of subreddits()
            try:
                print("Starting to fetch subscribed subreddits")
                subreddit_count = 0
                # Get the authenticated user's subscriptions
                async for subreddit in reddit.user.me().subscriptions():
                    subreddit_data = {
                        "display_name": subreddit.display_name,
                        "name": subreddit.name,
                        "title": subreddit.title,
                        "description": subreddit.description,
                        "created_utc": subreddit.created_utc,
                        "over_18": subreddit.over18,
                        "subscribers": subreddit.subscribers
                    }
                    user_data["subreddits"].append(subreddit_data)
                    subreddit_count += 1
                print(f"Fetched {subreddit_count} subscribed subreddits")
            except Exception as e:
                print(f"Error fetching subscribed subreddits: {str(e)}")
        
        # Rest of your existing code for fetching user info, posts, comments, etc.
        print(f"Initializing redditor object for {username}")
        user = await reddit.redditor(username)
        
        # Fetch user info
        try:
            await user.load()
            user_data["user_info"] = {
                "name": user.name,
                "created_utc": user.created_utc,
                "link_karma": user.link_karma,
                "comment_karma": user.comment_karma,
                "total_karma": user.total_karma,
                "is_employee": user.is_employee,
            }
            print("User info fetched successfully")
            
            try:
                subreddit = await user.subreddit()
                user_data["user_info"]["bio"] = subreddit.description
            except Exception as e:
                user_data["user_info"]["bio"] = "No bio available"
                print(f"Error fetching user bio: {str(e)}")
                
        except Exception as e:
            print(f"Error fetching user info: {str(e)}")
            
        # Fetch posts
        try:
            print("Starting to fetch posts")
            post_count = 0
            async for submission in user.submissions.new(limit=10):
                post_data = {
                    "title": submission.title,
                    "selftext": submission.selftext if hasattr(submission, 'selftext') else "",
                    "url": submission.url,
                    "subreddit": submission.subreddit.display_name,
                    "score": submission.score,
                    "num_comments": submission.num_comments,
                    "over_18": submission.over_18,
                    "is_video": submission.is_video,
                    "created_utc": submission.created_utc,
                }
                user_data["posts"].append(post_data)
                post_count += 1
            print(f"Fetched {post_count} posts")
        except Exception as e:
            print(f"Error fetching posts: {str(e)}")

        # Fetch comments
        try:
            print("Starting to fetch comments")
            comment_count = 0
            async for comment in user.comments.new(limit=100):
                comment_data = {
                    "body": comment.body,
                    "created_utc": comment.created_utc,
                    "score": comment.score,
                    "ups": comment.ups,
                    "subreddit": comment.subreddit.display_name,
                }
                user_data["comments"].append(comment_data)
                comment_count += 1
            print(f"Fetched {comment_count} comments")
        except Exception as e:
            print(f"Error fetching comments: {str(e)}")

        # Fetch upvoted posts
        try:
            print("Starting to fetch upvoted posts")
            upvoted_count = 0
            async for submission in user.upvoted(limit=100):
                upvoted_data = {
                    "title": submission.title,
                    "selftext": submission.selftext if hasattr(submission, 'selftext') else "",
                    "url": submission.url,
                    "subreddit": submission.subreddit.display_name,
                    "score": submission.score,
                    "num_comments": submission.num_comments,
                    "over_18": submission.over_18,
                    "is_video": submission.is_video,
                    "created_utc": submission.created_utc,
                }
                user_data["upvoted_posts"].append(upvoted_data)
                upvoted_count += 1
            print(f"Fetched {upvoted_count} upvoted posts")
        except Exception as e:
            print(f"Error fetching upvoted posts: {str(e)}")

        # Close Reddit session
        await reddit.close()
        print("Reddit session closed")
        return clean_reddit_data(user_data)
        
    except Exception as e:
        print(f"Critical error in fetch_user_data: {str(e)}")
        raise
import os
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI

def format_reddit_data(data):
    """
    Converts Reddit data (dicts, lists) into readable string format.
    """
    if isinstance(data, list):
        return "\n".join([format_reddit_data(item) for item in data])  # Recursively format lists

    if isinstance(data, dict):
        return ", ".join([f"{key}: {format_reddit_data(value)}" for key, value in data.items()])  # Format dicts

    return str(data)  # Convert everything else to string

def analyze_personality(user_data):
    """
    Uses GPT-4o to analyze a Reddit user's personality based on their activity.
    """
    openai_api_key = os.getenv("OPENAI_API_KEY")
    llm = ChatOpenAI(model="gpt-4o-mini",temperature=0.1,api_key=openai_api_key)

    # ✅ Ensure all keys exist (prevent "name 'upvoted_posts' is not defined" error)
    formatted_data = {
        "user_info": format_reddit_data(user_data.get("user_info", {})),
        "posts": format_reddit_data(user_data.get("posts", [])),
        "comments": format_reddit_data(user_data.get("comments", [])),
        "upvoted_posts": format_reddit_data(user_data.get("upvoted_posts", [])),  # ✅ Fix
        "subreddits": format_reddit_data(user_data.get("subreddits", [])),
    }

    prompt_template = PromptTemplate(
        input_variables=["user_info", "posts", "comments", "upvoted_posts", "subreddits"],
        template="""
        You are an AI personality analyst. Based on the following **Reddit activity**, generate a **detailed personality breakdown**:

        - **User Info:** {user_info}
        - **Posts (Summarized & Clustered):** {posts}
        - **Comments (Summarized & Clustered):** {comments}
        - **Upvoted posts (Summarized & Clustered):** {upvoted_posts}
        - **Subreddits:** {subreddits}
        answer in these 6 points and try to specific  .

        the main thing is all these points should fit together and not contradict each other. 
        🔍 **Analysis Categories:**
        User Activity and Engagement Patterns:
By analyzing the frequency and regularity of a user's posts, comments, and upvotes, we can understand how engaged they are. For instance, if a user posts every day and interacts actively with others’ content, they’re highly engaged. Also, observing active hours (e.g., morning vs. night) can offer insight into their routine.
rank activity on these basis
1. if more than 100 upvotes and comments per week the user is highly active , if 10-100 per week the user is medium ans less than 10 per week the user is low active
 2. you should also calculate the time period in wchich he was most active for ex from june to jult 2024 if he has maxaimum activity in that time period 
Example: A user who posts consistently at night may be a night owl or someone working irregular hours.

Content Consumption and Interests:
The subreddits a user joins reveal their core interests. A user with a diverse set of subscriptions likely has broad interests, while one with a narrow range may have specialized topics they enjoy. Additionally, analyzing if they prefer video or text-based content helps identify content type preferences.
rank content consumption 
1. if he has more thann 10 varied intrests then great and diverse , if 3 to 10 then good and if less than 4 the user is limited
Example: A user actively engaging with both r/funny and r/technology might have both a sense of humor and a technical interest.

Personality Insights from Activity and Engagement:
By studying the type of content they engage with, we can discern whether they’re a creator or a consumer. A user creating original, highly upvoted posts is likely a content creator, while someone upvoting content without posting much could be a consumer.
see if the user upvoted over 18 content 
Example: A user who posts informative content on r/science is likely an expert or enthusiast in the field.

Sentiment and Tone Analysis:
Sentiment analysis of comments helps gauge a user’s emotional tone—whether they lean more positive, negative, or neutral. Understanding their communication style (supportive, critical, etc.) adds depth to personality analysis.

Example: A user leaving positive feedback on r/fitness may be supportive and encouraging.

Content Creation and Popularity:
By evaluating the popularity of a user’s posts (number of upvotes, comments), we can determine if they’re an influential figure. Popular posts suggest the user has a significant impact within certain subreddits.

Example: A user’s post with 5,000 upvotes indicates they are likely an influential member in a specific subreddit like r/gaming.

Behavioral and Psychological Insights:
The consistency and variety of topics a user engages with show psychological traits. Frequent involvement in specific areas indicates a passion, while sporadic participation could suggest a more casual user.

Example: A user frequently posting in r/mentalhealth and r/psychology might have a deep interest in human behavior or personal growth.





        Be specific and engaging in your analysis!
        """
    )

    formatted_prompt = prompt_template.format(**formatted_data)

    # ✅ Use invoke() instead of calling llm directly
    
    
    return llm.invoke(formatted_prompt)