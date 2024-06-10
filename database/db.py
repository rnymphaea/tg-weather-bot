import json

def create_db():
    with open("db.json", "w") as f:
        json.dump({"users_data": []}, f)


def get_users_data():
    with open ("db.json", "r") as f:
        data = json.load(f)
        return data["users_data"]


def add_user_info(info: dict):
    # info represents a dictionary with keys tg-id and city of this user
    with open("db.json", "r+") as f:
        data = json.load(f)
        if (check_iser_exists(info["telegram_id"])):
            return
        data["users_data"].append(info)
        f.seek(0)
        json.dump(data, f, ensure_ascii=False)


def update_user_info(info: dict):
    with open("db.json", "r+") as f:
        data = json.load(f)
        for key in data["users_data"]:
            if key["telegram_id"] == info["telegram_id"]:
                key["city"] = info["city"]
        f.truncate(0)
        f.seek(0)
        json.dump(data, f, ensure_ascii=False)


def check_iser_exists(id):
    with open("db.json", "r") as f:
        data = json.load(f)
        for d in data["users_data"]:
            if id == d['telegram_id']:
                return True
        return False



