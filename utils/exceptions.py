from disnake.ext.commands import CommandError


class NotNeko(CommandError):
    pass

class NoChannelProvided(CommandError):
    pass


class NSFWChannel(CommandError):
    pass


class NoVote(CommandError):
    pass


class NoNeko(CommandError):
    pass

