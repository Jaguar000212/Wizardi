import disnake
from disnake.ext import commands
import json
import requests
import animec
import datetime
from disnake.ext.commands.params import Param

from utils.exceptions import NoNeko
from bot import Bot


class Anime(commands.Cog):
    """For Anime fun"""

    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    def neko_api(ctx, x, msg=""):
        """
        Fetches data from the nekos.fun API and creates an embed with the image.

        Parameters:
        - ctx (disnake.AppCmdInter): The context of the command.
        - x (str): The type of neko image to fetch.
        - msg (str): Additional message to include in the embed.

        Returns:
        - embed (disnake.Embed): The embed with the neko image.
        """
        req = requests.get(f"http://api.nekos.fun:8080/api/{x}")
        if req.status_code != 200:
            raise NoNeko("Couldn't load image")
        embed = disnake.Embed(description=msg, colour=0x428DFF)
        embed.set_image(url=json.loads(req.text)["image"])
        embed.set_author(
            name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url
        )
        return embed

    @commands.guild_only()
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.slash_command(
        name="anime-info", description="Get info about an Anime or a Manga"
    )
    async def info(
        self, ctx: disnake.AppCmdInter, name=Param(description="Title of the series")
    ):
        """
        Retrieves information about an anime or manga series and sends an embed with the details.

        Parameters:
        - ctx (disnake.AppCmdInter): The context of the command.
        - name (str): The title of the anime or manga series.

        Returns:
        - None
        """
        await ctx.response.defer()
        anime = animec.Anime(name)
        try:
            embed = disnake.Embed(
                title=anime.title_english,
                url=anime.url,
                description=f"{anime.description[:300]}....",
                color=disnake.Colour.random(),
            )
            embed.add_field(name="Episodes", value=str(anime.episodes))
            embed.add_field(name="Rating", value=str(anime.rating))
            embed.add_field(name="Aired", value=str(anime.aired))
            embed.add_field(name="Ranked", value=str(anime.ranked))
            embed.add_field(name="Popularity", value=str(anime.popularity))
            embed.add_field(name="Favourites", value=str(anime.favorites))
            embed.add_field(name="Broadcast", value=str(anime.broadcast))
            embed.add_field(name="Status", value=str(anime.status))
            embed.add_field(name="Type", value=str(anime.type))
            embed.add_field(
                name="Name of the anime in japanese", value=str(anime.title_jp)
            )
            embed.add_field(
                name="The Anime is also known as", value=str(anime.alt_titles)
            )
            embed.add_field(name="Producers", value=(", ".join(anime.producers)))
            embed.add_field(name="Genres", value=", ".join(anime.genres))
            embed.add_field(name="Teaser", value=str(anime.teaser))
            embed.add_field(name="Recommend", value=", ".join(anime.recommend()))
            embed.add_field(name="NSFW status", value="🔞" if anime.is_nsfw() else "🆗")
            embed.set_thumbnail(url=anime.poster)
            embed.set_author(
                name=ctx.bot.user.display_name, icon_url=f"{ctx.bot.user.avatar.url}"
            )
            embed.set_footer(
                text=f"Requested by {ctx.author.display_name}",
                icon_url=ctx.author.display_avatar.url,
            )
            await ctx.send(embed=embed)
        except AttributeError:
            await ctx.send(
                embed=disnake.Embed(
                    description=f"{self.bot.icons['failed']} No corresponding Anime is found for the search query",
                    color=disnake.Colour.red(),
                ),
                delete_after=5,
            )
            return

    @commands.guild_only()
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.slash_command(
        name="anime-character", description="Get image of an Anime or Manga character"
    )
    async def character(
        self,
        ctx: disnake.AppCmdInter,
        name: str = Param(description="Name of the character"),
    ):
        """
        Retrieves the image of an anime or manga character and sends an embed with the image.

        Parameters:
        - ctx (disnake.AppCmdInter): The context of the command.
        - name (str): The name of the character.

        Returns:
        - None
        """
        await ctx.response.defer()
        try:
            char = animec.Charsearch(name)
        except animec.errors.NoResultFound:
            await ctx.send(
                embed=disnake.Embed(
                    description=f"{self.bot.icons['failed']} No corresponding Anime Character is found for the search query",
                    color=disnake.Colour.red(),
                ),
                delete_after=5,
            )
            return
        embed = disnake.Embed(
            title=char.title, url=char.url, color=disnake.Colour.random()
        )
        embed.set_image(url=char.image_url)
        embed.set_footer(text=", ".join(list(char.references.keys())[:2]))
        embed.set_author(
            name=ctx.bot.user.display_name, icon_url=f"{ctx.bot.user.avatar.url}"
        )
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.slash_command(name="anime-news", description="Get latest anime news")
    async def news(
        self,
        ctx: disnake.AppCmdInter,
        amount: int = Param(3, description="No of news per request"),
    ):
        """
        Retrieves the latest anime news and sends an embed with the news articles.

        Parameters:
        - ctx (disnake.AppCmdInter): The context of the command.
        - amount (int): The number of news articles to retrieve.

        Returns:
        - None
        """
        num_emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣"]
        await ctx.response.defer()
        try:
            news = animec.Aninews(amount)
        except animec.errors.TooManyRequests as e:
            await ctx.send(
                embed=disnake.Embed(
                    description=f"{self.bot.icons['warning']} Amount cannot exceed 8 per command",
                    color=disnake.Colour.red(),
                ),
                delete_after=5,
            )
            return
        links = news.links
        titles = news.titles
        descriptions = news.description

        embed = disnake.Embed(
            title="Latest Anime News 🗞️",
            color=disnake.Colour.random(),
            timestamp=datetime.datetime.utcnow(),
        )
        embed.set_author(
            name=ctx.bot.user.display_name, icon_url=f"{ctx.bot.user.avatar.url}"
        )
        embed.set_footer(
            text=f"Requested by {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url,
        )
        embed.set_thumbnail(url=news.images[0])

        for i in range(amount):
            embed.add_field(
                name=f"{num_emojis[i]} {titles[i]}",
                value=f"> {descriptions[i][:200]}...\n[Read more]({links[i]})",
                inline=False,
            )
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.slash_command(name="emote-neko", description="Post a neko")
    async def neko(self, ctx: disnake.AppCmdInter):
        """
        Sends an embed with a random neko image.

        Parameters:
        - ctx (disnake.AppCmdInter): The context of the command.

        Returns:
        - None
        """
        await ctx.response.defer()
        await ctx.send(embed=self.neko_api(ctx, "neko"))

    @commands.guild_only()
    @commands.cooldown(1, 5)
    @commands.slash_command(name="emote-waifu", description="Post a waifu")
    async def waifu(self, ctx: disnake.AppCmdInter):
        """
        Sends an embed with a random waifu image.

        Parameters:
        - ctx (disnake.AppCmdInter): The context of the command.

        Returns:
        - None
        """
        await ctx.response.defer()
        await ctx.send(embed=self.neko_api(ctx, "waifu"))

    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.slash_command(name="emote-tickle", description="Tickle any member")
    async def tickle(
        self,
        ctx: disnake.AppCmdInter,
        member: disnake.Member = Param(description="mention a member"),
    ):
        """
        Sends an embed with a neko image and mentions the member being tickled.

        Parameters:
        - ctx (disnake.AppCmdInter): The context of the command.
        - member (disnake.Member): The member to be tickled.

        Returns:
        - None
        """
        await ctx.response.defer()
        try:
            await ctx.send(
                embed=self.neko_api(
                    ctx, "tickle", f"{member.mention} is laughing hard!"
                )
            )
        except commands.MemberNotFound:
            return await ctx.send("Whom to tickle?", delete_after=5)

    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.slash_command(name="emote-poke", description="Poke a member")
    async def poke(
        self,
        ctx: disnake.AppCmdInter,
        member: disnake.Member = Param(description="mention a member"),
    ):
        """
        Sends an embed with a neko image and mentions the member being poked.

        Parameters:
        - ctx (disnake.AppCmdInter): The context of the command.
        - member (disnake.Member): The member to be poked.

        Returns:
        - None
        """
        await ctx.response.defer()
        try:
            await ctx.send(
                embed=self.neko_api(ctx, "poke", f"{member.mention} got poked!")
            )
        except commands.MemberNotFound:
            return await ctx.send("Whom to poke?", delete_after=5)

    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.slash_command(name="emote-kiss", description="Kiss a member")
    async def kiss(
        self,
        ctx: disnake.AppCmdInter,
        member: disnake.Member = Param(description="mention a member"),
    ):
        """
        Sends an embed with a neko image and mentions the members involved in a kiss.

        Parameters:
        - ctx (disnake.AppCmdInter): The context of the command.
        - member (disnake.Member): The member to be kissed.

        Returns:
        - None
        """
        await ctx.response.defer()
        try:
            await ctx.send(
                embed=self.neko_api(
                    ctx, "kiss", f"{ctx.author.mention} kisses {member.mention} 💓"
                )
            )
        except commands.MemberNotFound:
            return await ctx.send("Whose that? Again please!", delete_after=5)

    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.slash_command(name="emote-slap", description="Slap a member")
    async def slap(
        self,
        ctx: disnake.AppCmdInter,
        member: disnake.Member = Param(description="mention a member"),
    ):
        """
        Sends an embed with a neko image and mentions the member being slapped.

        Parameters:
        - ctx (disnake.AppCmdInter): The context of the command.
        - member (disnake.Member): The member to be slapped.

        Returns:
        - None
        """
        await ctx.response.defer()
        try:
            await ctx.send(
                embed=self.neko_api(
                    ctx, "slap", f"Thatt! {member.mention} wish no one saw that!"
                )
            )
        except commands.MemberNotFound:
            return await ctx.send("Whom to defame?", delete_after=5)

    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.slash_command(name="emote-lick", description="Lick any member")
    async def lick(
        self,
        ctx: disnake.AppCmdInter,
        member: disnake.Member = Param(description="mention a member"),
    ):
        """
        Licks a specified member.

        Parameters:
        - ctx: The context of the command.
        - member: The member to be licked.

        Returns:
        None
        """
        await ctx.response.defer()
        try:
            await ctx.send(embed=self.neko_api(ctx, "lick", f"Licked {member.mention}"))
        except commands.MemberNotFound:
            return await ctx.send("Whom to lick?", delete_after=5)

    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.slash_command(name="emote-hug", description="Hug any member")
    async def hug(
        self,
        ctx: disnake.AppCmdInter,
        member: disnake.Member = Param(description="mention a member"),
    ):
        """
        Sends a hug message to the specified member.

        Parameters:
        - ctx: The context of the command.
        - member: The member to hug.

        Returns:
        None
        """
        await ctx.response.defer()
        try:
            await ctx.send(embed=self.neko_api(ctx, "hug", f"Hugged {member.mention}"))
        except commands.MemberNotFound:
            return await ctx.send("Whom to hug?", delete_after=5)

    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.slash_command(name="emote-pat", description="Pat any member")
    async def pat(
        self,
        ctx: disnake.AppCmdInter,
        member: disnake.Member = Param(description="mention a member"),
    ):
        """
        Pat a member.

        Parameters:
        - ctx (disnake.AppCmdInter): The context of the command.
        - member (disnake.Member): The member to pat.

        Returns:
        None
        """
        await ctx.response.defer()
        try:
            await ctx.send(embed=self.neko_api(ctx, "pat", f"patted {member.mention}"))
        except commands.MemberNotFound:
            return await ctx.send("Whom to pat?", delete_after=5)

    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.slash_command(name="emote-cry", description="Show you're broken")
    async def cry(self, ctx: disnake.AppCmdInter):
        """
        Sends a cry animation.

        Parameters:
        - ctx: The context object representing the command invocation.

        Returns:
        - None
        """
        await ctx.response.defer()
        await ctx.send(embed=self.neko_api(ctx, "cry"))

    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.slash_command(name="emote-smug", description="Smug")
    async def smug(self, ctx: disnake.AppCmdInter):
        """
        Sends a smug anime image.

        Parameters:
        - ctx: The Discord context object.

        Returns:
        - None
        """
        await ctx.response.defer()
        await ctx.send(embed=self.neko_api(ctx, "smug"))

    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.slash_command(name="emote-lol", description="Laughing out loud")
    async def lol(self, ctx: disnake.AppCmdInter):
        """
        Sends a laughing image.

        Parameters:
        - ctx (disnake.AppCmdInter): The context object representing the command invocation.

        Returns:
        - None
        """
        await ctx.response.defer()
        await ctx.send(embed=self.neko_api(ctx, "laugh"))

    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.slash_command(name="emote-feed", description="Feed any member")
    async def feed(
        self,
        ctx: disnake.AppCmdInter,
        member: disnake.Member = Param(description="mention a member"),
    ):
        """
        Feed a member.

        Parameters:
        - ctx: The context of the command.
        - member: The member to feed.

        Returns:
        None
        """
        await ctx.response.defer()
        try:
            await ctx.send(embed=self.neko_api(ctx, "feed", f"fed {member.mention}"))
        except commands.MemberNotFound:
            return await ctx.send("Whom to feed?", delete_after=5)


def setup(bot):
    bot.add_cog(Anime(bot))
