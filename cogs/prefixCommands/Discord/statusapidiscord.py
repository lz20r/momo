import discord
from discord.ext import commands, tasks
import requests

class APIWebhook(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.webhook_urls = {}  # Store webhook URLs by channel ID
        self.api_check.start()  # Start the background task when the cog is loaded

    def cog_unload(self):
        self.api_check.cancel()  # Cancel the task when the cog is unloaded

    @commands.command(name='DisocrdApiStatus', aliases=["setSD"] , help='Sets or creates a webhook for the specified channel for API status updates.')
    @commands.has_permissions(manage_channels=True)  # Ensure only users with manage channels permission can set the webhook
    async def set_webhook(self, ctx, channel: discord.TextChannel):
        # Check if the bot has permissions to create webhooks in the specified channel
        if not channel.permissions_for(ctx.guild.me).manage_webhooks:
            await ctx.send("I don't have permission to manage webhooks in the specified channel.")
            return

        # Find existing webhooks created by the bot in the channel
        webhooks = await channel.webhooks()
        webhook = discord.utils.get(webhooks, user=ctx.guild.me)

        # If a webhook by the bot doesn't exist, create one
        if webhook is None:
            webhook = await channel.create_webhook(name="API Status Webhook")

        # Store the webhook URL in the dictionary with the channel ID as the key
        self.webhook_urls[channel.id] = webhook.url
        await ctx.send(f'Webhook for API status updates has been set for {channel.mention}.')

    @tasks.loop(minutes=60)  # Adjust the frequency of checks as needed
    async def api_check(self):
        if not self.webhook_urls:
            print("No webhooks set. Skipping API check.")
            return

        response = requests.get('https://discordstatus.com/api/v2/status.json')
        if response.status_code == 200:
            data = response.json()
            status = data['status']['description']
            if status != 'All Systems Operational':
                for channel_id, webhook_url in self.webhook_urls.items():
                    await self.send_webhook(webhook_url, status, data['page']['updated_at'])

    async def send_webhook(self, webhook_url, status, updated_at):
        content = {
            "embeds": [
                {
                    "title": "Discord API Status Alert",
                    "description": "There seems to be an issue with the Discord API.",
                    "color": 15158332,  # Red
                    "fields": [
                        {"name": "Status", "value": status},
                        {"name": "Updated", "value": updated_at}
                    ]
                }
            ]
        }

        # Send the POST request to the webhook URL
        result = requests.post(webhook_url, json=content, headers={"Content-Type": "application/json"})
        if result.status_code != 204:
            print(f"Failed to send webhook for channel ID {channel_id}, status code: {result.status_code}")

asyn def setup(bot):
    await bot.add_cog(APIWebhook(bot))