import json
import re  # Import the regular expression module
response=response = {
    "username": "me",
    "personality": {
        "content": "### Personality Breakdown of User: mayhem_king007\n\n#### 1. User Activity and Engagement Patterns:\nmayhem_king007 exhibits a moderate level of engagement on Reddit, with a total karma of 34, primarily derived from comments (33) rather than posts (1). This suggests that the user prefers to engage with existing content rather than create new posts. The user’s activity appears to be more concentrated in late December 2024, indicating a possible seasonal interest or a recent increase in engagement. The comments are often humorous or relatable, suggesting that the user enjoys light-hearted interactions. The sporadic nature of their activity may indicate a casual user who engages with the platform when they find content that resonates with them.\n\n#### 2. Content Consumption and Interests:\nThe user’s engagement spans various subreddits, primarily focusing on humor and memes (e.g., r/IndianDankMemes, r/FingMemes, r/DesiVideoMemes). This indicates a strong interest in comedic content and a preference for visual or video-based humor. Additionally, the user has shown interest in more serious topics, such as personal development and job skills, as seen in their comment on r/sunraybee. This blend of interests suggests that mayhem_king007 enjoys both entertainment and self-improvement, reflecting a balanced personality that appreciates humor while also valuing personal growth.\n\n#### 3. Personality Insights from Activity and Engagement:\nmayhem_king007 appears to be more of a consumer than a creator, as evidenced by their low number of posts compared to comments. The user’s comments often reflect a humorous and relatable tone, indicating a personality that values connection through shared experiences and laughter. Their engagement style suggests they are likely to be an observer who enjoys participating in discussions rather than leading them. This could imply a more introverted personality, comfortable with expressing thoughts in a supportive community rather than taking center stage.\n\n#### 4. Sentiment and Tone Analysis:\nThe sentiment of mayhem_king007’s comments leans towards the positive and humorous side. Phrases like \"Zyaada dark ho gya.... humor bhi nhi dikh rha😂\" and \"Ghar mai chawal khatam hone k baad mai....🥺\" showcase a playful and light-hearted approach to communication. The user also expresses empathy and understanding in their advice about personal development, indicating a supportive and encouraging nature. This blend of humor and empathy suggests a personality that values positivity and connection with others, likely making them approachable and relatable within their online interactions.\n\n#### 5. Content Creation and Popularity:\nWhile mayhem_king007 has only one post, it has garnered significant attention, indicating that they have the potential to create engaging content. The user’s upvoted posts, particularly those related to humor and memes, suggest they have a knack for identifying and sharing content that resonates with a broader audience. This ability to engage with popular content indicates that they are in tune with current trends and cultural references, which enhances their influence within the communities they participate in.\n\n#### 6. Behavioral and Psychological Insights:\nThe variety in mayhem_king007’s engagement—from humorous memes to thoughtful advice—suggests a multifaceted personality. Their frequent interaction with comedic content indicates a desire for entertainment and a light-hearted approach to life, while their comments on personal development reflect a deeper, introspective side. This duality may point to a personality that values both fun and growth, indicating a well-rounded individual who seeks to balance enjoyment with self-improvement. The user’s engagement patterns suggest they are likely to be adaptable, enjoying both social interactions and moments of reflection.\n\n### Conclusion:\nIn summary, mayhem_king007 is a humorous and relatable individual who enjoys engaging with comedic content while also valuing personal growth. Their activity suggests a casual yet thoughtful approach to Reddit, where they contribute positively to discussions and connect with others through shared experiences. This blend of humor and introspection paints a picture of a well-rounded personality that appreciates both the lighter and more serious aspects of life.",
        "additional_kwargs": {}
    },
    "response_metadata": {
        "token_usage": {
            "completion_tokens": 816,
            "prompt_tokens": 4142,
            "total_tokens": 4958,
            "completion_tokens_details": {
                "accepted_prediction_tokens": 0,
                "audio_tokens": 0,
                "reasoning_tokens": 0,
                "rejected_prediction_tokens": 0
            },
            "prompt_tokens_details": {
                "audio_tokens": 0,
                "cached_tokens": 0
            }
        },
        "model_name": "gpt-4o-mini",
        "system_fingerprint": "fp_7fcd609668",
        "finish_reason": "stop",
        "logprobs": None
    },
    "type": "ai",
    "name": None,
    "id": "run-81b40bfa-ae8a-4fca-9012-2a2248241729-0",
    "example": False,
    "tool_calls": [],
    "invalid_tool_calls": [],
    "usage_metadata": None
}

def clean_gpt_response(json_response):
    """
    Cleans a JSON response and returns a formatted string with key points.
    Removes ** from start and end of headings.
    """
    try:
        if isinstance(json_response, str):
            response_dict = json.loads(json_response)
        else:
            response_dict = json_response

        content = response_dict["personality"]["content"]

        sections = content.split("#### ")
        points_string = ""

        for i in range(1, 7):
            try:
                section_title = sections[i].split("\n")[0].strip().replace(".","")

                # Remove ** from start and end of the heading using regex:
                section_title = re.sub(r"^\*\*|\*\*$", "", section_title).strip() # added this line

                section_content = "\n".join(sections[i].split("\n")[1:]).strip()
                points_string += f"\n\n{section_title}\n{section_content}"
            except IndexError:
                print(f"Warning: Section {i} not found in GPT response.")
                points_string += f"\n\nPoint {i}:\n"

        return points_string

    except (json.JSONDecodeError, KeyError, TypeError) as e:
        print(f"Error processing GPT response: {e}")
        return None

# Example usage:
cleaned_data = clean_gpt_response(response)  # 'response' is your JSON data

if cleaned_data:
    print(cleaned_data)  # Print the formatted string
else:
    print("Failed to clean GPT response.")


# Example with a JSON string:
response_string = '{"username":"me","personality":{"content":"### Personality Breakdown of User: mayhem_king007\\n\\n#### 1. User Activity and Engagement Patterns:\\nmayhem_king007 exhibits a moderate level of engagement...\\n\\n#### 2. Content Consumption and Interests:\\nThe user’s engagement spans various subreddits...\\n\\n#### 3. Personality Insights from Activity and Engagement:\\nmayhem_king007 appears to be more of a consumer than a creator...\\n\\n#### 4. Sentiment and Tone Analysis:\\nThe sentiment of mayhem_king007’s comments leans towards...\\n\\n#### 5. Content Creation and Popularity:\\nWhile mayhem_king007 has only one post...\\n\\n#### 6. Behavioral and Psychological Insights:\\nThe variety in mayhem_king007’s engagement—from humorous memes...\\n\\n### Conclusion:\\nIn summary, mayhem_king007 is a humorous and relatable...","additional_kwargs":{},"response_metadata":{"token_usage":{"completion_tokens":816,"prompt_tokens":4142,"total_tokens":4958,"completion_tokens_details":{"accepted_prediction_tokens":0,"audio_tokens":0,"reasoning_tokens":0,"rejected_prediction_tokens":0},"prompt_tokens_details":{"audio_tokens":0,"cached_tokens":0}},"model_name":"gpt-4o-mini","system_fingerprint":"fp_7fcd609668","finish_reason":"stop","logprobs":null},"type":"ai","name":null,"id":"run-81b40bfa-ae8a-4fca-9012-2a2248241729-0","example":false,"tool_calls":[],"invalid_tool_calls":[],"usage_metadata":null}}'

cleaned_data_from_string = clean_gpt_response(response_string)

if cleaned_data_from_string:
    print(cleaned_data_from_string)  # Print the formatted string
else:
    print("Failed to clean GPT response.")