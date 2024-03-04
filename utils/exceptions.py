from disnake.ext.commands import CommandError


class NotNeko(CommandError):
    """Exception raised when a neko command is called but the user is not a neko."""

class NoChannelProvided(CommandError):
    """Exception raised when a required channel is not provided."""

class NSFWChannel(CommandError):
    """Exception raised when a non-NSFW channel is used for an NSFW command."""

class NoVote(CommandError):
    """Exception raised when a vote command is called but no vote is provided."""

class NoNeko(CommandError):
    """Exception raised when a neko command is called but no neko is provided."""

class NoVote(CommandError):
    """Exception raised when a vote command is called but no vote is provided."""
