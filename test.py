import os
from dotenv import load_dotenv

# 1. Load variables from .env
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

print("--- Step 1: Checking .env loading ---")
if not api_key:
    print("❌ FAILED: GOOGLE_API_KEY is not set or .env file is missing/empty.")
    exit(1)

# Mask the key so it's safe to view on screen
masked_key = f"{api_key[:6]}...{api_key[-4:]}"
print(f"✅ SUCCESS: Key loaded from .env: {masked_key}")

# 2. Test actual API connectivity with a minimal call
print("\n--- Step 2: Testing connection to Gemini API ---")
try:
    from langchain_google_genai import ChatGoogleGenerativeAI

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.8-flash",
        temperature=0.6
    )

    response = llm.invoke("Reply with the single word: Connected")
    print(f"✅ SUCCESS: API responded: {response.text}")
    print("\n🎉 Your environment is properly configured!")

except Exception as e:
    print(f"❌ FAILED: API call threw an error:\n{e}")