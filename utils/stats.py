import requests


class DiscordBotListStats:
    def __init__(self, bot):
        self.bot = bot
        self.dbl_token = self.bot.config.api_keys["dbl"]

    def update_stats(self):
        headers = {
            "Authorization": self.dbl_token,
        }
        payload = {
            "guilds": len(self.bot.guilds),
            "users": len(self.bot.users),
        }
        url = f"https://discordbotlist.com/api/v1/bots/{self.bot.user.id}/stats"
        post = requests.post(url, headers=headers, json=payload)
        if post.status_code == 200:
            self.bot.logger.info("Discord Bot List stats updated.")
        else:
            self.bot.logger.error(
                f"Failed to update Discord Bot List stats: {post.status_code} : {post.json().get('message')}"
            )

    def get_votes(self):
        headers = {
            "Authorization": self.dbl_token,
        }
        url = f"https://discordbotlist.com/api/v1/bots/{self.bot.user.id}/upvotes"
        get = requests.get(url, headers=headers)
        if get.status_code == 200:
            return get.json()
        else:
            self.bot.logger.error(
                f"Failed to fetch Discord Bot List votes: {get.status_code}"
            )
            return None
