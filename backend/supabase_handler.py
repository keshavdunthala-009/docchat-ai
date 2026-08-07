import os
from dotenv import load_dotenv

load_dotenv()


class SupabaseHandler:
    """Handle Supabase database operations"""

    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        self.client = None
        self._connect()

    def _connect(self):
        """Connect to Supabase"""
        try:
            from supabase_handler import create_client
            if self.url and self.key:
                self.client = create_client(self.url, self.key)
                print("✅ Supabase connected!")
            else:
                print("❌ Supabase credentials missing!")
        except Exception as e:
            print(f"❌ Supabase connection error: {e}")

    def save_document(self, session_id: str, document_name: str, full_text: str):
        """Save document to Supabase"""
        try:
            if not self.client:
                print("Supabase not connected!")
                return False

            # Delete old document for this session
            self.client.table("documents").delete().eq(
                "session_id", session_id
            ).execute()

            # Insert new document
            self.client.table("documents").insert({
                "session_id": session_id,
                "document_name": document_name,
                "full_text": full_text
            }).execute()

            print(f"✅ Saved to Supabase: {document_name}")
            return True

        except Exception as e:
            print(f"❌ Supabase save error: {e}")
            return False

    def get_document(self, session_id: str):
        """Get document from Supabase"""
        try:
            if not self.client:
                print("Supabase not connected!")
                return None

            result = self.client.table("documents").select("*").eq(
                "session_id", session_id
            ).order("created_at", desc=True).limit(1).execute()

            if result.data:
                print(f"✅ Found in Supabase: {result.data[0]['document_name']}")
                return result.data[0]
            else:
                print(f"No document found for session: {session_id}")
                return None

        except Exception as e:
            print(f"❌ Supabase get error: {e}")
            return None