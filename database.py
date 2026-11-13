
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing Supabase credentials in .env")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def test_connection():
    try:
        print("Supabase client initialized successfully.")
        return True
    except Exception as error:
        print("Connection test failed:", error)
        return False


# Existing rewrite history
def save_rewrite(original_text, rewritten_text, tone):
    try:
        supabase.table("rewrite_history").insert({
            "original_text": original_text,
            "rewritten_text": rewritten_text,
            "tone": tone
        }, returning="minimal").execute()
        return True
    except Exception as error:
        print("Failed to save rewrite:", error)
        return False


# FEATURE 1: HUMAN REVIEW WORKFLOW
def save_review(brand_name, original_text, rewritten_text):
    try:
        response = supabase.table("content_reviews").insert({
            "brand_name": brand_name,
            "original_text": original_text,
            "rewritten_text": rewritten_text,
            "status": "Draft"
        }).execute()
        return response.data[0] if response.data else None
    except Exception as error:
        print("Review save failed:", error)
        return None


def get_reviews():
    try:
        response = supabase.table("content_reviews").select("*").order(
            "created_at", desc=True
        ).execute()
        return response.data or []
    except Exception as error:
        print("Review retrieval failed:", error)
        return []


def update_review(review_id, status, comment):
    allowed = ["Draft", "Under Review", "Changes Requested", "Approved"]

    if status not in allowed:
        return False

    try:
        supabase.table("content_reviews").update({
            "status": status,
            "reviewer_comment": comment
        }).eq("id", review_id).execute()
        return True
    except Exception as error:
        print("Review update failed:", error)
        return False


# FEATURE 2: RECURRING MISTAKE TRACKER
def save_mistakes(brand_name, issues, original_text):
    try:
        records = [
            {
                "brand_name": brand_name,
                "issue_type": issue["type"],
                "issue_description": issue["description"],
                "original_text": original_text
            }
            for issue in issues
        ]

        if not records:
            return True

        supabase.table("mistake_logs").insert(records).execute()
        return True
    except Exception as error:
        print("Mistake logging failed:", error)
        return False


def get_mistake_summary():
    try:
        response = supabase.table("mistake_logs").select("*").execute()
        return response.data or []
    except Exception as error:
        print("Mistake retrieval failed:", error)
        return []


# FEATURE 3: BRAND FACT AND REFERENCE CHECKING
def save_brand_fact(brand_name, fact_text, fact_type="General"):
    try:
        response = supabase.table("brand_facts").insert({
            "brand_name": brand_name,
            "fact_text": fact_text,
            "fact_type": fact_type
        }).execute()
        return response.data[0] if response.data else True
    except Exception as error:
        print("Brand fact save failed:", error)
        return False


def get_brand_facts(brand_name):
    try:
        response = supabase.table("brand_facts").select("*").eq(
            "brand_name", brand_name
        ).execute()
        return response.data or []
    except Exception as error:
        print("Brand fact retrieval failed:", error)
        return []


if __name__ == "__main__":
    test_connection()
