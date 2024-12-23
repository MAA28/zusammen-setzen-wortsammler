from supabase import create_client, Client
from dotenv import dotenv_values

config = dotenv_values(".env")

url: str = config["SUPABASE_URL"]
key: str = config["SUPABASE_KEY"]
supabase: Client = create_client(url, key)
