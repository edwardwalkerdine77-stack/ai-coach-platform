from supabase import create_client, Client

# ---------------- SUPABASE CONNECTION ----------------
SUPABASE_URL = "https://dsjhvymuaaoqcgavidrb.supabase.co"
SUPABASE_KEY = "sb_publishable_h1tLW3yVRLXVyu5aDYb3YQ_H0IehfAY"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# ---------------- HELPER FUNCTIONS ----------------

def get_user(username: str):
    """Fetch a user from Supabase"""
    response = supabase.table("users").select("*").eq("username", username).execute()

    if response.data:
        return response.data[0]
    return None


def create_user(username: str, password: str):
    """Create a new user in Supabase"""
    response = supabase.table("users").insert({
        "username": username,
        "password": password,
        "plan": "bronze"
    }).execute()

    return response.data


def update_user_plan(username: str, plan: str):
    """Update user subscription plan"""
    response = supabase.table("users").update({
        "plan": plan
    }).eq("username", username).execute()

    return response.data