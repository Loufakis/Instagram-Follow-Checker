import os
import time
from instagrapi import Client
from instagrapi.exceptions import TwoFactorRequired
from dotenv import load_dotenv


def save_to_file(filename: str, usernames: list[str]) -> None:
    """
    Saves a list of Instagram usernames to a text file.

    Args:
        filename (str): The file path to save the data.
        usernames (list[str]): The list of usernames to write.
    """
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Write each username to a new line in the file
    with open(filename, 'w') as f:
        f.writelines(f"{user}\n" for user in usernames)


def get_env_variable(key: str) -> str:
    """
    Retrieves a required environment variable from the .env file.

    Args:
        key (str): The name of the environment variable.

    Returns:
        str: The value of the environment variable.

    Raises:
        ValueError: If the environment variable is missing.
    """
    value = os.getenv(key)
    if not value:
        raise ValueError(f"{key} not found in .env")
    return value


def login_with_env(session_file: str = "session.json") -> Client:
    """
    Logs into Instagram using credentials from the .env file,
    handling 2FA if required, and reusing session if available.

    Args:
        session_file (str): Path to the saved session file.

    Returns:
        Client: Authenticated instagrapi client instance.
    """
    cl = Client()
    username = get_env_variable("IG_USERNAME")
    password = get_env_variable("IG_PASSWORD")

    # Attempt to reuse an existing session to avoid logging in again
    if os.path.exists(session_file):
        try:
            cl.load_settings(session_file)        # Load saved session settings
            cl.login(username, password)          # Attempt login using session
            cl.get_timeline_feed()                # Test if session is still valid
            print("✅ Logged in using saved session")
            return cl
        except Exception as e:
            print("⚠️ Failed to reuse session:", e)
            os.remove(session_file)               # Delete invalid session and fallback to fresh login

    # Fallback to fresh login
    try:
        cl.login(username, password)
        print("✅ Logged in fresh and session saved")
    except TwoFactorRequired:
        # If 2FA is enabled, prompt user for the code
        verification_code = input("🔐 Enter the 2FA code sent to your device: ").strip()
        cl.login(username, password, verification_code=verification_code)
        print("✅ Logged in with 2FA successfully")

    # Save the session for future runs
    cl.dump_settings(session_file)
    return cl


def compare_followers_and_following(cl: Client, username: str) -> None:
    """
    Compares your followers and following lists and saves usernames to CSV files.

    Args:
        cl (Client): Authenticated instagrapi client.
        username (str): Your Instagram username.
    """
    # Get the internal Instagram user ID
    user_id = cl.user_id_from_username(username)

    print("📥 Fetching followers...")
    followers = cl.user_followers(user_id)
    time.sleep(3)  # Pause to mimic human behavior

    print("📤 Fetching following...")
    following = cl.user_following(user_id)
    time.sleep(3)  # Pause to mimic human behavior

    # Extract just the usernames from user objects
    followers_usernames = sorted({user.username for user in followers.values()})
    following_usernames = sorted({user.username for user in following.values()})

    # Determine who you follow that doesn’t follow you back
    not_following_back = sorted(set(following_usernames) - set(followers_usernames))

    # Determine who follows you but you don’t follow back
    not_followed_back = sorted(set(followers_usernames) - set(following_usernames))

    # Make sure the output folder exists
    os.makedirs("outputs", exist_ok=True)

    # Save the results as .txt files
    with open("outputs/not_following_back.txt", "w") as f:
        f.writelines(f"{username}\n" for username in not_following_back)

    with open("outputs/fans.txt", "w") as f:
        f.writelines(f"{username}\n" for username in not_followed_back)

    print("✅ TXT files saved:")
    print(f"   • {len(not_following_back)} not following you back → outputs/not_following_back.txt")
    print(f"   • {len(not_followed_back)} you’re not following back → outputs/fans.txt")


# Entry point of the script
if __name__ == "__main__":
    load_dotenv()  # Load credentials from .env file
    client = login_with_env()
    username = get_env_variable("IG_USERNAME")
    compare_followers_and_following(client, username)
