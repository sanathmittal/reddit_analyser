Reddit Analyzer – AI-Powered Reddit Insights
📌 Project Overview
Reddit Analyzer is a multi-agent AI-powered application that analyzes Reddit data using FastAPI, LangChain, OpenAI's GPT-4o-mini, and ChromaDB. This project fetches Reddit data through the PRAW (Python Reddit API Wrapper), processes it with LLMs, and provides intelligent insights.

Currently, the project has two primary agents:

Personality & Interest Analyzer – Analyzes a user's upvoted posts and subreddit activity.
AI-Powered Meme & Viral Content Tracker – Tracks trending meme posts, subreddits, and users.
This project is designed to be fully customizable, allowing users to plug in their own Reddit credentials and run their own analysis.

📌 Agents & How They Work
1️⃣ Agent 1: Reddit Personality & Interest Analyzer
This agent analyzes a Reddit user’s personality and interests based on:
✔️ Upvoted Posts – What kind of content the user enjoys.
✔️ Frequent Subreddits – Communities where the user is most active.
✔️ Diversity of Interests – Determines if the user is interested in a wide range of topics or specific ones.
✔️ Humorous Personality Summary – Generates a fun AI-driven summary of the user’s Reddit habits.

💡 How It Works:

Fetches upvoted posts and subreddits using the Reddit API.
Structures the data and sends it to GPT-4o-mini using LangChain.
Returns a 6-point analysis in a structured format.
📌 FastAPI Route:

http
Copy
Edit
GET /analyze_personality/me?access_token=<Reddit Access Token>
Input: Reddit OAuth access token
Output: A text-based personality analysis
2️⃣ Agent 2: AI-Powered Meme & Viral Content Tracker
This agent tracks trending memes and viral content on Reddit.

✔️ Tracks Meme Posts – Fetches trending posts from hot, rising, and top categories.
✔️ Gathers All Metadata – Includes award count, comment velocity, gilding, stickied status, video content, NSFW flag, flair, and self-text.
✔️ Identifies Trending Meme Subreddits – Finds subreddits posting viral meme content.
✔️ Analyzes User Profiles – Identifies users posting viral content.
✔️ Extracts Flair & Tags – Captures post tags and common flair.
✔️ Historical Analysis – Estimates meme trends based on past data.

💡 How It Works:

Fetches trending meme content using PRAW.
Structures all metadata and converts it into a string format.
Sends data to GPT-4o-mini via LangChain PromptTemplate.
Returns an LLM-generated analysis of meme trends.
📌 FastAPI Route:

http
Copy
Edit
GET /meme_trends?access_token=<Reddit Access Token>
Input: Reddit OAuth access token
Output: AI-generated analysis of trending memes
📌 Setup & Installation Guide
1️⃣ Prerequisites
Ensure you have the following installed:
✅ Python 3.10+
✅ Poetry (for dependency management)
✅ Git
✅ FastAPI & Uvicorn

2️⃣ Clone the Repository
Run the following command:

bash
Copy
Edit
git clone https://github.com/yourusername/reddit-analyzer.git
cd reddit-analyzer
3️⃣ Install Dependencies
We are using Poetry for package management. Run:

bash
Copy
Edit
poetry install
If you don’t have Poetry, install it first:

bash
Copy
Edit
pip install poetry
4️⃣ Set Up Your Reddit API Credentials
Since we use the Reddit API (PRAW), you need to create a Reddit app and obtain API credentials.

📌 Steps to Create a Reddit App:
Go to Reddit Developer Portal.
Click "Create App".
Choose "script" as the app type.
Fill in:
Name: Any name you want
Redirect URI: http://localhost:8000/
Permissions: Select all required scopes
Click Create App.
Copy your Client ID and Client Secret.
5️⃣ Configure .env File
Inside your project, create a .env file and store your credentials:

ini
Copy
Edit
REDDIT_CLIENT_ID="your-client-id"
REDDIT_CLIENT_SECRET="your-client-secret"
REDDIT_USER_AGENT="your-app-name"
OPENAI_API_KEY="your-openai-api-key"
6️⃣ Run the FastAPI Server
Start the application:

bash
Copy
Edit
poetry run uvicorn main:app --reload
The API will be available at:

cpp
Copy
Edit
http://127.0.0.1:8000
📌 FastAPI Routes & How to Use Them
1️⃣ Get Personality Analysis
📌 Endpoint:

http
Copy
Edit
GET /analyze_personality/me?access_token=<Reddit Access Token>
📌 Example Response:

markdown
Copy
Edit
Personality Analysis:
1. You love tech news and AI discussions.
2. You frequently engage in meme content.
3. Your subreddit activity is diverse, ranging from gaming to philosophy.
...
2️⃣ Get Meme Trends
📌 Endpoint:

http
Copy
Edit
GET /meme_trends?access_token=<Reddit Access Token>
📌 Example Response:

bash
Copy
Edit
Meme Trends Analysis:
1. Memes related to "Elden Ring" are trending in r/gamingmemes.
2. Viral meme formats include "Expanding Brain" and "Drakeposting".
...
📌 Future Plans
🚀 More AI Agents – Adding more insights & trends beyond memes and personalities.
📈 Better Historical Data Analysis – Storing meme trends over time.
💡 User Recommendations – Suggesting meme formats based on past trends.

📌 Contributing
We’d love to grow this project with community contributions! 🚀

Here’s how you can contribute:

🔹 Add More AI Agents
Want to analyze something new?
You can create a new agent that fetches Reddit data, uses LangChain & GPT, and provides useful insights.
Examples:
Subreddit Sentiment Analyzer
Reddit Comment Toxicity Detector
AI-Powered Reddit Post Recommender
🔹 Build a Frontend
We currently have a FastAPI backend but no UI.
A frontend using Streamlit, React, or Flask would make this app more user-friendly!
🔹 Improve Meme Trend Analysis
Help us refine meme tracking using historical trends and real-time Reddit API updates.
🔹 Submit a Pull Request
Fork the repository
Create a new branch
Make changes & commit
Submit a Pull Request (PR)
Let’s build something awesome together! 🚀🔥
