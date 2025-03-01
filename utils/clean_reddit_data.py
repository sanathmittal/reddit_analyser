import datetime

def clean_value(value, default=None):
    """
    Helper function to replace missing values with a default.
    """
    if isinstance(value, str) and "Error" in value:  # If the value is an error message, return default
        return default
    if value is None or value == "":
        return default
    return value

def clean_timestamp(timestamp):
    """
    Convert Reddit's Unix timestamp to a human-readable format.
    """
    try:
        return datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    except:
        return "Unknown"

def clean_reddit_data(user_data):
    """
    Cleans and formats extracted Reddit user data.
    """
    cleaned_data = {}

    # **🔹 Clean User Info**
    if isinstance(user_data.get("user_info"), dict):  # Ensure it's a dictionary
        cleaned_data["user_info"] = {
            "name": clean_value(user_data["user_info"].get("name"), "Unknown"),
            "created_utc": clean_timestamp(user_data["user_info"].get("created_utc")),
            "link_karma": clean_value(user_data["user_info"].get("link_karma"), 0),
            "comment_karma": clean_value(user_data["user_info"].get("comment_karma"), 0),
            "total_karma": clean_value(user_data["user_info"].get("total_karma"), 0),
            "bio": clean_value(user_data["user_info"].get("bio"), "No bio available"),
            "is_employee": clean_value(user_data["user_info"].get("is_employee"), False),
        }
    else:
        cleaned_data["user_info"] = "Error fetching user info"

    # **🔹 Clean Posts Created**
    cleaned_data["posts"] = []
    if isinstance(user_data.get("posts"), list):  # Ensure it's a list
        for post in user_data["posts"]:
            cleaned_data["posts"].append({
                "title": clean_value(post.get("title"), "No Title"),
                "selftext": clean_value(post.get("selftext"), "No Content"),
                "url": clean_value(post.get("url"), "No URL"),
                "subreddit": clean_value(post.get("subreddit"), "Unknown Subreddit"),
                "score": clean_value(post.get("score"), 0),
                "num_comments": clean_value(post.get("num_comments"), 0),
                "over_18": clean_value(post.get("over_18"), False),
                "is_video": clean_value(post.get("is_video"), False),
                "created_utc": clean_timestamp(post.get("created_utc")),
            })
    else:
        cleaned_data["posts"] = "Error fetching posts"

    # **🔹 Clean Comments**
    cleaned_data["comments"] = []
    if isinstance(user_data.get("comments"), list):
        for comment in user_data["comments"]:
            cleaned_data["comments"].append({
                "body": clean_value(comment.get("body"), "No Comment"),
                "created_utc": clean_timestamp(comment.get("created_utc")),
                "score": clean_value(comment.get("score"), 0),
                "ups": clean_value(comment.get("ups"), 0),
                "subreddit": clean_value(comment.get("subreddit"), "Unknown Subreddit"),
            })
    else:
        cleaned_data["comments"] = "Error fetching comments"

    # **🔹 Clean Subreddits Joined**
    cleaned_data["subreddits"] = []
    if isinstance(user_data.get("subreddits"), list):
        for subreddit in user_data["subreddits"]:
            cleaned_data["subreddits"].append({
                "display_name": clean_value(subreddit.get("display_name"), "Unknown"),
                "name": clean_value(subreddit.get("name"), "Unknown"),
                "title": clean_value(subreddit.get("title"), "No Title"),
                "description": clean_value(subreddit.get("description"), "No Description"),
                "created_utc": clean_timestamp(subreddit.get("created_utc")),
                "over_18": clean_value(subreddit.get("over_18"), False),
                "subscribers": clean_value(subreddit.get("subscribers"), 0),
            })
    else:
        cleaned_data["subreddits"] = "Error fetching subreddits"

    # **🔹 Clean Upvoted Posts**
    cleaned_data["upvoted_posts"] = []
    if isinstance(user_data.get("upvoted_posts"), list):
        for upvote in user_data["upvoted_posts"]:
            cleaned_data["upvoted_posts"].append({
                "title": clean_value(upvote.get("title"), "No Title"),
                "selftext": clean_value(upvote.get("selftext"), "No Content"),
                "url": clean_value(upvote.get("url"), "No URL"),
                "subreddit": clean_value(upvote.get("subreddit"), "Unknown Subreddit"),
                "score": clean_value(upvote.get("score"), 0),
                "num_comments": clean_value(upvote.get("num_comments"), 0),
                "over_18": clean_value(upvote.get("over_18"), False),
                "is_video": clean_value(upvote.get("is_video"), False),
                "created_utc": clean_timestamp(upvote.get("created_utc")),
            })
    else:
        cleaned_data["upvoted_posts"] = "Error fetching upvoted posts"

    return cleaned_data
