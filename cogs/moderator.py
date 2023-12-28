from disnake.ext import commands
from disnake.ext.commands.params import Param
import disnake
import datetime as dt
from bot import Bot
from typing import Union


class Moderator(commands.Cog):
    """
    Commands for control over the server
    """

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.guild_only()
    @commands.slash_command(
        name="channel-purge", description="Purge messages from a channel"
    )
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    @commands.cooldown(1, 15, commands.BucketType.guild)
    async def purge(
        self,
        ctx: disnake.AppCmdInter,
        amount: int = Param(10, description="No of messages to be purged"),
        member: disnake.Member = Param(
            None, description="Member whose messages to be purged"
        ),
    ):
        if not member is None:
            specify = f"{member.mention}"

            def check(msg):
                return msg.author == member

        else:
            specify = f"{ctx.guild.default_role.mention}"

            def check(msg):
                return True

        purged = await ctx.channel.purge(limit=amount, check=check)

        embed = disnake.Embed(
            title="Purged",
            description=f"{self.bot.icons['passed']} Purged {len(purged)} messages by {specify}",
            colour=53759,
            timestamp=dt.datetime.now(dt.timezone.utc),
        )
        embed.set_author(
            name=self.bot.user.display_name, icon_url=f"{self.bot.user.avatar.url}"
        )
        embed.set_footer(
            text=f"Moderator : {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url,
        )

        await ctx.send(embed=embed, delete_after=3)

    @commands.guild_only()
    @commands.slash_command(name="channel-nuke", description="Nuke a channel")
    @commands.has_permissions(manage_messages=True, manage_channels=True)
    @commands.bot_has_permissions(manage_messages=True, manage_channels=True)
    @commands.cooldown(1, 15, commands.BucketType.guild)
    async def nuke(
        self,
        ctx: disnake.AppCmdInter,
        channel: disnake.TextChannel = Param(None, description="Channel to be nuked"),
    ):
        await ctx.response.defer()
        if channel is None:
            channel = ctx.channel
        position = channel.position
        embed = self.bot.Embed(self.bot, ctx, "Nuked")
        embed.title = "Nuked"
        embed.description = "This channel has been nuked"
        embed.timestamp = dt.datetime.now(dt.timezone.utc)
        new_channel = await channel.clone(reason="Has been Nuked!")
        await new_channel.move(beginning = True, offset = position)
        await channel.delete()
        await new_channel.send(embed=embed)
        try:
            await ctx.send(
                embed=disnake.Embed(description=f"Nuked {new_channel.mention} sucessfully!"),
                delete_after=4,
            )
        except:
            pass

    @commands.guild_only()
    @commands.slash_command(name="channel-lock", description="Lock a channel")
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
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

        embed = disnake.Embed(
            title="Locked!",
            description=f"{self.bot.icons['lock']} {channel.mention} is now locked for {specific}.",
            colour=53759,
            timestamp=dt.datetime.now(dt.timezone.utc),
        )
        embed.set_author(
            name=self.bot.user.display_name, icon_url=f"{self.bot.user.avatar.url}"
        )
        embed.set_footer(
            text=f"Moderator : {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url,
        )
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.slash_command(name="channel-unlock", description="Unlock a channel")
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
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
        embed = disnake.Embed(
            title="Unocked!",
            description=f"{self.bot.icons['unlock']} {channel.mention} is now unlocked for {specific}.",
            colour=53759,
            timestamp=dt.datetime.now(dt.timezone.utc),
        )
        embed.set_author(
            name=self.bot.user.display_name, icon_url=f"{self.bot.user.avatar.url}"
        )
        embed.set_footer(
            text=f"Moderator : {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url,
        )
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.slash_command(name="channel-hide", description="Hide a channel")
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
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
        await ctx.response.defer()

        if channel is None:
            channel = ctx.channel

        await channel.set_permissions(ctx.guild.self_role, view_channel=True)
        await channel.set_permissions(ctx.author, view_channel=True)

        if member is None and role is None:
            specific = f"{ctx.guild.default_role.mention}"
            await channel.set_permissions(
                ctx.guild.default_role, view_channel=False
            )
        else:
            specific = ""
            if member:
                specific += f"{member.mention} "
                await channel.set_permissions(member, view_channel=False)
            if role:
                specific += f"{role.mention} "
                await channel.set_permissions(role, view_channel=False)

        embed = disnake.Embed(
            title="Hidden!",
            description=f"{channel.mention} is now hidden for {specific}.",
            colour=53759,
            timestamp=dt.datetime.now(dt.timezone.utc),
        )
        embed.set_author(
            name=self.bot.user.display_name, icon_url=f"{self.bot.user.avatar.url}"
        )
        embed.set_footer(
            text=f"Moderator : {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url,
        )
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.slash_command(name="channel-show", description="Show a channel")
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
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
        embed = disnake.Embed(
            title="Visible!",
            description=f"{channel.mention} is now visible for {specific}.",
            colour=53759,
            timestamp=dt.datetime.now(dt.timezone.utc),
        )
        embed.set_author(
            name=self.bot.user.display_name, icon_url=f"{self.bot.user.avatar.url}"
        )
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
        reason=Param("Not specified", description="Reason for kick"),
    ):
        await ctx.response.defer()
        embed = disnake.Embed(
            title="Kicked!",
            description=f"{self.bot.icons['moderator']} Kicked `{member}` with reason **{reason}**",
            colour=53759,
            timestamp=dt.datetime.now(dt.timezone.utc),
        )
        embed.set_author(
            name=self.bot.user.display_name, icon_url=f"{self.bot.user.avatar.url}"
        )
        embed.set_footer(
            text=f"Moderator : {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url,
        )

        embed_dm = disnake.Embed(
            title="Kicked!",
            description=f"You have been kicked from `{ctx.guild.name}` for **{reason}**",
        )
        embed_dm.set_author(
            name=self.bot.user.display_name, icon_url=f"{self.bot.user.avatar.url}"
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
        reason=Param("Not specified!", description="Reason for ban"),
    ):
        await ctx.response.defer()

        embed = disnake.Embed(
            title="Banned!",
            description=f"{self.bot.icons['moderator']} Banned `{member}` with reason **{reason}**",
            colour=53759,
            timestamp=dt.datetime.now(dt.timezone.utc),
        )
        embed.set_author(
            name=self.bot.user.display_name, icon_url=f"{self.bot.user.avatar.url}"
        )
        embed.set_footer(
            text=f"Moderator : {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url,
        )

        embed_dm = disnake.Embed(
            title="Banned!",
            description=f"You have been banned from `{ctx.guild.name}` for **{reason}**",
        )
        embed_dm.set_author(
            name=self.bot.user.display_name, icon_url=f"{self.bot.user.avatar.url}"
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
        member: disnake.User = Param(description="User to unban"),
        reason=Param("Not specified!", description="Reason for unban"),
    ):
        await ctx.response.defer()
        embed = disnake.Embed(
            title="Ban Revoked!",
            description=f"{self.bot.icons['moderator']} Unbanned `{member}` with reason **{reason}**",
            colour=53759,
            timestamp=dt.datetime.now(dt.timezone.utc),
        )
        embed.set_author(
            name=self.bot.user.display_name, icon_url=f"{self.bot.user.avatar.url}"
        )
        embed.set_footer(
            text=f"Moderator : {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url,
        )

        embed_dm = disnake.Embed(
            title="Ban Revoked!",
            description=f"You have been unbanned from `{ctx.guild.name}` for **{reason}**",
        )
        embed_dm.set_author(
            name=self.bot.user.display_name, icon_url=f"{self.bot.user.avatar.url}"
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
        until: int = Param(description="For minutes to mute"),
        reason="Not specified",
    ):
        await ctx.response.defer()
        await member.timeout(duration=(until * 60), reason=reason)
        if until != 0:
            embed = disnake.Embed(
                title="Timed-out!",
                description=f"{self.bot.icons['moderator']} Timed-out `{member}` with reason **{reason}** until {until} minute(s).",
                colour=53759,
                timestamp=dt.datetime.now(dt.timezone.utc),
            )
        
            embed_dm = disnake.Embed(
            title="Timed-out!",
            description=f"You have been timed-out in `{ctx.guild.name}` for **{reason}**",
            )
        else:
            embed = disnake.Embed(
                title="Time-out Removed!",
                description=f"{self.bot.icons['moderator']} Time-out removed for `{member}` with reason **{reason}**.",
                colour=53759,
                timestamp=dt.datetime.now(dt.timezone.utc),
            )
        
            embed_dm = disnake.Embed(
            title="Timed-out!",
            description=f"Your time-out has been removed in `{ctx.guild.name}` for **{reason}**.",
            timestamp=dt.datetime.now(dt.timezone.utc),
            )

        embed.set_author(
            name=self.bot.user.display_name, icon_url=f"{self.bot.user.avatar.url}"
        )
        embed.set_footer(
            text=f"Moderator : {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url,
        )

        embed_dm.set_author(
            name=self.bot.user.display_name, icon_url=f"{self.bot.user.avatar.url}"
        )
        embed_dm.set_footer(
            text=f"Moderator : {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url,
        )
        if member == ctx.author:
            await ctx.send(
                embed=disnake.Embed(description=f"{self.bot.icons['failed']} Cannot time out yourselves."),
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
    @commands.slash_command(description="Create a poll")
    @commands.has_permissions(manage_guild=True)
    async def poll(
        self,
        ctx: disnake.AppCmdInter,
        question=Param(description="Question of poll"),
        options: str = Param(description="Poll options"),
    ):
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
            reactions = ["1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣", "9⃣", "🔟"]
        description = []
        for x, option in enumerate(options):
            description += f"\n{reactions[x]} {option}\n"
        embed = disnake.Embed(
            title=question,
            description="".join(description),
            color=disnake.Colour.random(),
        )
        embed.set_footer(text=f"Poll by {ctx.author.name}")
        await ctx.send(embed=embed)
        msg = await ctx.original_message()
        for reaction in reactions[: len(options)]:
            await msg.add_reaction(reaction)


def setup(bot):
    bot.add_cog(Moderator(bot))
