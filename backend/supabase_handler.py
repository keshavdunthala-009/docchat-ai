import os
from dotenv import load_dotenv
from supabase import create_client

# Load variables from .env when running locally
load_dotenv()


class SupabaseHandler:
    """Handle Supabase database operations"""

    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_SECRET_API_KEY")
        self.client = None

        self._connect()

    def _connect(self):
        """Connect to Supabase"""
        try:
            # Check that environment variables exist
            if not self.url:
                raise ValueError("SUPABASE_URL is missing")

            if not self.key:
                raise ValueError("SUPABASE_API_KEY is missing")

            # Remove accidental spaces/newlines
            self.url = self.url.strip()
            self.key = self.key.strip()

            # Don't print the actual secret key
            print(f"Supabase URL: {self.url}")
            print(f"Supabase key found: {bool(self.key)}")
            print(f"Supabase key type: {self.key[:12]}...")

            self.client = create_client(
                self.url,
                self.key
            )

            print("✅ Supabase connected!")

        except Exception as e:
            print(f"❌ Supabase connection error: {e}")
            self.client = None

    def save_document(
        self,
        session_id: str,
        document_name: str,
        full_text: str
    ):
        """Save document to Supabase"""
        try:
            if not self.client:
                print("❌ Supabase not connected!")
                return False

            # Delete existing document for this session
            self.client.table("documents").delete().eq(
                "session_id",
                session_id
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
                print("❌ Supabase not connected!")
                return None

            result = (
                self.client
                .table("documents")
                .select("*")
                .eq("session_id", session_id)
                .order("created_at", desc=True)
                .limit(1)
                .execute()
            )

            if result.data:
                print(
                    f"✅ Found in Supabase: "
                    f"{result.data[0]['document_name']}"
                )
                return result.data[0]

            print(f"No document found for session: {session_id}")
            return None

        except Exception as e:
            print(f"❌ Supabase get error: {e}")
            return None