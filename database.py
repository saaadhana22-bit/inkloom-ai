
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing Supabase credentials in .env")

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def test_connection():
    """Check Supabase configuration."""
    try:
        if supabase is None:
            return False

        print("Supabase client initialized successfully.")
        print("Project URL:", SUPABASE_URL)
        return True

    except Exception as error:
        print("Connection test failed:", error)
        return False


def save_rewrite(original_text, rewritten_text, tone):
    try:
        data = {
            "original_text": original_text,
            "rewritten_text": rewritten_text,
            "tone": tone
        }

        supabase.table("rewrite_history").insert(
            data,
            returning="minimal"
        ).execute()

        print("Rewrite saved successfully!")
        return True

    except Exception as error:
        print("Failed to save rewrite:", error)
        return False

if __name__ == "__main__":
    test_connection()
