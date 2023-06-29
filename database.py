import json

from supabase import Client, create_client


class Database:
    def __init__(self, URL, KEY):
        self.db: Client = create_client(URL, KEY)

    """Getters"""

    async def get_user(self, user_id):
        data = self.db.table("users").select("*").eq("user_id", user_id).execute()
        return data.data

    async def get_users(self):
        data = self.db.table("users").select("*").execute()
        return data.data

    async def get_payment_history(self, user_id):
        data = self.db.table("payment_history").select("*").eq("user_id", user_id).execute()
        return data.data

    async def get_vpn(self, vpn_id):
        data = self.db.table("vpn_keys").select("*").eq("id", vpn_id).execute()
        return data.data

    async def get_tariffs(self):
        data = self.db.table("tariffs").select("*").eq("enable", True).order("id").execute()
        return data.data

    async def get_tariff(self, tariff_id):
        data = self.db.table("tariffs").select("*").eq("id", tariff_id).execute()
        return data.data

    """Setters"""

    async def add_vpn(self, file_id, photo_id, user_id):
        return self.db.table("vpn_keys").insert({
            "file_id": file_id,
            "photo_id": photo_id,
            "user_id": user_id
        }).execute()

    async def change_vpn(self, vpn_id):
        self.db.table("vpns").update({"used": True}).eq("id", vpn_id).execute()

    async def add_new_payment(self, user_id, amount, title):
        data = {
            "user_id": user_id,
            "amount": amount,
            "type": title
        }

        self.db.table("payment_history").insert(data).execute()

    async def update_user_info(self, user_id, data):
        self.db.table("users").update(data).eq("user_id", user_id).execute()

    async def add_new_user(self, user_id, username, full_name):
        if not await self.get_user(user_id):
            data = {
                "user_id": user_id,
                "username": username,
                "full_name": full_name,
            }

            self.db.table("users").insert(data).execute()
        else:
            self.db.table("users").update({"username": username}).eq("user_id", user_id).execute()


async def json_dump(date):
    data = json.dumps(date, default=str)
    return data
