from disnake.ext import commands
from disnake.ext.commands.params import Param
import disnake
from typing import Union

from bot import Bot


class Moderator(commands.Cog):
    """
    Commands for control over the server
    """

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.guild_only()
    @commands.slash_command(
        name="mod-channel-purge", description="Purge messages from a channel"
    )
    @commands.has_permissions(
        manage_messages=True, manage_channels=True, manage_roles=True
    )
    @commands.bot_has_permissions(
        manage_messages=True, manage_channels=True, manage_roles=True
    )
    @commands.cooldown(1, 15, commands.BucketType.guild)
    async def purge(
        self,
        ctx: disnake.AppCmdInter,
        amount: int = Param(10, description="No of messages to be purged"),
        member: disnake.Member = Param(
            None, description="Member whose messages to be purged"
        ),
        role: disnake.Role = Param(
            None, description="Role whose messages to be purged"
        ),
    ):
        """
        Purge messages from a channel.

        Parameters:
        - ctx (disnake.AppCmdInter): The context of the command.
        - amount (int): Number of messages to be purged (default: 10).
        - member (disnake.Member): Member whose messages to be purged (default: None).
        - role (disnake.Role): Role whose messages to be purged (default: None).
        """
        specify = ""
        if not role is None and not member is None:
            specify = f"{role.mention} & {member.mention}"

            def check(msg):
                return role in msg.author.roles or msg.author == member

        if not member is None and role is None:
            specify = f"{member.mention}"

            def check(msg):
                return msg.author == member

        if not role is None and member is None:
            specify = f"{role.mention}"

            def check(msg):
                return role in msg.author.roles

        if member is None and role is None:
            specify = f"{ctx.guild.default_role.mention}"

            def check(msg):
                return True

        purged = await ctx.channel.purge(limit=amount, check=check)

        embed = self.bot.Embed(self.bot, ctx, "Purged")
        embed.title = "Purged"
        embed.description = (
            f"{self.bot.icons['passed']} Purged {len(purged)} messages by {specify}"
        )
        embed.colour = 53759
        embed.set_footer(
            text=f"Moderator : {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url,
        )

        await ctx.send(embed=embed, delete_after=3)

    @commands.guild_only()
    @commands.slash_command(name="mod-channel-nuke", description="Nuke a channel")
    @commands.has_permissions(manage_messages=True, manage_channels=True)
    @commands.bot_has_permissions(manage_messages=True, manage_channels=True)
    @commands.cooldown(1, 15, commands.BucketType.guild)
    async def nuke(
        self,
        ctx: disnake.AppCmdInter,
        channel: disnake.TextChannel = Param(None, description="Channel to be nuked"),
    ):
        """
        Nuke a channel.

        Parameters:
        - ctx (disnake.AppCmdInter): The context of the command.
        - channel (disnake.TextChannel): Channel to be nuked (default: None).
        """
        await ctx.response.defer()
        if channel is None:
            channel = ctx.channel
        position = channel.position
        embed = self.bot.Embed(self.bot, ctx, "Nuked")
        embed.title = "Nuked"
        embed.description = "This channel has been nuked"
        new_channel = await channel.clone(reason="Has been Nuked!")
        await new_channel.move(beginning=True, offset=position)
        await channel.delete()
        await new_channel.send(embed=embed)
        try:
            embed = self.bot.Embed(self.bot, ctx, "Nuked")
            embed.title = "Nuked"
            embed.description = f"{new_channel.mention} channel has been nuked"
            await ctx.send(
                embed=embed,
                delete_after=4,
            )
        except:
            pass

    @commands.guild_only()
    @commands.slash_command(name="mod-channel-lock", description="Lock a channel")
    @commands.has_permissions(manage_channels=True, manage_roles=True)
    @commands.bot_has_permissions(manage_channels=True, manage_roles=True)
    @commands.cooldown(1, 15, commands.BucketType.guild)
    async def lock(
        self,
        ctx: disnake.AppCmdInter,
        channel: Union[
            disnake.CategoryChannel, disnake.VoiceChannel, disnake.TextChannel
        ] = Param(None, description="Channel to lock"),
        member: disnake.Member = Param(None, description="Member to lock for"),
        role: disnake.Role = Param(None, description="Role to lock for"),
    ):
        """
        Lock a channel.

        Parameters:
        - ctx (disnake.AppCmdInter): The context of the command.
        - channel (Union[disnake.CategoryChannel, disnake.VoiceChannel, disnake.TextChannel]): Channel to lock (default: None).
        - member (disnake.Member): Member to lock for (default: None).
        - role (disnake.Role): Role to lock for (default: None).
        """
        await ctx.response.defer()
        if channel is None:
            channel = ctx.channel
        await channel.set_permissions(ctx.guild.self_role, send_messages=True)
        await channel.set_permissions(ctx.author, send_messages=True)

        if member is None and role is None:
            specific = f"{ctx.guild.default_role.mention}"
            await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        else:
            specific = ""
            if member:
                specific += f"{member.mention} "
                await channel.set_permissions(member, send_messages=False)
            if role:
                specific += f"{role.mention} "
                await channel.set_permissions(role, send_messages=False)

        embed = self.bot.Embed(self.bot, ctx, "Locked")
        embed.title = "Locked!"
        embed.description = (
            f"{self.bot.icons['lock']} {channel.mention} is now locked for {specific}."
        )
        embed.colour = 53759
        embed.set_footer(
            text=f"Moderator : {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url,
        )
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.slash_command(name="mod-channel-unlock", description="Unlock a channel")
    @commands.has_permissions(manage_channels=True, manage_roles=True)
    @commands.bot_has_permissions(manage_channels=True, manage_roles=True)
    @commands.cooldown(1, 15, commands.BucketType.guild)
    async def unlock(
        self,
        ctx: disnake.AppCmdInter,
        channel: Union[
            disnake.CategoryChannel, disnake.VoiceChannel, disnake.TextChannel
        ] = Param(None, description="Channel to lock"),
        member: disnake.Member = Param(None, description="Member to lock for"),
        role: disnake.Role = Param(None, description="Role to lock for"),
    ):
        """
        Unlock a channel.

        Parameters:
        - ctx (disnake.AppCmdInter): The context of the command.
        - channel (Union[disnake.CategoryChannel, disnake.VoiceChannel, disnake.TextChannel]): Channel to lock (default: None).
        - member (disnake.Member): Member to lock for (default: None).
        - role (disnake.Role): Role to lock for (default: None).
        """
        await ctx.response.defer()
        if channel is None:
            channel = ctx.channel

        if member is None and role is None:
            specific = f"{ctx.guild.default_role.mention}"
            await channel.set_permissions(ctx.guild.default_role, send_messages=True)
        else:
            specific = ""
            if member:
                specific += f"{member.mention} "
                await channel.set_permissions(member, send_messages=True)
            if role:
                specific += f"{role.mention} "
                await channel.set_permissions(role, send_messages=True)
        embed = self.bot.Embed(self.bot, ctx, "Unlocked")
        embed.title = "Unocked!"
        embed.description = f"{self.bot.icons['unlock']} {channel.mention} is now unlocked for {specific}."
        embed.colour = 53759
        embed.set_footer(
            text=f"Moderator : {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url,
        )
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.slash_command(name="mod-channel-hide", description="Hide a channel")
    @commands.has_permissions(manage_channels=True, manage_roles=True)
    @commands.bot_has_permissions(manage_channels=True, manage_roles=True)
    @commands.cooldown(1, 15, commands.BucketType.guild)
    async def hide(
        self,
        ctx: disnake.AppCmdInter,
        channel: Union[
            disnake.CategoryChannel, disnake.VoiceChannel, disnake.TextChannel
        ] = Param(None, description="Channel to hide"),
        member: disnake.Member = Param(None, description="Member to unlock for"),
        role: disnake.Role = Param(None, description="Role to unlock for"),
    ):
        """
        Hide a channel.

        Parameters:
        - ctx (disnake.AppCmdInter): The context of the command.
        - channel (Union[disnake.CategoryChannel, disnake.VoiceChannel, disnake.TextChannel]): Channel to hide (default: None).
        - member (disnake.Member): Member to unlock for (default: None).
        - role (disnake.Role): Role to unlock for (default: None).
        """
        await ctx.response.defer()

        if channel is None:
            channel = ctx.channel

        await channel.set_permissions(ctx.guild.self_role, view_channel=True)
        await channel.set_permissions(ctx.author, view_channel=True)

        if member is None and role is None:
            specific = f"{ctx.guild.default_role.mention}"
            await channel.set_permissions(ctx.guild.default_role, view_channel=False)
        else:
            specific = ""
            if member:
                specific += f"{member.mention} "
                await channel.set_permissions(member, view_channel=False)
            if role:
                specific += f"{role.mention} "
                await channel.set_permissions(role, view_channel=False)

        embed = self.bot.Embed(self.bot, ctx, "Hidden")
        embed.title = "Hidden!"
        embed.description = f"{channel.mention} is now hidden for {specific}."
        embed.colour = 53759
        embed.set_footer(
            text=f"Moderator : {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url,
        )
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.slash_command(name="mod-channel-show", description="Show a channel")
    @commands.has_permissions(manage_channels=True, manage_roles=True)
    @commands.bot_has_permissions(manage_channels=True, manage_roles=True)
    @commands.cooldown(1, 15, commands.BucketType.guild)
    async def show(
        self,
        ctx: disnake.AppCmdInter,
        channel: Union[
            disnake.CategoryChannel, disnake.VoiceChannel, disnake.TextChannel
        ] = Param(None, description="Channel to show"),
        member: disnake.Member = Param(None, description="Member to unlock for"),
        role: disnake.Role = Param(None, description="Role to unlock for"),
    ):
        """
        Show a channel.

        Parameters:
        - ctx (disnake.AppCmdInter): The context of the command.
        - channel (Union[disnake.CategoryChannel, disnake.VoiceChannel, disnake.TextChannel]): Channel to show (default: None).
        - member (disnake.Member): Member to unlock for (default: None).
        - role (disnake.Role): Role to unlock for (default: None).
        """
        await ctx.response.defer()

        if channel is None:
            channel = ctx.channel

        if member is None and role is None:
            specific = f"{ctx.guild.default_role.mention}"
            await channel.set_permissions(ctx.guild.default_role, view_channel=True)
        else:
            specific = ""
            if member:
                specific += f"{member.mention} "
                await channel.set_permissions(member, view_channel=True)
            if role:
                specific += f"{role.mention} "
                await channel.set_permissions(role, view_channel=True)

        embed = self.bot.Embed(self.bot, ctx, "Visible")
        embed.title = "Visible!"
        embed.description = f"{channel.mention} is now visible for {specific}."
        embed.colour = 53759
        embed.set_footer(
            text=f"Moderator : {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url,
        )
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.slash_command(name="mod-kick", description="Kick a member")
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1, 15, commands.BucketType.guild)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(
        self,
        ctx: disnake.AppCmdInter,
        member: disnake.Member = Param(description="Member to kick"),
        reason: str = Param("Not specified", description="Reason for kick"),
    ):
        """
        Kicks a member from the server.

        Parameters:
        - ctx (disnake.AppCmdInter): The context of the command.
        - member (disnake.Member): The member to be kicked.
        - reason (str): The reason for the kick. Default is "Not specified".
        """
        await ctx.response.defer()
        embed = self.bot.Embed(self.bot, ctx, "Kicked")
        embed.title = "Kicked!"
        embed.description = (
            f"{self.bot.icons['moderator']} Kicked `{member}` with reason **{reason}**"
        )
        embed.colour = 53759
        embed.set_footer(
            text=f"Moderator : {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url,
        )

        embed_dm = self.bot.Embed(self.bot, ctx, "Kicked")
        embed_dm.title = ("Kicked!",)
        embed_dm.description = (
            f"You have been kicked from `{ctx.guild.name}` for **{reason}**",
        )
        embed_dm.set_footer(
            text=f"Moderator : {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url,
        )
        if member == ctx.author:
            await ctx.send(
                embed=disnake.Embed(
                    description="This drunken guy wants to kick themselves! Bring him some lemonade"
                ),
                delete_after=3,
            )
        else:
            try:
                await member.send(embed=embed_dm)
            except:
                pass
            await member.kick(reason=reason)
            await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.slash_command(name="mod-ban", description="Ban a member")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.cooldown(1, 15, commands.BucketType.guild)
    async def ban(
        self,
        ctx: disnake.AppCmdInter,
        member: disnake.User = Param(description="Member to ban"),
        reason: str = Param("Not specified!", description="Reason for ban"),
    ):
        """
        Bans a member from the server.

        Parameters:
        - ctx (disnake.AppCmdInter): The context of the command.
        - member (disnake.User): The member to ban.
        - reason (str): The reason for the ban. Default is "Not specified!".

        Returns:
        None
        """
        await ctx.response.defer()

        embed = self.bot.Embed(self.bot, ctx, "Banned")
        embed.title = "Banned!"
        embed.description = (
            f"{self.bot.icons['moderator']} Banned `{member}` with reason **{reason}**"
        )
        embed.colour = 53759
        embed.set_footer(
            text=f"Moderator : {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url,
        )

        embed_dm = self.bot.Embed(self.bot, ctx, "Banned")
        embed_dm.title = ("Banned!",)
        embed_dm.description = (
            f"You have been banned from `{ctx.guild.name}` for **{reason}**",
        )
        embed_dm.set_footer(
            text=f"Moderator : {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url,
        )
        if member == ctx.author:
            await ctx.send(
                embed=disnake.Embed(description="Mad? Banning yourselves?"),
                delete_after=3,
            )
        else:
            try:
                await member.send(embed=embed_dm)
            except:
                pass
            await ctx.guild.ban(user=member, reason=reason)
            await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.slash_command(name="mod-unban", description="Unban a member")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.cooldown(1, 15, commands.BucketType.guild)
    async def unban(
        self,
        ctx: disnake.AppCmdInter,
        member: str = Param(description="UserID to unban"),
        reason: str = Param("Not specified!", description="Reason for unban"),
    ):
        """
        Unbans a user from the server.

        Parameters:
        - ctx (disnake.AppCmdInter): The context of the command.
        - member (disnake.User): The user to unban.
        - reason (str): The reason for the unban. Defaults to "Not specified!".

        Returns:
        None
        """
        await ctx.response.defer()
        try:
            member = int(member)
        except:
            raise commands.BadArgument("Invalid member ID")
        member = await self.bot.get_or_fetch_user(int(member))
        embed = self.bot.Embed(self.bot, ctx, "Unbanned")
        embed.title = "Ban Revoked!"
        embed.description = f"{self.bot.icons['moderator']} Unbanned `{member}` with reason **{reason}**"
        embed.colour = 53759
        embed.set_footer(
            text=f"Moderator : {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url,
        )

        embed_dm = self.bot.Embed(self.bot, ctx, "Unbanned")
        embed_dm.title = "Ban Revoked!"
        embed_dm.description = (
            f"You have been unbanned from `{ctx.guild.name}` for **{reason}**"
        )
        embed_dm.set_footer(
            text=f"Moderator : {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url,
        )

        try:
            await member.send(embed=embed_dm)
        except:
            pass
        await ctx.guild.unban(user=member, reason=reason)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.slash_command(name="mod-timeout", description="Timeout/Mute a member")
    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    @commands.cooldown(1, 15, commands.BucketType.guild)
    async def timeout(
        self,
        ctx: disnake.AppCmdInter,
        member: disnake.Member = Param(description="User to mute"),
        until: int = Param(
            description="For minutes to mute (max 40300 mins or 28 days)"
        ),
        reason: str = Param("Not specified!", description="Reason for timeout"),
    ):
        """
        Timeout a member for a specified duration.

        Parameters:
        - ctx (disnake.AppCmdInter): The context of the command.
        - member (disnake.Member): The member to be timed out.
        - until (int): The duration of the timeout in minutes.
        - reason (str): The reason for the timeout.

        Returns:
        None
        """
        await ctx.response.defer()
        if until > 40300:
            raise commands.BadArgument("Timeout duration cannot exceed 40300 minutes")

        await member.timeout(duration=(until * 60), reason=reason)
        if until != 0:
            embed = self.bot.Embed(self.bot, ctx, "Timed-out!")
            embed.title = "Timed-out!"
            embed.description = f"{self.bot.icons['moderator']} Timed-out `{member}` with reason **{reason}** until {until} minute(s)."
            embed.colour = 53759

            embed_dm = self.bot.Embed(self.bot, ctx, "Timed-out!")
            embed_dm.title = "Timed-out!"
            embed_dm.description = (
                f"You have been timed-out in `{ctx.guild.name}` for **{reason}**"
            )
        else:
            embed = self.bot.Embed(self.bot, ctx, "Timed-out Removed!")
            embed.title = "Time-out Removed!"
            embed.description = f"{self.bot.icons['moderator']} Time-out removed for `{member}` with reason **{reason}**."
            embed.colour = 53759

            embed_dm = self.bot.Embed(self.bot, ctx, "Time-out Removed!")
            embed_dm.title = "Timed-out Removed!"
            embed_dm.description = f"Your time-out has been removed in `{ctx.guild.name}` for **{reason}**."

        embed.set_footer(
            text=f"Moderator : {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url,
        )

        embed_dm.set_footer(
            text=f"Moderator : {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url,
        )
        if member == ctx.author:
            await ctx.send(
                embed=disnake.Embed(
                    description=f"{self.bot.icons['failed']} Cannot time out yourselves."
                ),
                delete_after=3,
            )
        else:
            try:
                await member.send(embed=embed_dm)
            except:
                pass
            await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.slash_command(name="mod-poll", description="Create a poll")
    @commands.has_permissions(manage_guild=True)
    async def poll(
        self,
        ctx: disnake.AppCmdInter,
        question=Param(description="Question of poll"),
        options: str = Param(description="Poll options"),
    ):
        """
        Create a poll.

        Parameters:
        - ctx (disnake.AppCmdInter): The context of the command.
        - question (str): The question of the poll.
        - options (str): The options for the poll.

        Returns:
        None
        """
        await ctx.response.defer()
        options = options.split(",")
        if len(options) <= 1:
            await ctx.send(
                embed=disnake.Embed(
                    description="You need more than one option to make a poll!"
                )
            )
            return
        if len(options) > 10:
            await ctx.send(
                embed=disnake.Embed(
                    description="You cannot make a poll for more than 10 things!"
                )
            )
            return

        if (
            len(options) == 2
            and options[0].lower().replace(" ", "") == "yes"
            and options[1].lower().replace(" ", "") == "no"
        ):
            reactions = [f"{self.bot.icons['like']}", f"{self.bot.icons['dislike']}"]
        else:
            reactions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        description = []
        for x, option in enumerate(options):
            description += f"\n{reactions[x]} {option}\n"
        embed = self.bot.Embed(self.bot, ctx, "Poll")
        embed.title = question
        embed.description = "".join(description)
        embed.color = disnake.Colour.random()

        await ctx.send(embed=embed)
        msg = await ctx.original_message()
        for reaction in reactions[: len(options)]:
            await msg.add_reaction(reaction)


def setup(bot):
    bot.add_cog(Moderator(bot))
