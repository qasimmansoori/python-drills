from .models import UserModel

def print_user_card(user: UserModel | None):
    if user is None:
        print("❌ Could not display user report due to an error.")
        print("-" * 55)
        return

    bio_clean = user.bio.strip().replace("\r\n", " ") if user.bio else "No bio provided"
    print(f"👤 {user.username} (ID: {user.id})")
    print(f"   📦 Repos: {user.public_repos} | 👥 Followers: {user.followers}")
    print(f"   📝 Bio: {bio_clean}")
    print("-" * 55)
