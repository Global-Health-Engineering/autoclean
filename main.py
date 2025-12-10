from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Get your API key
api_key = os.getenv("OPENAI_API_KEY")

# Now use it
print(api_key)  # sk-proj-xxxxxx...