from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
from agents.personality.personality_agent import fetch_user_data, analyze_personality
import aiohttp
import os
from dotenv import load_dotenv
import urllib.parse
from utils.clean_gpt import clean_gpt_response
from fastapi.responses import PlainTextResponse
# Load environment variables
from langchain.callbacks.tracers import LangChainTracer
from langchain.callbacks.tracers import LangChainTracer
from agents.personality.memeTrendsAgent import analyze_meme_trends
load_dotenv()

router = APIRouter()

REDIRECT_URI = "http://localhost:8000/callback"
STATE = "randomstring"  # You can use a secure random state in production

@router.get("/login")
async def login():
    client_id = os.getenv("REDDIT_CLIENT_ID")
    redirect_uri = urllib.parse.quote(REDIRECT_URI, safe="")  # URL encode it
    scope = "identity history read vote"  # ✅ Ensure all required scopes are included
    url = f"https://www.reddit.com/api/v1/authorize?client_id={client_id}&response_type=code&state={STATE}&redirect_uri={redirect_uri}&duration=permanent&scope={scope}"
    return RedirectResponse(url)

# Store refresh token globally for testing (replace with database/session in production)
stored_refresh_token = None

@router.get("/callback")
async def callback(code: str, state: str):
    """
    Exchange the authorization code for an access token and store refresh token.
    """
    if state != STATE:
        raise HTTPException(status_code=400, detail="Invalid state parameter.")

    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")

    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://www.reddit.com/api/v1/access_token",
            auth=aiohttp.BasicAuth(client_id, client_secret),
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": REDIRECT_URI,
            },
            headers={"User-Agent": "RedditAnalyzer/0.1"}
        ) as response:
            token_data = await response.json()

            # Check if access token is retrieved
            if "access_token" not in token_data:
                raise HTTPException(status_code=400, detail="Failed to retrieve access token")

            access_token = token_data["access_token"]
            refresh_token = token_data.get("refresh_token")

            # Debugging: Print out the refresh token
            print(f"Access Token: {access_token}")
            print(f"Refresh Token: {refresh_token}")

            # Store refresh token globally (or in database/session for production)
            global stored_refresh_token
            stored_refresh_token = refresh_token

            # Redirect to the personality analysis page with the access token
            return RedirectResponse(f"/analyze_personality/me?access_token={access_token}")


@router.get("/analyze_personality/{username}")
async def analyze_personality_endpoint(username: str, access_token: str):
    """
    API endpoint to analyze a Reddit user's personality, interests, liked posts, and subreddit activity.
    Requires OAuth access token.
    """
    try:
        # Fetch Reddit data asynchronously
        user_data = await fetch_user_data(username, access_token,stored_refresh_token)
   

        # Analyze personality using GPT-4o
        personality = analyze_personality(user_data)
        print(personality)
        response_text = personality.content
        print("this is tre")
        print(response_text)
        # ans=clean_gpt_response(response_text)
        # print(ans)
        return PlainTextResponse(response_text)
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/fetch_reddit_data/{username}")
async def get_reddit_data(username: str, access_token: str, refresh_token: str = None):
    """
    Fetches raw Reddit user data and returns it as JSON.
    Allows sending a refresh token for authentication.
    """
    try:
        user_data = await fetch_user_data(username, access_token, refresh_token)
        return user_data  # ✅ Returns raw JSON data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/meme-trends")
def get_meme_trends():
    result = analyze_meme_trends()
    return {"trends_analysis": result}