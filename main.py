import sys
import asyncio
from github_reporter.client import fetch_all_users
from github_reporter.printer import print_user_card

async def cli():
    usernames = sys.argv[1:]

    if not usernames:
        print("⚠️ Usage: uv run main.py <username1> <username2> ...")

    else:
        print(f"Fetching Github reports for {','.join(usernames)}...\n")

        results = await fetch_all_users(usernames)

        for user in results:
            print_user_card(user)

if __name__ == "__main__":
    asyncio.run(cli())