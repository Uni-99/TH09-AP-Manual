# Object classes from AP that represent different types of options that you can create
from Options import Option, FreeText, NumericOption, Toggle, DefaultOnToggle, Choice, TextChoice, Range, NamedRange, OptionGroup, PerGameCommonOptions
# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, get_option_value
from typing import Type, Any


####################################################################
# NOTE: At the time that options are created, Manual has no concept of the multiworld or its own world.
#       Options are defined before the world is even created.
#
# Example of creating your own option:
#
#   class MakeThePlayerOP(Toggle):
#       """Should the player be overpowered? Probably not, but you can choose for this to do... something!"""
#       display_name = "Make me OP"
#
#   options["make_op"] = MakeThePlayerOP
#
#
# Then, to see if the option is set, you can call is_option_enabled or get_option_value.
#####################################################################


# To add an option, use the before_options_defined hook below and something like this:
#   options["total_characters_to_win_with"] = TotalCharactersToWinWith
#
class GameMode(Choice):
    """Which mode would you like to play on?
    Story Mode: Played in story mode. Restart from stage 1 if you die more times than you have life items. Clear stage 9 to receive ending items.
    Match Mode: Played in match mode vs computers. Survive a specified amount of time against opponents. Defeat final opponents to receive ending items."""
    display_name = "game mode"
    option_story_mode = 0
    option_match_mode = 1
    default = 0

class MatchRandom(Toggle):
    """[Match Mode] Should character opponents be randomized? If false, characters you fight will be ordered similar to story mode."""
    display_name = "random match opponents"
    default = 0

class EndingsRequired(Range):
    """How many ending items should be required to goal?"""
    display_name = "endings to goal"
    range_start = 1
    range_end = 16
    default = 1

class StoryDifficultyMid(Choice):
    """[Story Mode] Should life items be required to make stage 6, 7 and 8 in-logic?
    3 Lives: 1 life item makes stage 6 in-logic, 2 life items for stage 7, 3 life items for stage 8.
    2 Lives: 1 life item makes stage 6 in-logic, 2 life items for stage 7 and 8.
    1 Life: 1 life item makes all 3 stages in-logic.
    None: All 3 stages are in-logic without the need of life items."""
    display_name = "story mid game lives"
    option_3_lives = 3
    option_2_lives = 2
    option_1_life = 1
    option_none = 0
    default = 3

class StoryDifficultyEnd(Range):
    """[Story Mode] How many life items should be required to make stage 9 in-logic?"""
    display_name = "story end game lives"
    range_start = 1
    range_end = 7
    default = 6

class MatchDifficultyMinimum(Choice):
    """[Match Mode] What should be the minimum required survival time to make opponents in-logic?"""
    display_name = "match minimum time"
    option_4_minutes = 4
    option_3_minutes = 3
    option_2_minutes = 2
    option_1_minute = 1
    default = 2

class MatchDifficultyBase(Choice):
    """[Match Mode] Increase base survival time?
    By default, 1 minute is the shortest time for starting opponents and the shortest possible time for final opponents.
    match_difficulty_minimum may need to be increased to compensate."""
    display_name = "match base time"
    option_add_2_minutes = 2
    option_add_1_minute = 1
    option_default = 0
    default = 0

class AyaMediDifficulty(Toggle):
    """Should Aya and Medicine require any of their progressive items to make their locations in-logic?"""
    display_name = "aya and medicine progression"
    default = 1

# This is called before any manual options are defined, in case you want to define your own with a clean slate or let Manual define over them
def before_options_defined(options: dict[str, Type[Option[Any]]]) -> dict[str, Type[Option[Any]]]:
    # options["game_mode"] = GameMode
    # options["match_random"] = MatchRandom
    # options["endings_required"] = EndingsRequired
    # options["story_difficulty_mid"] = StoryDifficultyMid
    # options["story_difficulty_end"] = StoryDifficultyEnd
    # options["match_difficulty_minimum"] = MatchDifficultyMinimum
    # options["match_difficulty_base"] = MatchDifficultyBase
    # options["ayamedi_difficulty"] = AyaMediDifficulty
    return options

# This is called after any manual options are defined, in case you want to see what options are defined or want to modify the defined options
def after_options_defined(options: Type[PerGameCommonOptions]):
    # To access a modifiable version of options check the dict in options.type_hints
    # For example if you want to change DLC_enabled's display name you would do:
    # options.type_hints["DLC_enabled"].display_name = "New Display Name"

    #  Here's an example on how to add your aliases to the generated goal
    # options.type_hints['goal'].aliases.update({"example": 0, "second_alias": 1})
    # options.type_hints['goal'].options.update({"example": 0, "second_alias": 1})  #for an alias to be valid it must also be in options

    pass

# Use this Hook if you want to add your Option to an Option group (existing or not)
def before_option_groups_created(groups: dict[str, list[Type[Option[Any]]]]) -> dict[str, list[Type[Option[Any]]]]:
    # Uses the format groups['GroupName'] = [TotalCharactersToWinWith]
    return groups

def after_option_groups_created(groups: list[OptionGroup]) -> list[OptionGroup]:
    return groups
