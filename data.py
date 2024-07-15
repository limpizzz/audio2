from config import max_seconds
import logging

user_seconds = {}


def update_user_seconds(user_id, seconds):
    total_seconds = user_seconds.get(user_id, 0) + seconds
    if total_seconds > max_seconds:
        return False
    user_seconds[user_id] = total_seconds
    return True


def check_limit(user_id, length_of_text):
    try:
        current_usage = user_seconds.get(user_id, 0)
        new_usage = current_usage + length_of_text
        return new_usage <= max_seconds
    except Exception as e:
        logging.error(f"Error checking token limit for user {user_id}: {str(e)}")
        return False


def update_usage(user_id, length_of_text):
    if not check_limit(user_id, length_of_text):
        logging.warning(f"Attempt to exceed token limit for user {user_id}. Operation aborted.")
        return

    try:
        user_seconds[user_id] = max(0, user_seconds.get(user_id, 0) + length_of_text)
        logging.info(f"Updated token usage for user {user_id}. New usage: {user_seconds[user_id]}")
    except Exception as e:
        logging.error(f"Error updating token usage for user {user_id}: {str(e)}")


def reset_or_initialize_user(user_id):
    try:
        user_seconds[user_id] = 0
        logging.info(f"Token count for user {user_id} has been reset.")
    except Exception as e:
        logging.error(f"Error resetting token count for user {user_id}: {str(e)}")


def get_user_token_usage(user_id):
    return user_seconds.get(user_id, 0)
