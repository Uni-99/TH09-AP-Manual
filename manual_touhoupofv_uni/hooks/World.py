# Object classes from AP core, to represent an entire MultiWorld and this individual World that's part of it
from worlds.AutoWorld import World
from BaseClasses import MultiWorld, CollectionState, Item

# Object classes from Manual -- extending AP core -- representing items and locations that are used in generation
from ..Items import ManualItem
from ..Locations import ManualLocation

# Raw JSON data from the Manual apworld, respectively:
#          data/game.json, data/items.json, data/locations.json, data/regions.json
#
from ..Data import game_table, item_table, location_table, region_table

# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, get_option_value, format_state_prog_items_key, ProgItemsCat

# calling logging.info("message") anywhere below in this file will output the message to both console and log file
import logging

########################################################################################
## Order of method calls when the world generates:
##    1. create_regions - Creates regions and locations
##    2. create_items - Creates the item pool
##    3. set_rules - Creates rules for accessing regions and locations
##    4. generate_basic - Runs any post item pool options, like place item/category
##    5. pre_fill - Creates the victory location
##
## The create_item method is used by plando and start_inventory settings to create an item from an item name.
## The fill_slot_data method will be used to send data to the Manual client for later use, like deathlink.
########################################################################################

# Use this function to change the valid filler items to be created to replace item links or starting items.
# Default value is the `filler_item_name` from game.json
def hook_get_filler_item_name(world: World, multiworld: MultiWorld, player: int) -> str | bool:
    return False

# Called before regions and locations are created. Not clear why you'd want this, but it's here. Victory location is included, but Victory event is not placed yet.
def before_create_regions(world: World, multiworld: MultiWorld, player: int):
    pass

# Called after regions and locations are created, in case you want to see or modify that information. Victory location is included.
def after_create_regions(world: World, multiworld: MultiWorld, player: int):

    # Getting option values
    game_mode = get_option_value(multiworld, player, "game_mode")
    character_items = get_option_value(multiworld, player, "character_items")
    match_random_opponents = get_option_value(multiworld, player, "match_random_opponents")

    match_base_time = get_option_value(multiworld, player, "match_base_time")

    random_enabled_characters = get_option_value(multiworld, player, "random_enabled_characters")
    enable_reimu = get_option_value(multiworld, player, "enable_reimu")
    enable_marisa = get_option_value(multiworld, player, "enable_marisa")
    enable_sakuya = get_option_value(multiworld, player, "enable_sakuya")
    enable_youmu = get_option_value(multiworld, player, "enable_youmu")
    enable_reisen = get_option_value(multiworld, player, "enable_reisen")
    enable_cirno = get_option_value(multiworld, player, "enable_cirno")
    enable_lyrica = get_option_value(multiworld, player, "enable_lyrica")
    enable_mystia = get_option_value(multiworld, player, "enable_mystia")
    enable_tewi = get_option_value(multiworld, player, "enable_tewi")
    enable_aya = get_option_value(multiworld, player, "enable_aya")
    enable_medicine = get_option_value(multiworld, player, "enable_medicine")
    enable_yuuka = get_option_value(multiworld, player, "enable_yuuka")
    enable_komachi = get_option_value(multiworld, player, "enable_komachi")
    enable_shikieiki = get_option_value(multiworld, player, "enable_shikieiki")
    enable_merlin = get_option_value(multiworld, player, "enable_merlin")
    enable_lunasa = get_option_value(multiworld, player, "enable_lunasa")

    characters = ["Reimu", "Marisa", "Sakuya", "Youmu", "Reisen", "Cirno", "Lyrica", "Merlin", "Lunasa", "Mystia", "Tewi", "Aya", "Medicine", "Yuuka", "Komachi", "Shikieiki"]

    d_char = characters.copy()
    if enable_reimu: d_char.remove("Reimu")
    if enable_marisa: d_char.remove("Marisa")
    if enable_sakuya: d_char.remove("Sakuya")
    if enable_youmu: d_char.remove("Youmu")
    if enable_reisen: d_char.remove("Reisen")
    if enable_cirno: d_char.remove("Cirno")
    if enable_lyrica: d_char.remove("Lyrica")
    if enable_merlin and game_mode: d_char.remove("Merlin")
    if enable_lunasa and game_mode: d_char.remove("Lunasa")
    if enable_mystia: d_char.remove("Mystia")
    if enable_tewi: d_char.remove("Tewi")
    if enable_aya: d_char.remove("Aya")
    if enable_medicine: d_char.remove("Medicine")
    if enable_yuuka: d_char.remove("Yuuka")
    if enable_komachi: d_char.remove("Komachi")
    if enable_shikieiki: d_char.remove("Shikieiki")

    e_char = characters.copy()
    if not enable_reimu: e_char.remove("Reimu")
    if not enable_marisa: e_char.remove("Marisa")
    if not enable_sakuya: e_char.remove("Sakuya")
    if not enable_youmu: e_char.remove("Youmu")
    if not enable_reisen: e_char.remove("Reisen")
    if not enable_cirno: e_char.remove("Cirno")
    if not enable_lyrica: e_char.remove("Lyrica")
    if not enable_merlin or not game_mode: e_char.remove("Merlin")
    if not enable_lunasa or not game_mode: e_char.remove("Lunasa")
    if not enable_mystia: e_char.remove("Mystia")
    if not enable_tewi: e_char.remove("Tewi")
    if not enable_aya: e_char.remove("Aya")
    if not enable_medicine: e_char.remove("Medicine")
    if not enable_yuuka: e_char.remove("Yuuka")
    if not enable_komachi: e_char.remove("Komachi")
    if not enable_shikieiki: e_char.remove("Shikieiki")

    world.d_char = d_char.copy() # List of player disabled characters
    world.e_char = e_char.copy() # List of player enabled characters

    # UT support for randomness
    if hasattr(multiworld, "generation_is_fake") and hasattr(multiworld, "re_gen_passthrough"):
        if world.game in multiworld.re_gen_passthrough:
            slot_data = multiworld.re_gen_passthrough[world.game]

            if game_mode: world.character_matchups = slot_data["character_matchups"]
            if len(world.e_char) > random_enabled_characters and random_enabled_characters != 0: world.in_pool_characters = slot_data["in_pool_characters"]
    else:
        # Letting the randomizer choose which character to disable if enabled characters are more than random_enabled_characters option value
        if len(world.e_char) > random_enabled_characters and random_enabled_characters != 0:
            random_choice = world.e_char.copy()
            world.random.shuffle(random_choice)

            while len(random_choice) > random_enabled_characters:
                random_choice.pop()
            for p1 in world.e_char:
                if p1 not in random_choice: e_char.remove(p1)

        world.in_pool_characters = e_char # List of randomizer enabled characters

        # Character matchups for match mode
        if game_mode:
            world.character_matchups = {}
            
            if match_random_opponents: # Randomize character matchups if match_random_opponents option is enabled
                char_mu_random = {}
                for p1 in e_char:
                    char_mu_random[p1] = characters.copy()
                    world.random.shuffle(char_mu_random[p1])
                    while len(char_mu_random[p1]) > 9: char_mu_random[p1].pop()
                world.character_matchups = char_mu_random
            else:
                # Imitate matchups from story mode if match_random_opponents option is disabled
                story_opponents = {}
                def story_opps():
                    world.character_matchups[p1].append(sm)
                    story_opponents[p1].remove(sm)

                for p1 in e_char:
                    world.character_matchups[p1] = []
                    story_opponents[p1] = characters.copy()
                    world.random.shuffle(story_opponents[p1])
                    for stage in range (1, 10):
                        for sm in story_opponents[p1]:
                            match stage:
                                # Stage 1 Opponents
                                case 1 if p1 != "Cirno" and p1 != "Lyrica" and p1 != "Merlin" and p1 != "Lunasa" and p1 != "Mystia" and p1 != "Medicine" and p1 != "Komachi":
                                    if sm == "Cirno" or sm == "Mystia":
                                        story_opps()
                                        break
                                case 1 if p1 == "Cirno":
                                    if sm == "Mystia":
                                        story_opps()
                                        break
                                case 1 if p1 == "Lyrica" or p1 == "Merlin" or p1 == "Lunasa" or p1 == "Mystia" or p1 == "Komachi":
                                    if sm == "Cirno":
                                        story_opps()
                                        break
                                case 1 if p1 == "Medicine":
                                    if sm == "Mystia" or sm == "Lyrica":
                                        story_opps()
                                        break
                                # Stage 2 Opponents
                                case 2 if p1 != "Cirno" and p1 != "Lyrica" and p1 != "Merlin" and p1 != "Lunasa" and p1 != "Mystia" and p1 != "Tewi" and p1 != "Medicine" and p1 != "Komachi":
                                    if sm == "Cirno" or sm == "Mystia" or sm == "Lyrica":
                                        story_opps()
                                        break
                                case 2 if p1 == "Cirno":
                                    if sm == "Lyrica":
                                        story_opps()
                                        break
                                case 2 if p1 == "Lyrica" or p1 == "Merlin" or p1 == "Lunasa":
                                    if sm == "Mystia" or sm == "Tewi":
                                        story_opps()
                                        break
                                case 2 if p1 == "Mystia":
                                    if sm == "Tewi" or sm == "Lyrica":
                                        story_opps()
                                        break
                                case 2 if p1 == "Tewi":
                                    if sm == "Cirno" or sm == "Mystia":
                                        story_opps()
                                        break
                                case 2 if p1 == "Medicine":
                                    if sm == "Mystia" or sm == "Lyrica":
                                        story_opps()
                                        break
                                case 2 if p1 == "Komachi":
                                    if sm == "Tewi" or sm == "Reisen":
                                        story_opps()
                                        break
                                # Stage 3 Opponents
                                case 3 if p1 == "Reimu" or p1 == "Reisen":
                                    if sm == "Lyrica" or sm == "Tewi":
                                        story_opps()
                                        break
                                case 3 if p1 == "Marisa" or p1 == "Mystia" or p1 == "Shikieiki":
                                    if sm == "Lyrica" or sm == "Tewi" or sm == "Reisen" or sm == "Youmu":
                                        story_opps()
                                        break
                                case 3 if p1 == "Sakuya":
                                    if sm == "Lyrica" or sm == "Youmu" or sm == "Reisen":
                                        story_opps()
                                        break
                                case 3 if p1 == "Youmu":
                                    if sm == "Mystia" or sm == "Lyrica" or sm == "Tewi" or sm == "Reimu" or sm == "Marisa":
                                        story_opps()
                                        break
                                case 3 if p1 == "Cirno":
                                    if sm == "Marisa" or sm == "Sakuya" or sm == "Tewi":
                                        story_opps()
                                        break
                                case 3 if p1 == "Lyrica" or p1 == "Merlin" or p1 == "Lunasa":
                                    if sm == "Mystia" or sm == "Tewi" or sm == "Reisen":
                                        story_opps()
                                        break
                                case 3 if p1 == "Tewi":
                                    if sm == "Sakuya" or sm == "Lyrica":
                                        story_opps()
                                        break
                                case 3 if p1 == "Aya":
                                    if sm == "Lyrica" or sm == "Tewi" or sm == "Reimu" or sm == "Sakuya":
                                        story_opps()
                                        break
                                case 3 if p1 == "Medicine":
                                    if sm == "Tewi":
                                        story_opps()
                                        break
                                case 3 if p1 == "Yuuka":
                                    if sm == "Lyrica" or sm == "Tewi" or sm == "Marisa" or sm == "Sakuya" or sm == "Youmu" or sm == "Reisen":
                                        story_opps()
                                        break
                                case 3 if p1 == "Komachi":
                                    if sm == "Sakuya":
                                        story_opps()
                                        break
                                # Stage 4 Opponents
                                case 4 if p1 == "Reimu":
                                    if sm == "Lyrica" or sm == "Tewi" or sm == "Reisen":
                                        story_opps()
                                        break
                                case 4 if p1 == "Marisa" or p1 == "Mystia":
                                    if sm == "Lyrica" or sm == "Tewi" or sm == "Reisen" or sm == "Youmu":
                                        story_opps()
                                        break
                                case 4 if p1 == "Sakuya":
                                    if sm == "Lyrica" or sm == "Youmu" or sm == "Reisen" or sm == "Reimu" or sm == "Marisa":
                                        story_opps()
                                        break
                                case 4 if p1 == "Youmu":
                                    if sm == "Lyrica" or sm == "Tewi" or sm == "Reimu" or sm == "Marisa" or sm == "Reisen":
                                        story_opps()
                                        break
                                case 4 if p1 == "Reisen":
                                    if sm == "Lyrica" or sm == "Tewi" or sm == "Reimu" or sm == "Marisa" or sm == "Youmu":
                                        story_opps()
                                        break
                                case 4 if p1 == "Cirno":
                                    if sm == "Marisa" or sm == "Sakuya" or sm == "Tewi" or sm == "Reimu" or sm == "Youmu":
                                        story_opps()
                                        break
                                case 4 if p1 == "Lyrica" or p1 == "Merlin" or p1 == "Lunasa":
                                    if sm == "Tewi" or sm == "Reisen" or sm == "Reimu" or sm == "Marisa" or sm == "Sakuya":
                                        story_opps()
                                        break
                                case 4 if p1 == "Tewi":
                                    if sm == "Lyrica" or sm == "Marisa" or sm == "Youmu":
                                        story_opps()
                                        break
                                case 4 if p1 == "Aya":
                                    if sm == "Tewi" or sm == "Reimu" or sm == "Sakuya" or sm == "Youmu" or sm == "Reisen":
                                        story_opps()
                                        break
                                case 4 if p1 == "Medicine":
                                    if sm == "Reimu" or sm == "Marisa" or sm == "Reisen":
                                        story_opps()
                                        break
                                case 4 if p1 == "Yuuka":
                                    if sm == "Tewi" or sm == "Marisa" or sm == "Sakuya" or sm == "Youmu" or sm == "Reisen":
                                        story_opps()
                                        break
                                case 4 if p1 == "Komachi" or p1 == "Shikieiki":
                                    if sm == "Tewi" or sm == "Reisen" or sm == "Youmu":
                                        story_opps()
                                        break
                                # Stage 5 Opponents
                                case 5 if p1 == "Reimu" or p1 == "Yuuka":
                                    if sm == "Reisen" or sm == "Youmu" or sm == "Marisa" or sm == "Sakuya":
                                        story_opps()
                                        break
                                case 5 if p1 == "Marisa":
                                    if sm == "Reisen" or sm == "Youmu" or sm == "Reimu" or sm == "Sakuya":
                                        story_opps()
                                        break
                                case 5 if p1 == "Sakuya":
                                    if sm == "Youmu" or sm == "Reisen" or sm == "Reimu" or sm == "Marisa":
                                        story_opps()
                                        break
                                case 5 if p1 == "Youmu" or p1 == "Medicine":
                                    if sm == "Reimu" or sm == "Marisa" or sm == "Reisen":
                                        story_opps()
                                        break
                                case 5 if p1 == "Reisen":
                                    if sm == "Reimu" or sm == "Marisa" or sm == "Youmu":
                                        story_opps()
                                        break
                                case 5 if p1 == "Cirno":
                                    if sm == "Marisa" or sm == "Sakuya" or sm == "Tewi" or sm == "Reimu" or sm == "Youmu":
                                        story_opps()
                                        break
                                case 5 if p1 == "Lyrica" or p1 == "Merlin" or p1 == "Lunasa":
                                    if sm == "Reimu" or sm == "Marisa" or sm == "Sakuya":
                                        story_opps()
                                        break
                                case 5 if p1 == "Mystia":
                                    if sm == "Marisa" or sm == "Sakuya":
                                        story_opps()
                                        break
                                case 5 if p1 == "Tewi":
                                    if sm == "Sakuya" or sm == "Marisa" or sm == "Youmu" or sm == "Reimu":
                                        story_opps()
                                        break
                                case 5 if p1 == "Aya":
                                    if sm == "Tewi" or sm == "Reimu" or sm == "Sakuya" or sm == "Youmu" or sm == "Reisen":
                                        story_opps()
                                        break
                                case 5 if p1 == "Komachi":
                                    if sm == "Tewi" or sm == "Reisen" or sm == "Youmu":
                                        story_opps()
                                        break
                                case 5 if p1 == "Shikieiki":
                                    if sm == "Youmu" or sm == "Reisen" or sm == "Sakuya":
                                        story_opps()
                                        break
                                # Stage 6 Opponents
                                case 6 if p1 == "Reimu":
                                    if sm == "Marisa" or sm == "Sakuya":
                                        story_opps()
                                        break
                                case 6 if p1 == "Marisa":
                                    if sm == "Reimu" or sm == "Sakuya":
                                        story_opps()
                                        break
                                case 6 if p1 == "Sakuya":
                                    if sm == "Tewi":
                                        story_opps()
                                        break
                                case 6 if p1 == "Youmu" or p1 == "Reisen" or p1 == "Medicine":
                                    if sm == "Sakuya":
                                        story_opps()
                                        break
                                case 6 if p1 == "Cirno" or p1 == "Tewi":
                                    if sm == "Reisen":
                                        story_opps()
                                        break
                                case 6 if p1 == "Lyrica" or p1 == "Merlin" or p1 == "Lunasa":
                                    if sm == "Youmu":
                                        story_opps()
                                        break
                                case 6 if p1 == "Mystia" or p1 == "Yuuka":
                                    if sm == "Reimu":
                                        story_opps()
                                        break
                                case 6 if p1 == "Aya" or p1 == "Komachi" or p1 == "Shikieiki":
                                    if sm == "Marisa":
                                        story_opps()
                                        break
                                # Stage 7 Opponents
                                case 7 if p1 != "Sakuya" and p1 != "Reisen" and p1 != "Mystia" and p1 != "Tewi" and p1 != "Aya" and p1 != "Medicine" and p1 != "Komachi":
                                    if sm == "Aya":
                                        story_opps()
                                        break
                                case 7 if p1 == "Sakuya" or p1 == "Reisen" or p1 == "Mystia" or p1 == "Tewi" or p1 == "Aya":
                                    if sm == "Medicine":
                                        story_opps()
                                        break
                                case 7 if p1 == "Medicine" or p1 == "Komachi":
                                    if sm == "Yuuka":
                                        story_opps()
                                        break
                                # Stage 8 Opponents
                                case 8 if p1 != "Cirno" and p1 != "Lyrica" and p1 != "Merlin" and p1 != "Lunasa" and p1 != "Mystia" and p1 != "Komachi":
                                    if sm == "Komachi":
                                        story_opps()
                                        break
                                case 8 if p1 == "Cirno" or p1 == "Lyrica" or p1 == "Merlin" or p1 == "Lunasa" or p1 == "Mystia":
                                    if sm == "Yuuka":
                                        story_opps()
                                        break
                                case 8 if p1 == "Komachi":
                                    if sm == "Reimu":
                                        story_opps()
                                        break
                                # Stage 9 Opponents
                                case 9 if p1 != "Shikieiki":
                                    if sm == "Shikieiki":
                                        story_opps()
                                        break
                                case 9 if p1 == "Shikieiki":
                                    if sm == "Reimu":
                                        story_opps()
                                        break

    # in_pool_characters stays as list of player enabled characters if enabled characters is not more than random_enabled_characters
    if len(world.e_char) <= random_enabled_characters or random_enabled_characters == 0: world.in_pool_characters = e_char

    # Choosing locations not to remove
    locationNamesToKeep: list[str] = ["Incident Resolved"] # List of location names

    if not game_mode:
        for p1 in world.in_pool_characters:
            for i in range(1, 10): locationNamesToKeep.append(f"[{p1}] Stage {i}")
    else:
        p2mu = {}

        time1 = f"{1 + match_base_time} Minutes"
        if time1 == "1 Minutes": time1 = "1 Minute"
        if character_items:
            time2 = f"{2 + match_base_time} Minutes"
            time3 = f"{4 + match_base_time} Minutes"
            time4 = f"{6 + match_base_time} Minutes"
            time5 = f"{8 + match_base_time} Minutes"
        else:
            time2 = f"{3 + match_base_time} Minutes"
            time3 = f"{5 + match_base_time} Minutes"
            time4 = f"{7 + match_base_time} Minutes"
            time5 = f"{9 + match_base_time} Minutes"

        for p1 in world.in_pool_characters:
            p2mu[p1 + "_m1p2"], p2mu[p1 + "_m2p2"], p2mu[p1 + "_m3p2"], p2mu[p1 + "_m4p2"] = world.character_matchups[p1][:4]
            p2mu[p1 + "_m5p2"], p2mu[p1 + "_m6p2"], p2mu[p1 + "_m7p2"], p2mu[p1 + "_m8p2"], p2mu[p1 + "_m9p2"] = world.character_matchups[p1][4:]
            locationNamesToKeep.append(f"[{p1}] VS {p2mu[p1 + "_m1p2"]} - {time1}")
            locationNamesToKeep.append(f"[{p1}] VS {p2mu[p1 + "_m2p2"]} - {time1}")
            locationNamesToKeep.append(f"[{p1}] VS {p2mu[p1 + "_m3p2"]} - {time2}")
            locationNamesToKeep.append(f"[{p1}] VS {p2mu[p1 + "_m4p2"]} - {time2}")
            locationNamesToKeep.append(f"[{p1}] VS {p2mu[p1 + "_m5p2"]} - {time3}")
            locationNamesToKeep.append(f"[{p1}] VS {p2mu[p1 + "_m6p2"]} - {time3}")
            locationNamesToKeep.append(f"[{p1}] VS {p2mu[p1 + "_m7p2"]} - {time4}")
            locationNamesToKeep.append(f"[{p1}] VS {p2mu[p1 + "_m8p2"]} - {time4}")
            locationNamesToKeep.append(f"[{p1}] Finale: VS {p2mu[p1 + "_m9p2"]} - {time5}")

    # Add your code here to calculate which locations to remove
    for region in multiworld.regions:
        if region.player == player:
            for location in list(region.locations):
                if location.name not in locationNamesToKeep:
                    region.locations.remove(location)

# This hook allows you to access the item names & counts before the items are created. Use this to increase/decrease the amount of a specific item in the pool
# Valid item_config key/values:
# {"Item Name": 5} <- This will create qty 5 items using all the default settings
# {"Item Name": {"useful": 7}} <- This will create qty 7 items and force them to be classified as useful
# {"Item Name": {"progression": 2, "useful": 1}} <- This will create 3 items, with 2 classified as progression and 1 as useful
# {"Item Name": {0b0110: 5}} <- If you know the special flag for the item classes, you can also define non-standard options. This setup
#       will create 5 items that are the "useful trap" class
# {"Item Name": {ItemClassification.useful: 5}} <- You can also use the classification directly
def before_create_items_all(item_config: dict[str, int|dict], world: World, multiworld: MultiWorld, player: int) -> dict[str, int|dict]:
    return item_config

# The item pool before starting items are processed, in case you want to see the raw item pool at that stage
def before_create_items_starting(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    # Use this hook to remove items from the item pool
    itemNamesToRemove: list[str] = [] # List of item names
    
    # Removing items from characters if they have been disabled by random_enabled_characters option
    game_mode = get_option_value(multiworld, player, "game_mode")
    character_items = get_option_value(multiworld, player, "character_items")
    characters = ["Reimu", "Marisa", "Sakuya", "Youmu", "Reisen", "Cirno", "Lyrica", "Merlin", "Lunasa", "Mystia", "Tewi", "Aya", "Medicine", "Yuuka", "Komachi", "Shikieiki"]
    
    for p1 in characters:
        if p1 not in world.in_pool_characters and p1 not in world.d_char:
            if character_items: itemNamesToRemove.append(f"Character Unlock - {p1}")
            if game_mode == 0:
                for _ in range(8):
                    itemNamesToRemove.append(f"+1 Life - {p1}")
            else:
                for _ in range(8):
                    itemNamesToRemove.append(f"-1 Minute - {p1}")
            itemNamesToRemove.append(f"Ending - {p1}")
        elif p1 not in world.d_char and character_items:
            if game_mode == 0:
                itemNamesToRemove.append(f"+1 Life - {p1}")
            else:
                itemNamesToRemove.append(f"-1 Minute - {p1}")

    for itemName in itemNamesToRemove:
        item = next(i for i in item_pool if i.name == itemName)
        item_pool.remove(item)

    return item_pool

# The item pool after starting items are processed but before filler is added, in case you want to see the raw item pool at that stage
def before_create_items_filler(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    # Use this hook to remove items from the item pool
    itemNamesToRemove: list[str] = [] # List of item names

    # Add your code here to calculate which items to remove.
    #
    # Because multiple copies of an item can exist, you need to add an item name
    # to the list multiple times if you want to remove multiple copies of it.

    for itemName in itemNamesToRemove:
        item = next(i for i in item_pool if i.name == itemName)
        item_pool.remove(item)

    return item_pool

    # Some other useful hook options:

    ## Place an item at a specific location
    # location = next(l for l in multiworld.get_unfilled_locations(player=player) if l.name == "Location Name")
    # item_to_place = next(i for i in item_pool if i.name == "Item Name")
    # location.place_locked_item(item_to_place)
    # item_pool.remove(item_to_place)

# The complete item pool prior to being set for generation is provided here, in case you want to make changes to it
def after_create_items(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    return item_pool

# Called before rules for accessing regions and locations are created. Not clear why you'd want this, but it's here.
def before_set_rules(world: World, multiworld: MultiWorld, player: int):
    pass

# Called after rules for accessing regions and locations are created, in case you want to see or modify that information.
def after_set_rules(world: World, multiworld: MultiWorld, player: int):
    # Use this hook to modify the access rules for a given location

    # Getting option values
    game_mode = get_option_value(multiworld, player, "game_mode")
    endings_required = get_option_value(multiworld, player, "endings_required")
    character_items = get_option_value(multiworld, player, "character_items")

    story_mid_game_lives = get_option_value(multiworld, player, "story_mid_game_lives")
    story_end_game_lives = get_option_value(multiworld, player, "story_end_game_lives")
    match_minimum_time = get_option_value(multiworld, player, "match_minimum_time")
    match_base_time = get_option_value(multiworld, player, "match_base_time")
    ayamedi_progression = get_option_value(multiworld, player, "ayamedi_progression")

    # Character items aren't needed if character_items option is disabled
    if not character_items:
        for region in multiworld.get_regions(player):
            for region_entrance in region.entrances:
                region_entrance.access_rule = lambda state: True
    
    # Goal access rules
    ending = multiworld.get_location("Incident Resolved", player)
    ending.access_rule = lambda state: (state.count_group("Endings", world.player) >= endings_required)

    # Story Mode access rules
    if game_mode == 0:
        early_game = {}
        for p1 in world.in_pool_characters:
            for stage in range(1, 6):
                early_game[f"c{p1}s{stage}"] = world.get_location(f"[{p1}] Stage {stage}")
                early_game[f"c{p1}s{stage}"].access_rule = lambda state: True

        if story_mid_game_lives == 0:
            s6access = 0
            s7access = 0
            s8access = 0
        else:
            s6access = 1
            if story_mid_game_lives == 1:
                s7access = 1
                s8access = 1
            else:
                s7access = 2
                if story_mid_game_lives == 2:
                    s8access = 2
                else:
                    s8access = 3

        if story_mid_game_lives >= story_end_game_lives:
            s9access = story_mid_game_lives + 1
        else:
            s9access = story_end_game_lives

        if "Reimu" in world.in_pool_characters:
            s6reimu = multiworld.get_location("[Reimu] Stage 6", player)
            s7reimu = multiworld.get_location("[Reimu] Stage 7", player)
            s8reimu = multiworld.get_location("[Reimu] Stage 8", player)
            s9reimu = multiworld.get_location("[Reimu] Stage 9", player)
            s6reimu.access_rule = lambda state: (state.count("+1 Life - Reimu", world.player) >= s6access)
            s7reimu.access_rule = lambda state: (state.count("+1 Life - Reimu", world.player) >= s7access)
            s8reimu.access_rule = lambda state: (state.count("+1 Life - Reimu", world.player) >= s8access)
            s9reimu.access_rule = lambda state: (state.count("+1 Life - Reimu", world.player) >= s9access)
        if "Marisa" in world.in_pool_characters:
            s6marisa = multiworld.get_location("[Marisa] Stage 6", player)
            s7marisa = multiworld.get_location("[Marisa] Stage 7", player)
            s8marisa = multiworld.get_location("[Marisa] Stage 8", player)
            s9marisa = multiworld.get_location("[Marisa] Stage 9", player)
            s6marisa.access_rule = lambda state: (state.count("+1 Life - Marisa", world.player) >= s6access)
            s7marisa.access_rule = lambda state: (state.count("+1 Life - Marisa", world.player) >= s7access)
            s8marisa.access_rule = lambda state: (state.count("+1 Life - Marisa", world.player) >= s8access)
            s9marisa.access_rule = lambda state: (state.count("+1 Life - Marisa", world.player) >= s9access)
        if "Sakuya" in world.in_pool_characters:
            s6sakuya = multiworld.get_location("[Sakuya] Stage 6", player)
            s7sakuya = multiworld.get_location("[Sakuya] Stage 7", player)
            s8sakuya = multiworld.get_location("[Sakuya] Stage 8", player)
            s9sakuya = multiworld.get_location("[Sakuya] Stage 9", player)
            s6sakuya.access_rule = lambda state: (state.count("+1 Life - Sakuya", world.player) >= s6access)
            s7sakuya.access_rule = lambda state: (state.count("+1 Life - Sakuya", world.player) >= s7access)
            s8sakuya.access_rule = lambda state: (state.count("+1 Life - Sakuya", world.player) >= s8access)
            s9sakuya.access_rule = lambda state: (state.count("+1 Life - Sakuya", world.player) >= s9access)
        if "Youmu" in world.in_pool_characters:
            s6youmu = multiworld.get_location("[Youmu] Stage 6", player)
            s7youmu = multiworld.get_location("[Youmu] Stage 7", player)
            s8youmu = multiworld.get_location("[Youmu] Stage 8", player)
            s9youmu = multiworld.get_location("[Youmu] Stage 9", player)
            s6youmu.access_rule = lambda state: (state.count("+1 Life - Youmu", world.player) >= s6access)
            s7youmu.access_rule = lambda state: (state.count("+1 Life - Youmu", world.player) >= s7access)
            s8youmu.access_rule = lambda state: (state.count("+1 Life - Youmu", world.player) >= s8access)
            s9youmu.access_rule = lambda state: (state.count("+1 Life - Youmu", world.player) >= s9access)
        if "Reisen" in world.in_pool_characters:
            s6reisen = multiworld.get_location("[Reisen] Stage 6", player)
            s7reisen = multiworld.get_location("[Reisen] Stage 7", player)
            s8reisen = multiworld.get_location("[Reisen] Stage 8", player)
            s9reisen = multiworld.get_location("[Reisen] Stage 9", player)
            s6reisen.access_rule = lambda state: (state.count("+1 Life - Reisen", world.player) >= s6access)
            s7reisen.access_rule = lambda state: (state.count("+1 Life - Reisen", world.player) >= s7access)
            s8reisen.access_rule = lambda state: (state.count("+1 Life - Reisen", world.player) >= s8access)
            s9reisen.access_rule = lambda state: (state.count("+1 Life - Reisen", world.player) >= s9access)
        if "Cirno" in world.in_pool_characters:
            s6cirno = multiworld.get_location("[Cirno] Stage 6", player)
            s7cirno = multiworld.get_location("[Cirno] Stage 7", player)
            s8cirno = multiworld.get_location("[Cirno] Stage 8", player)
            s9cirno = multiworld.get_location("[Cirno] Stage 9", player)
            s6cirno.access_rule = lambda state: (state.count("+1 Life - Cirno", world.player) >= s6access)
            s7cirno.access_rule = lambda state: (state.count("+1 Life - Cirno", world.player) >= s7access)
            s8cirno.access_rule = lambda state: (state.count("+1 Life - Cirno", world.player) >= s8access)
            s9cirno.access_rule = lambda state: (state.count("+1 Life - Cirno", world.player) >= s9access)
        if "Lyrica" in world.in_pool_characters:
            s6lyrica = multiworld.get_location("[Lyrica] Stage 6", player)
            s7lyrica = multiworld.get_location("[Lyrica] Stage 7", player)
            s8lyrica = multiworld.get_location("[Lyrica] Stage 8", player)
            s9lyrica = multiworld.get_location("[Lyrica] Stage 9", player)
            s6lyrica.access_rule = lambda state: (state.count("+1 Life - Lyrica", world.player) >= s6access)
            s7lyrica.access_rule = lambda state: (state.count("+1 Life - Lyrica", world.player) >= s7access)
            s8lyrica.access_rule = lambda state: (state.count("+1 Life - Lyrica", world.player) >= s8access)
            s9lyrica.access_rule = lambda state: (state.count("+1 Life - Lyrica", world.player) >= s9access)
        if "Mystia" in world.in_pool_characters:
            s6mystia = multiworld.get_location("[Mystia] Stage 6", player)
            s7mystia = multiworld.get_location("[Mystia] Stage 7", player)
            s8mystia = multiworld.get_location("[Mystia] Stage 8", player)
            s9mystia = multiworld.get_location("[Mystia] Stage 9", player)
            s6mystia.access_rule = lambda state: (state.count("+1 Life - Mystia", world.player) >= s6access)
            s7mystia.access_rule = lambda state: (state.count("+1 Life - Mystia", world.player) >= s7access)
            s8mystia.access_rule = lambda state: (state.count("+1 Life - Mystia", world.player) >= s8access)
            s9mystia.access_rule = lambda state: (state.count("+1 Life - Mystia", world.player) >= s9access)
        if "Tewi" in world.in_pool_characters:
            s6tewi = multiworld.get_location("[Tewi] Stage 6", player)
            s7tewi = multiworld.get_location("[Tewi] Stage 7", player)
            s8tewi = multiworld.get_location("[Tewi] Stage 8", player)
            s9tewi = multiworld.get_location("[Tewi] Stage 9", player)
            s6tewi.access_rule = lambda state: (state.count("+1 Life - Tewi", world.player) >= s6access)
            s7tewi.access_rule = lambda state: (state.count("+1 Life - Tewi", world.player) >= s7access)
            s8tewi.access_rule = lambda state: (state.count("+1 Life - Tewi", world.player) >= s8access)
            s9tewi.access_rule = lambda state: (state.count("+1 Life - Tewi", world.player) >= s9access)
        if "Aya" in world.in_pool_characters:
            s6aya = multiworld.get_location("[Aya] Stage 6", player)
            s7aya = multiworld.get_location("[Aya] Stage 7", player)
            s8aya = multiworld.get_location("[Aya] Stage 8", player)
            s9aya = multiworld.get_location("[Aya] Stage 9", player)
            if ayamedi_progression == False:
                s6aya.access_rule = lambda state: True
                s7aya.access_rule = lambda state: True
                s8aya.access_rule = lambda state: True
                s9aya.access_rule = lambda state: True
            else:
                s6aya.access_rule = lambda state: (state.count("+1 Life - Aya", world.player) >= s6access)
                s7aya.access_rule = lambda state: (state.count("+1 Life - Aya", world.player) >= s7access)
                s8aya.access_rule = lambda state: (state.count("+1 Life - Aya", world.player) >= s8access)
                s9aya.access_rule = lambda state: (state.count("+1 Life - Aya", world.player) >= s9access)
        if "Medicine" in world.in_pool_characters:
            s6medicine = multiworld.get_location("[Medicine] Stage 6", player)
            s7medicine = multiworld.get_location("[Medicine] Stage 7", player)
            s8medicine = multiworld.get_location("[Medicine] Stage 8", player)
            s9medicine = multiworld.get_location("[Medicine] Stage 9", player)
            if ayamedi_progression == False:
                s6medicine.access_rule = lambda state: True
                s7medicine.access_rule = lambda state: True
                s8medicine.access_rule = lambda state: True
                s9medicine.access_rule = lambda state: True
            else:
                s6medicine.access_rule = lambda state: (state.count("+1 Life - Medicine", world.player) >= s6access)
                s7medicine.access_rule = lambda state: (state.count("+1 Life - Medicine", world.player) >= s7access)
                s8medicine.access_rule = lambda state: (state.count("+1 Life - Medicine", world.player) >= s8access)
                s9medicine.access_rule = lambda state: (state.count("+1 Life - Medicine", world.player) >= s9access)
        if "Yuuka" in world.in_pool_characters:
            s6yuuka = multiworld.get_location("[Yuuka] Stage 6", player)
            s7yuuka = multiworld.get_location("[Yuuka] Stage 7", player)
            s8yuuka = multiworld.get_location("[Yuuka] Stage 8", player)
            s9yuuka = multiworld.get_location("[Yuuka] Stage 9", player)
            s6yuuka.access_rule = lambda state: (state.count("+1 Life - Yuuka", world.player) >= s6access)
            s7yuuka.access_rule = lambda state: (state.count("+1 Life - Yuuka", world.player) >= s7access)
            s8yuuka.access_rule = lambda state: (state.count("+1 Life - Yuuka", world.player) >= s8access)
            s9yuuka.access_rule = lambda state: (state.count("+1 Life - Yuuka", world.player) >= s9access)
        if "Komachi" in world.in_pool_characters:
            s6komachi = multiworld.get_location("[Komachi] Stage 6", player)
            s7komachi = multiworld.get_location("[Komachi] Stage 7", player)
            s8komachi = multiworld.get_location("[Komachi] Stage 8", player)
            s9komachi = multiworld.get_location("[Komachi] Stage 9", player)
            s6komachi.access_rule = lambda state: (state.count("+1 Life - Komachi", world.player) >= s6access)
            s7komachi.access_rule = lambda state: (state.count("+1 Life - Komachi", world.player) >= s7access)
            s8komachi.access_rule = lambda state: (state.count("+1 Life - Komachi", world.player) >= s8access)
            s9komachi.access_rule = lambda state: (state.count("+1 Life - Komachi", world.player) >= s9access)
        if "Shikieiki" in world.in_pool_characters:
            s6shikieiki = multiworld.get_location("[Shikieiki] Stage 6", player)
            s7shikieiki = multiworld.get_location("[Shikieiki] Stage 7", player)
            s8shikieiki = multiworld.get_location("[Shikieiki] Stage 8", player)
            s9shikieiki = multiworld.get_location("[Shikieiki] Stage 9", player)
            s6shikieiki.access_rule = lambda state: (state.count("+1 Life - Shikieiki", world.player) >= s6access)
            s7shikieiki.access_rule = lambda state: (state.count("+1 Life - Shikieiki", world.player) >= s7access)
            s8shikieiki.access_rule = lambda state: (state.count("+1 Life - Shikieiki", world.player) >= s8access)
            s9shikieiki.access_rule = lambda state: (state.count("+1 Life - Shikieiki", world.player) >= s9access)

    # Match Mode access rules
    if game_mode == 1:
        match match_minimum_time:
            case 1: match_timer = 7
            case 2: match_timer = 6
            case 3: match_timer = 5
            case 4: match_timer = 4
        m1access = match_timer + (match_base_time - 7)
        m2access = match_timer + (match_base_time - 6)
        m3access = match_timer + (match_base_time - 4)
        m4access = match_timer + (match_base_time - 2)
        m5access = match_timer + match_base_time

        time1 = f"{1 + match_base_time} Minutes"
        if time1 == "1 Minutes": time1 = "1 Minute"
        if character_items:
            time2 = f"{2 + match_base_time} Minutes"
            time3 = f"{4 + match_base_time} Minutes"
            time4 = f"{6 + match_base_time} Minutes"
            time5 = f"{8 + match_base_time} Minutes"
        else:
            m2access += 1
            m3access += 1
            m4access += 1
            m5access += 1
            time2 = f"{3 + match_base_time} Minutes"
            time3 = f"{5 + match_base_time} Minutes"
            time4 = f"{7 + match_base_time} Minutes"
            time5 = f"{9 + match_base_time} Minutes"

        if "Reimu" in world.in_pool_characters:
            m1p2, m2p2, m3p2, m4p2, m5p2, m6p2, m7p2, m8p2, m9p2 = world.character_matchups["Reimu"]
            m1reimu = multiworld.get_location(f"[Reimu] VS {m1p2} - {time1}", player)
            m2reimu = multiworld.get_location(f"[Reimu] VS {m2p2} - {time1}", player)
            m3reimu = multiworld.get_location(f"[Reimu] VS {m3p2} - {time2}", player)
            m4reimu = multiworld.get_location(f"[Reimu] VS {m4p2} - {time2}", player)
            m5reimu = multiworld.get_location(f"[Reimu] VS {m5p2} - {time3}", player)
            m6reimu = multiworld.get_location(f"[Reimu] VS {m6p2} - {time3}", player)
            m7reimu = multiworld.get_location(f"[Reimu] VS {m7p2} - {time4}", player)
            m8reimu = multiworld.get_location(f"[Reimu] VS {m8p2} - {time4}", player)
            m9reimu = multiworld.get_location(f"[Reimu] Finale: VS {m9p2} - {time5}", player)
            m1reimu.access_rule = lambda state: (state.count("-1 Minute - Reimu", world.player) >= m1access)
            m2reimu.access_rule = lambda state: (state.count("-1 Minute - Reimu", world.player) >= m1access)
            m3reimu.access_rule = lambda state: (state.count("-1 Minute - Reimu", world.player) >= m2access)
            m4reimu.access_rule = lambda state: (state.count("-1 Minute - Reimu", world.player) >= m2access)
            m5reimu.access_rule = lambda state: (state.count("-1 Minute - Reimu", world.player) >= m3access)
            m6reimu.access_rule = lambda state: (state.count("-1 Minute - Reimu", world.player) >= m3access)
            m7reimu.access_rule = lambda state: (state.count("-1 Minute - Reimu", world.player) >= m4access)
            m8reimu.access_rule = lambda state: (state.count("-1 Minute - Reimu", world.player) >= m4access)
            m9reimu.access_rule = lambda state: (state.count("-1 Minute - Reimu", world.player) >= m5access)
        if "Marisa" in world.in_pool_characters:
            m1p2, m2p2, m3p2, m4p2, m5p2, m6p2, m7p2, m8p2, m9p2 = world.character_matchups["Marisa"]
            m1marisa = multiworld.get_location(f"[Marisa] VS {m1p2} - {time1}", player)
            m2marisa = multiworld.get_location(f"[Marisa] VS {m2p2} - {time1}", player)
            m3marisa = multiworld.get_location(f"[Marisa] VS {m3p2} - {time2}", player)
            m4marisa = multiworld.get_location(f"[Marisa] VS {m4p2} - {time2}", player)
            m5marisa = multiworld.get_location(f"[Marisa] VS {m5p2} - {time3}", player)
            m6marisa = multiworld.get_location(f"[Marisa] VS {m6p2} - {time3}", player)
            m7marisa = multiworld.get_location(f"[Marisa] VS {m7p2} - {time4}", player)
            m8marisa = multiworld.get_location(f"[Marisa] VS {m8p2} - {time4}", player)
            m9marisa = multiworld.get_location(f"[Marisa] Finale: VS {m9p2} - {time5}", player)
            m1marisa.access_rule = lambda state: (state.count("-1 Minute - Marisa", world.player) >= m1access)
            m2marisa.access_rule = lambda state: (state.count("-1 Minute - Marisa", world.player) >= m1access)
            m3marisa.access_rule = lambda state: (state.count("-1 Minute - Marisa", world.player) >= m2access)
            m4marisa.access_rule = lambda state: (state.count("-1 Minute - Marisa", world.player) >= m2access)
            m5marisa.access_rule = lambda state: (state.count("-1 Minute - Marisa", world.player) >= m3access)
            m6marisa.access_rule = lambda state: (state.count("-1 Minute - Marisa", world.player) >= m3access)
            m7marisa.access_rule = lambda state: (state.count("-1 Minute - Marisa", world.player) >= m4access)
            m8marisa.access_rule = lambda state: (state.count("-1 Minute - Marisa", world.player) >= m4access)
            m9marisa.access_rule = lambda state: (state.count("-1 Minute - Marisa", world.player) >= m5access)
        if "Sakuya" in world.in_pool_characters:
            m1p2, m2p2, m3p2, m4p2, m5p2, m6p2, m7p2, m8p2, m9p2 = world.character_matchups["Sakuya"]
            m1sakuya = multiworld.get_location(f"[Sakuya] VS {m1p2} - {time1}", player)
            m2sakuya = multiworld.get_location(f"[Sakuya] VS {m2p2} - {time1}", player)
            m3sakuya = multiworld.get_location(f"[Sakuya] VS {m3p2} - {time2}", player)
            m4sakuya = multiworld.get_location(f"[Sakuya] VS {m4p2} - {time2}", player)
            m5sakuya = multiworld.get_location(f"[Sakuya] VS {m5p2} - {time3}", player)
            m6sakuya = multiworld.get_location(f"[Sakuya] VS {m6p2} - {time3}", player)
            m7sakuya = multiworld.get_location(f"[Sakuya] VS {m7p2} - {time4}", player)
            m8sakuya = multiworld.get_location(f"[Sakuya] VS {m8p2} - {time4}", player)
            m9sakuya = multiworld.get_location(f"[Sakuya] Finale: VS {m9p2} - {time5}", player)
            m1sakuya.access_rule = lambda state: (state.count("-1 Minute - Sakuya", world.player) >= m1access)
            m2sakuya.access_rule = lambda state: (state.count("-1 Minute - Sakuya", world.player) >= m1access)
            m3sakuya.access_rule = lambda state: (state.count("-1 Minute - Sakuya", world.player) >= m2access)
            m4sakuya.access_rule = lambda state: (state.count("-1 Minute - Sakuya", world.player) >= m2access)
            m5sakuya.access_rule = lambda state: (state.count("-1 Minute - Sakuya", world.player) >= m3access)
            m6sakuya.access_rule = lambda state: (state.count("-1 Minute - Sakuya", world.player) >= m3access)
            m7sakuya.access_rule = lambda state: (state.count("-1 Minute - Sakuya", world.player) >= m4access)
            m8sakuya.access_rule = lambda state: (state.count("-1 Minute - Sakuya", world.player) >= m4access)
            m9sakuya.access_rule = lambda state: (state.count("-1 Minute - Sakuya", world.player) >= m5access)
        if "Youmu" in world.in_pool_characters:
            m1p2, m2p2, m3p2, m4p2, m5p2, m6p2, m7p2, m8p2, m9p2 = world.character_matchups["Youmu"]
            m1youmu = multiworld.get_location(f"[Youmu] VS {m1p2} - {time1}", player)
            m2youmu = multiworld.get_location(f"[Youmu] VS {m2p2} - {time1}", player)
            m3youmu = multiworld.get_location(f"[Youmu] VS {m3p2} - {time2}", player)
            m4youmu = multiworld.get_location(f"[Youmu] VS {m4p2} - {time2}", player)
            m5youmu = multiworld.get_location(f"[Youmu] VS {m5p2} - {time3}", player)
            m6youmu = multiworld.get_location(f"[Youmu] VS {m6p2} - {time3}", player)
            m7youmu = multiworld.get_location(f"[Youmu] VS {m7p2} - {time4}", player)
            m8youmu = multiworld.get_location(f"[Youmu] VS {m8p2} - {time4}", player)
            m9youmu = multiworld.get_location(f"[Youmu] Finale: VS {m9p2} - {time5}", player)
            m1youmu.access_rule = lambda state: (state.count("-1 Minute - Youmu", world.player) >= m1access)
            m2youmu.access_rule = lambda state: (state.count("-1 Minute - Youmu", world.player) >= m1access)
            m3youmu.access_rule = lambda state: (state.count("-1 Minute - Youmu", world.player) >= m2access)
            m4youmu.access_rule = lambda state: (state.count("-1 Minute - Youmu", world.player) >= m2access)
            m5youmu.access_rule = lambda state: (state.count("-1 Minute - Youmu", world.player) >= m3access)
            m6youmu.access_rule = lambda state: (state.count("-1 Minute - Youmu", world.player) >= m3access)
            m7youmu.access_rule = lambda state: (state.count("-1 Minute - Youmu", world.player) >= m4access)
            m8youmu.access_rule = lambda state: (state.count("-1 Minute - Youmu", world.player) >= m4access)
            m9youmu.access_rule = lambda state: (state.count("-1 Minute - Youmu", world.player) >= m5access)
        if "Reisen" in world.in_pool_characters:
            m1p2, m2p2, m3p2, m4p2, m5p2, m6p2, m7p2, m8p2, m9p2 = world.character_matchups["Reisen"]
            m1reisen = multiworld.get_location(f"[Reisen] VS {m1p2} - {time1}", player)
            m2reisen = multiworld.get_location(f"[Reisen] VS {m2p2} - {time1}", player)
            m3reisen = multiworld.get_location(f"[Reisen] VS {m3p2} - {time2}", player)
            m4reisen = multiworld.get_location(f"[Reisen] VS {m4p2} - {time2}", player)
            m5reisen = multiworld.get_location(f"[Reisen] VS {m5p2} - {time3}", player)
            m6reisen = multiworld.get_location(f"[Reisen] VS {m6p2} - {time3}", player)
            m7reisen = multiworld.get_location(f"[Reisen] VS {m7p2} - {time4}", player)
            m8reisen = multiworld.get_location(f"[Reisen] VS {m8p2} - {time4}", player)
            m9reisen = multiworld.get_location(f"[Reisen] Finale: VS {m9p2} - {time5}", player)
            m1reisen.access_rule = lambda state: (state.count("-1 Minute - Reisen", world.player) >= m1access)
            m2reisen.access_rule = lambda state: (state.count("-1 Minute - Reisen", world.player) >= m1access)
            m3reisen.access_rule = lambda state: (state.count("-1 Minute - Reisen", world.player) >= m2access)
            m4reisen.access_rule = lambda state: (state.count("-1 Minute - Reisen", world.player) >= m2access)
            m5reisen.access_rule = lambda state: (state.count("-1 Minute - Reisen", world.player) >= m3access)
            m6reisen.access_rule = lambda state: (state.count("-1 Minute - Reisen", world.player) >= m3access)
            m7reisen.access_rule = lambda state: (state.count("-1 Minute - Reisen", world.player) >= m4access)
            m8reisen.access_rule = lambda state: (state.count("-1 Minute - Reisen", world.player) >= m4access)
            m9reisen.access_rule = lambda state: (state.count("-1 Minute - Reisen", world.player) >= m5access)
        if "Cirno" in world.in_pool_characters:
            m1p2, m2p2, m3p2, m4p2, m5p2, m6p2, m7p2, m8p2, m9p2 = world.character_matchups["Cirno"]
            m1cirno = multiworld.get_location(f"[Cirno] VS {m1p2} - {time1}", player)
            m2cirno = multiworld.get_location(f"[Cirno] VS {m2p2} - {time1}", player)
            m3cirno = multiworld.get_location(f"[Cirno] VS {m3p2} - {time2}", player)
            m4cirno = multiworld.get_location(f"[Cirno] VS {m4p2} - {time2}", player)
            m5cirno = multiworld.get_location(f"[Cirno] VS {m5p2} - {time3}", player)
            m6cirno = multiworld.get_location(f"[Cirno] VS {m6p2} - {time3}", player)
            m7cirno = multiworld.get_location(f"[Cirno] VS {m7p2} - {time4}", player)
            m8cirno = multiworld.get_location(f"[Cirno] VS {m8p2} - {time4}", player)
            m9cirno = multiworld.get_location(f"[Cirno] Finale: VS {m9p2} - {time5}", player)
            m1cirno.access_rule = lambda state: (state.count("-1 Minute - Cirno", world.player) >= m1access)
            m2cirno.access_rule = lambda state: (state.count("-1 Minute - Cirno", world.player) >= m1access)
            m3cirno.access_rule = lambda state: (state.count("-1 Minute - Cirno", world.player) >= m2access)
            m4cirno.access_rule = lambda state: (state.count("-1 Minute - Cirno", world.player) >= m2access)
            m5cirno.access_rule = lambda state: (state.count("-1 Minute - Cirno", world.player) >= m3access)
            m6cirno.access_rule = lambda state: (state.count("-1 Minute - Cirno", world.player) >= m3access)
            m7cirno.access_rule = lambda state: (state.count("-1 Minute - Cirno", world.player) >= m4access)
            m8cirno.access_rule = lambda state: (state.count("-1 Minute - Cirno", world.player) >= m4access)
            m9cirno.access_rule = lambda state: (state.count("-1 Minute - Cirno", world.player) >= m5access)
        if "Lyrica" in world.in_pool_characters:
            m1p2, m2p2, m3p2, m4p2, m5p2, m6p2, m7p2, m8p2, m9p2 = world.character_matchups["Lyrica"]
            m1lyrica = multiworld.get_location(f"[Lyrica] VS {m1p2} - {time1}", player)
            m2lyrica = multiworld.get_location(f"[Lyrica] VS {m2p2} - {time1}", player)
            m3lyrica = multiworld.get_location(f"[Lyrica] VS {m3p2} - {time2}", player)
            m4lyrica = multiworld.get_location(f"[Lyrica] VS {m4p2} - {time2}", player)
            m5lyrica = multiworld.get_location(f"[Lyrica] VS {m5p2} - {time3}", player)
            m6lyrica = multiworld.get_location(f"[Lyrica] VS {m6p2} - {time3}", player)
            m7lyrica = multiworld.get_location(f"[Lyrica] VS {m7p2} - {time4}", player)
            m8lyrica = multiworld.get_location(f"[Lyrica] VS {m8p2} - {time4}", player)
            m9lyrica = multiworld.get_location(f"[Lyrica] Finale: VS {m9p2} - {time5}", player)
            m1lyrica.access_rule = lambda state: (state.count("-1 Minute - Lyrica", world.player) >= m1access)
            m2lyrica.access_rule = lambda state: (state.count("-1 Minute - Lyrica", world.player) >= m1access)
            m3lyrica.access_rule = lambda state: (state.count("-1 Minute - Lyrica", world.player) >= m2access)
            m4lyrica.access_rule = lambda state: (state.count("-1 Minute - Lyrica", world.player) >= m2access)
            m5lyrica.access_rule = lambda state: (state.count("-1 Minute - Lyrica", world.player) >= m3access)
            m6lyrica.access_rule = lambda state: (state.count("-1 Minute - Lyrica", world.player) >= m3access)
            m7lyrica.access_rule = lambda state: (state.count("-1 Minute - Lyrica", world.player) >= m4access)
            m8lyrica.access_rule = lambda state: (state.count("-1 Minute - Lyrica", world.player) >= m4access)
            m9lyrica.access_rule = lambda state: (state.count("-1 Minute - Lyrica", world.player) >= m5access)
        if "Merlin" in world.in_pool_characters:
            m1p2, m2p2, m3p2, m4p2, m5p2, m6p2, m7p2, m8p2, m9p2 = world.character_matchups["Merlin"]
            m1merlin = multiworld.get_location(f"[Merlin] VS {m1p2} - {time1}", player)
            m2merlin = multiworld.get_location(f"[Merlin] VS {m2p2} - {time1}", player)
            m3merlin = multiworld.get_location(f"[Merlin] VS {m3p2} - {time2}", player)
            m4merlin = multiworld.get_location(f"[Merlin] VS {m4p2} - {time2}", player)
            m5merlin = multiworld.get_location(f"[Merlin] VS {m5p2} - {time3}", player)
            m6merlin = multiworld.get_location(f"[Merlin] VS {m6p2} - {time3}", player)
            m7merlin = multiworld.get_location(f"[Merlin] VS {m7p2} - {time4}", player)
            m8merlin = multiworld.get_location(f"[Merlin] VS {m8p2} - {time4}", player)
            m9merlin = multiworld.get_location(f"[Merlin] Finale: VS {m9p2} - {time5}", player)
            m1merlin.access_rule = lambda state: (state.count("-1 Minute - Merlin", world.player) >= m1access)
            m2merlin.access_rule = lambda state: (state.count("-1 Minute - Merlin", world.player) >= m1access)
            m3merlin.access_rule = lambda state: (state.count("-1 Minute - Merlin", world.player) >= m2access)
            m4merlin.access_rule = lambda state: (state.count("-1 Minute - Merlin", world.player) >= m2access)
            m5merlin.access_rule = lambda state: (state.count("-1 Minute - Merlin", world.player) >= m3access)
            m6merlin.access_rule = lambda state: (state.count("-1 Minute - Merlin", world.player) >= m3access)
            m7merlin.access_rule = lambda state: (state.count("-1 Minute - Merlin", world.player) >= m4access)
            m8merlin.access_rule = lambda state: (state.count("-1 Minute - Merlin", world.player) >= m4access)
            m9merlin.access_rule = lambda state: (state.count("-1 Minute - Merlin", world.player) >= m5access)
        if "Lunasa" in world.in_pool_characters:
            m1p2, m2p2, m3p2, m4p2, m5p2, m6p2, m7p2, m8p2, m9p2 = world.character_matchups["Lunasa"]
            m1lunasa = multiworld.get_location(f"[Lunasa] VS {m1p2} - {time1}", player)
            m2lunasa = multiworld.get_location(f"[Lunasa] VS {m2p2} - {time1}", player)
            m3lunasa = multiworld.get_location(f"[Lunasa] VS {m3p2} - {time2}", player)
            m4lunasa = multiworld.get_location(f"[Lunasa] VS {m4p2} - {time2}", player)
            m5lunasa = multiworld.get_location(f"[Lunasa] VS {m5p2} - {time3}", player)
            m6lunasa = multiworld.get_location(f"[Lunasa] VS {m6p2} - {time3}", player)
            m7lunasa = multiworld.get_location(f"[Lunasa] VS {m7p2} - {time4}", player)
            m8lunasa = multiworld.get_location(f"[Lunasa] VS {m8p2} - {time4}", player)
            m9lunasa = multiworld.get_location(f"[Lunasa] Finale: VS {m9p2} - {time5}", player)
            m1lunasa.access_rule = lambda state: (state.count("-1 Minute - Lunasa", world.player) >= m1access)
            m2lunasa.access_rule = lambda state: (state.count("-1 Minute - Lunasa", world.player) >= m1access)
            m3lunasa.access_rule = lambda state: (state.count("-1 Minute - Lunasa", world.player) >= m2access)
            m4lunasa.access_rule = lambda state: (state.count("-1 Minute - Lunasa", world.player) >= m2access)
            m5lunasa.access_rule = lambda state: (state.count("-1 Minute - Lunasa", world.player) >= m3access)
            m6lunasa.access_rule = lambda state: (state.count("-1 Minute - Lunasa", world.player) >= m3access)
            m7lunasa.access_rule = lambda state: (state.count("-1 Minute - Lunasa", world.player) >= m4access)
            m8lunasa.access_rule = lambda state: (state.count("-1 Minute - Lunasa", world.player) >= m4access)
            m9lunasa.access_rule = lambda state: (state.count("-1 Minute - Lunasa", world.player) >= m5access)
        if "Mystia" in world.in_pool_characters:
            m1p2, m2p2, m3p2, m4p2, m5p2, m6p2, m7p2, m8p2, m9p2 = world.character_matchups["Mystia"]
            m1mystia = multiworld.get_location(f"[Mystia] VS {m1p2} - {time1}", player)
            m2mystia = multiworld.get_location(f"[Mystia] VS {m2p2} - {time1}", player)
            m3mystia = multiworld.get_location(f"[Mystia] VS {m3p2} - {time2}", player)
            m4mystia = multiworld.get_location(f"[Mystia] VS {m4p2} - {time2}", player)
            m5mystia = multiworld.get_location(f"[Mystia] VS {m5p2} - {time3}", player)
            m6mystia = multiworld.get_location(f"[Mystia] VS {m6p2} - {time3}", player)
            m7mystia = multiworld.get_location(f"[Mystia] VS {m7p2} - {time4}", player)
            m8mystia = multiworld.get_location(f"[Mystia] VS {m8p2} - {time4}", player)
            m9mystia = multiworld.get_location(f"[Mystia] Finale: VS {m9p2} - {time5}", player)
            m1mystia.access_rule = lambda state: (state.count("-1 Minute - Mystia", world.player) >= m1access)
            m2mystia.access_rule = lambda state: (state.count("-1 Minute - Mystia", world.player) >= m1access)
            m3mystia.access_rule = lambda state: (state.count("-1 Minute - Mystia", world.player) >= m2access)
            m4mystia.access_rule = lambda state: (state.count("-1 Minute - Mystia", world.player) >= m2access)
            m5mystia.access_rule = lambda state: (state.count("-1 Minute - Mystia", world.player) >= m3access)
            m6mystia.access_rule = lambda state: (state.count("-1 Minute - Mystia", world.player) >= m3access)
            m7mystia.access_rule = lambda state: (state.count("-1 Minute - Mystia", world.player) >= m4access)
            m8mystia.access_rule = lambda state: (state.count("-1 Minute - Mystia", world.player) >= m4access)
            m9mystia.access_rule = lambda state: (state.count("-1 Minute - Mystia", world.player) >= m5access)
        if "Tewi" in world.in_pool_characters:
            m1p2, m2p2, m3p2, m4p2, m5p2, m6p2, m7p2, m8p2, m9p2 = world.character_matchups["Tewi"]
            m1tewi = multiworld.get_location(f"[Tewi] VS {m1p2} - {time1}", player)
            m2tewi = multiworld.get_location(f"[Tewi] VS {m2p2} - {time1}", player)
            m3tewi = multiworld.get_location(f"[Tewi] VS {m3p2} - {time2}", player)
            m4tewi = multiworld.get_location(f"[Tewi] VS {m4p2} - {time2}", player)
            m5tewi = multiworld.get_location(f"[Tewi] VS {m5p2} - {time3}", player)
            m6tewi = multiworld.get_location(f"[Tewi] VS {m6p2} - {time3}", player)
            m7tewi = multiworld.get_location(f"[Tewi] VS {m7p2} - {time4}", player)
            m8tewi = multiworld.get_location(f"[Tewi] VS {m8p2} - {time4}", player)
            m9tewi = multiworld.get_location(f"[Tewi] Finale: VS {m9p2} - {time5}", player)
            m1tewi.access_rule = lambda state: (state.count("-1 Minute - Tewi", world.player) >= m1access)
            m2tewi.access_rule = lambda state: (state.count("-1 Minute - Tewi", world.player) >= m1access)
            m3tewi.access_rule = lambda state: (state.count("-1 Minute - Tewi", world.player) >= m2access)
            m4tewi.access_rule = lambda state: (state.count("-1 Minute - Tewi", world.player) >= m2access)
            m5tewi.access_rule = lambda state: (state.count("-1 Minute - Tewi", world.player) >= m3access)
            m6tewi.access_rule = lambda state: (state.count("-1 Minute - Tewi", world.player) >= m3access)
            m7tewi.access_rule = lambda state: (state.count("-1 Minute - Tewi", world.player) >= m4access)
            m8tewi.access_rule = lambda state: (state.count("-1 Minute - Tewi", world.player) >= m4access)
            m9tewi.access_rule = lambda state: (state.count("-1 Minute - Tewi", world.player) >= m5access)
        if "Aya" in world.in_pool_characters:
            m1p2, m2p2, m3p2, m4p2, m5p2, m6p2, m7p2, m8p2, m9p2 = world.character_matchups["Aya"]
            m1aya = multiworld.get_location(f"[Aya] VS {m1p2} - {time1}", player)
            m2aya = multiworld.get_location(f"[Aya] VS {m2p2} - {time1}", player)
            m3aya = multiworld.get_location(f"[Aya] VS {m3p2} - {time2}", player)
            m4aya = multiworld.get_location(f"[Aya] VS {m4p2} - {time2}", player)
            m5aya = multiworld.get_location(f"[Aya] VS {m5p2} - {time3}", player)
            m6aya = multiworld.get_location(f"[Aya] VS {m6p2} - {time3}", player)
            m7aya = multiworld.get_location(f"[Aya] VS {m7p2} - {time4}", player)
            m8aya = multiworld.get_location(f"[Aya] VS {m8p2} - {time4}", player)
            m9aya = multiworld.get_location(f"[Aya] Finale: VS {m9p2} - {time5}", player)
            if ayamedi_progression == False:
                m1aya.access_rule = lambda state: True
                m2aya.access_rule = lambda state: True
                m3aya.access_rule = lambda state: True
                m4aya.access_rule = lambda state: True
                m5aya.access_rule = lambda state: True
                m6aya.access_rule = lambda state: True
                m7aya.access_rule = lambda state: True
                m8aya.access_rule = lambda state: True
                m9aya.access_rule = lambda state: True
            else:
                m1aya.access_rule = lambda state: (state.count("-1 Minute - Aya", world.player) >= m1access)
                m2aya.access_rule = lambda state: (state.count("-1 Minute - Aya", world.player) >= m1access)
                m3aya.access_rule = lambda state: (state.count("-1 Minute - Aya", world.player) >= m2access)
                m4aya.access_rule = lambda state: (state.count("-1 Minute - Aya", world.player) >= m2access)
                m5aya.access_rule = lambda state: (state.count("-1 Minute - Aya", world.player) >= m3access)
                m6aya.access_rule = lambda state: (state.count("-1 Minute - Aya", world.player) >= m3access)
                m7aya.access_rule = lambda state: (state.count("-1 Minute - Aya", world.player) >= m4access)
                m8aya.access_rule = lambda state: (state.count("-1 Minute - Aya", world.player) >= m4access)
                m9aya.access_rule = lambda state: (state.count("-1 Minute - Aya", world.player) >= m5access)
        if "Medicine" in world.in_pool_characters:
            m1p2, m2p2, m3p2, m4p2, m5p2, m6p2, m7p2, m8p2, m9p2 = world.character_matchups["Medicine"]
            m1medicine = multiworld.get_location(f"[Medicine] VS {m1p2} - {time1}", player)
            m2medicine = multiworld.get_location(f"[Medicine] VS {m2p2} - {time1}", player)
            m3medicine = multiworld.get_location(f"[Medicine] VS {m3p2} - {time2}", player)
            m4medicine = multiworld.get_location(f"[Medicine] VS {m4p2} - {time2}", player)
            m5medicine = multiworld.get_location(f"[Medicine] VS {m5p2} - {time3}", player)
            m6medicine = multiworld.get_location(f"[Medicine] VS {m6p2} - {time3}", player)
            m7medicine = multiworld.get_location(f"[Medicine] VS {m7p2} - {time4}", player)
            m8medicine = multiworld.get_location(f"[Medicine] VS {m8p2} - {time4}", player)
            m9medicine = multiworld.get_location(f"[Medicine] Finale: VS {m9p2} - {time5}", player)
            if ayamedi_progression == False:
                m1medicine.access_rule = lambda state: True
                m2medicine.access_rule = lambda state: True
                m3medicine.access_rule = lambda state: True
                m4medicine.access_rule = lambda state: True
                m5medicine.access_rule = lambda state: True
                m6medicine.access_rule = lambda state: True
                m7medicine.access_rule = lambda state: True
                m8medicine.access_rule = lambda state: True
                m9medicine.access_rule = lambda state: True
            else:
                m1medicine.access_rule = lambda state: (state.count("-1 Minute - Medicine", world.player) >= m1access)
                m2medicine.access_rule = lambda state: (state.count("-1 Minute - Medicine", world.player) >= m1access)
                m3medicine.access_rule = lambda state: (state.count("-1 Minute - Medicine", world.player) >= m2access)
                m4medicine.access_rule = lambda state: (state.count("-1 Minute - Medicine", world.player) >= m2access)
                m5medicine.access_rule = lambda state: (state.count("-1 Minute - Medicine", world.player) >= m3access)
                m6medicine.access_rule = lambda state: (state.count("-1 Minute - Medicine", world.player) >= m3access)
                m7medicine.access_rule = lambda state: (state.count("-1 Minute - Medicine", world.player) >= m4access)
                m8medicine.access_rule = lambda state: (state.count("-1 Minute - Medicine", world.player) >= m4access)
                m9medicine.access_rule = lambda state: (state.count("-1 Minute - Medicine", world.player) >= m5access)
        if "Yuuka" in world.in_pool_characters:
            m1p2, m2p2, m3p2, m4p2, m5p2, m6p2, m7p2, m8p2, m9p2 = world.character_matchups["Yuuka"]
            m1yuuka = multiworld.get_location(f"[Yuuka] VS {m1p2} - {time1}", player)
            m2yuuka = multiworld.get_location(f"[Yuuka] VS {m2p2} - {time1}", player)
            m3yuuka = multiworld.get_location(f"[Yuuka] VS {m3p2} - {time2}", player)
            m4yuuka = multiworld.get_location(f"[Yuuka] VS {m4p2} - {time2}", player)
            m5yuuka = multiworld.get_location(f"[Yuuka] VS {m5p2} - {time3}", player)
            m6yuuka = multiworld.get_location(f"[Yuuka] VS {m6p2} - {time3}", player)
            m7yuuka = multiworld.get_location(f"[Yuuka] VS {m7p2} - {time4}", player)
            m8yuuka = multiworld.get_location(f"[Yuuka] VS {m8p2} - {time4}", player)
            m9yuuka = multiworld.get_location(f"[Yuuka] Finale: VS {m9p2} - {time5}", player)
            m1yuuka.access_rule = lambda state: (state.count("-1 Minute - Yuuka", world.player) >= m1access)
            m2yuuka.access_rule = lambda state: (state.count("-1 Minute - Yuuka", world.player) >= m1access)
            m3yuuka.access_rule = lambda state: (state.count("-1 Minute - Yuuka", world.player) >= m2access)
            m4yuuka.access_rule = lambda state: (state.count("-1 Minute - Yuuka", world.player) >= m2access)
            m5yuuka.access_rule = lambda state: (state.count("-1 Minute - Yuuka", world.player) >= m3access)
            m6yuuka.access_rule = lambda state: (state.count("-1 Minute - Yuuka", world.player) >= m3access)
            m7yuuka.access_rule = lambda state: (state.count("-1 Minute - Yuuka", world.player) >= m4access)
            m8yuuka.access_rule = lambda state: (state.count("-1 Minute - Yuuka", world.player) >= m4access)
            m9yuuka.access_rule = lambda state: (state.count("-1 Minute - Yuuka", world.player) >= m5access)
        if "Komachi" in world.in_pool_characters:
            m1p2, m2p2, m3p2, m4p2, m5p2, m6p2, m7p2, m8p2, m9p2 = world.character_matchups["Komachi"]
            m1komachi = multiworld.get_location(f"[Komachi] VS {m1p2} - {time1}", player)
            m2komachi = multiworld.get_location(f"[Komachi] VS {m2p2} - {time1}", player)
            m3komachi = multiworld.get_location(f"[Komachi] VS {m3p2} - {time2}", player)
            m4komachi = multiworld.get_location(f"[Komachi] VS {m4p2} - {time2}", player)
            m5komachi = multiworld.get_location(f"[Komachi] VS {m5p2} - {time3}", player)
            m6komachi = multiworld.get_location(f"[Komachi] VS {m6p2} - {time3}", player)
            m7komachi = multiworld.get_location(f"[Komachi] VS {m7p2} - {time4}", player)
            m8komachi = multiworld.get_location(f"[Komachi] VS {m8p2} - {time4}", player)
            m9komachi = multiworld.get_location(f"[Komachi] Finale: VS {m9p2} - {time5}", player)
            m1komachi.access_rule = lambda state: (state.count("-1 Minute - Komachi", world.player) >= m1access)
            m2komachi.access_rule = lambda state: (state.count("-1 Minute - Komachi", world.player) >= m1access)
            m3komachi.access_rule = lambda state: (state.count("-1 Minute - Komachi", world.player) >= m2access)
            m4komachi.access_rule = lambda state: (state.count("-1 Minute - Komachi", world.player) >= m2access)
            m5komachi.access_rule = lambda state: (state.count("-1 Minute - Komachi", world.player) >= m3access)
            m6komachi.access_rule = lambda state: (state.count("-1 Minute - Komachi", world.player) >= m3access)
            m7komachi.access_rule = lambda state: (state.count("-1 Minute - Komachi", world.player) >= m4access)
            m8komachi.access_rule = lambda state: (state.count("-1 Minute - Komachi", world.player) >= m4access)
            m9komachi.access_rule = lambda state: (state.count("-1 Minute - Komachi", world.player) >= m5access)
        if "Shikieiki" in world.in_pool_characters:
            m1p2, m2p2, m3p2, m4p2, m5p2, m6p2, m7p2, m8p2, m9p2 = world.character_matchups["Shikieiki"]
            m1shikieiki = multiworld.get_location(f"[Shikieiki] VS {m1p2} - {time1}", player)
            m2shikieiki = multiworld.get_location(f"[Shikieiki] VS {m2p2} - {time1}", player)
            m3shikieiki = multiworld.get_location(f"[Shikieiki] VS {m3p2} - {time2}", player)
            m4shikieiki = multiworld.get_location(f"[Shikieiki] VS {m4p2} - {time2}", player)
            m5shikieiki = multiworld.get_location(f"[Shikieiki] VS {m5p2} - {time3}", player)
            m6shikieiki = multiworld.get_location(f"[Shikieiki] VS {m6p2} - {time3}", player)
            m7shikieiki = multiworld.get_location(f"[Shikieiki] VS {m7p2} - {time4}", player)
            m8shikieiki = multiworld.get_location(f"[Shikieiki] VS {m8p2} - {time4}", player)
            m9shikieiki = multiworld.get_location(f"[Shikieiki] Finale: VS {m9p2} - {time5}", player)
            m1shikieiki.access_rule = lambda state: (state.count("-1 Minute - Shikieiki", world.player) >= m1access)
            m2shikieiki.access_rule = lambda state: (state.count("-1 Minute - Shikieiki", world.player) >= m1access)
            m3shikieiki.access_rule = lambda state: (state.count("-1 Minute - Shikieiki", world.player) >= m2access)
            m4shikieiki.access_rule = lambda state: (state.count("-1 Minute - Shikieiki", world.player) >= m2access)
            m5shikieiki.access_rule = lambda state: (state.count("-1 Minute - Shikieiki", world.player) >= m3access)
            m6shikieiki.access_rule = lambda state: (state.count("-1 Minute - Shikieiki", world.player) >= m3access)
            m7shikieiki.access_rule = lambda state: (state.count("-1 Minute - Shikieiki", world.player) >= m4access)
            m8shikieiki.access_rule = lambda state: (state.count("-1 Minute - Shikieiki", world.player) >= m4access)
            m9shikieiki.access_rule = lambda state: (state.count("-1 Minute - Shikieiki", world.player) >= m5access)

    def Example_Rule(state: CollectionState) -> bool:
        # Calculated rules take a CollectionState object and return a boolean
        # True if the player can access the location
        # CollectionState is defined in BaseClasses
        return True

    ## Common functions:
    # location = world.get_location(location_name, player)
    # location.access_rule = Example_Rule

    ## Combine rules:
    # old_rule = location.access_rule
    # location.access_rule = lambda state: old_rule(state) and Example_Rule(state)
    # OR
    # location.access_rule = lambda state: old_rule(state) or Example_Rule(state)

# The item name to create is provided before the item is created, in case you want to make changes to it
def before_create_item(item_name: str, world: World, multiworld: MultiWorld, player: int) -> str:

    # Aya and Medicine's resource items are classified as "useful" if ayamedi_progression option is false
    ayamedi_progression = get_option_value(multiworld, player, "ayamedi_progression")
    item_from_table = world.item_name_to_item.get(item_name)

    if "AyaMedi" in set(item_from_table.get('category', [])):
        if not ayamedi_progression:
            item_from_table['useful'] = True
            
            for removing_classification in ['progression', 'progression_skip_balancing']:
                if removing_classification in item_from_table.keys():
                    del item_from_table[removing_classification]
    return item_name

# The item that was created is provided after creation, in case you want to modify the item
def after_create_item(item: ManualItem, world: World, multiworld: MultiWorld, player: int) -> ManualItem:
    return item

# This method is run towards the end of pre-generation, before the place_item options have been handled and before AP generation occurs
def before_generate_basic(world: World, multiworld: MultiWorld, player: int):
    pass

# This method is run at the very end of pre-generation, once the place_item options have been handled and before AP generation occurs
def after_generate_basic(world: World, multiworld: MultiWorld, player: int):
    pass

# This method is run every time an item is added to the state, can be used to modify the value of an item.
# IMPORTANT! Any changes made in this hook must be cancelled/undone in after_remove_item
def after_collect_item(world: World, state: CollectionState, Changed: bool, item: Item):
    # the following let you add to the Potato Item Value count
    # if item.name == "Cooked Potato":
    #     state.prog_items[item.player][format_state_prog_items_key(ProgItemsCat.VALUE, "Potato")] += 1
    pass

# This method is run every time an item is removed from the state, can be used to modify the value of an item.
# IMPORTANT! Any changes made in this hook must be first done in after_collect_item
def after_remove_item(world: World, state: CollectionState, Changed: bool, item: Item):
    # the following let you undo the addition to the Potato Item Value count
    # if item.name == "Cooked Potato":
    #     state.prog_items[item.player][format_state_prog_items_key(ProgItemsCat.VALUE, "Potato")] -= 1
    pass


# This is called before slot data is set and provides an empty dict ({}), in case you want to modify it before Manual does
def before_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    game_mode = get_option_value(multiworld, player, "game_mode")
    random_enabled_characters = get_option_value(multiworld, player, "random_enabled_characters")

    if game_mode:
        slot_data["character_matchups"] = world.character_matchups
    if len(world.e_char) > random_enabled_characters and random_enabled_characters != 0:
        slot_data["in_pool_characters"] = world.in_pool_characters

    return slot_data

# This is called after slot data is set and provides the slot data at the time, in case you want to check and modify it after Manual is done with it
def after_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data

# This is called right at the end, in case you want to write stuff to the spoiler log
def before_write_spoiler(world: World, multiworld: MultiWorld, spoiler_handle) -> None:
    pass

# This is called when you want to add information to the hint text
def before_extend_hint_information(hint_data: dict[int, dict[int, str]], world: World, multiworld: MultiWorld, player: int) -> None:

    ### Example way to use this hook:
    # if player not in hint_data:
    #     hint_data.update({player: {}})
    # for location in multiworld.get_locations(player):
    #     if not location.address:
    #         continue
    #
    #     use this section to calculate the hint string
    #
    #     hint_data[player][location.address] = hint_string

    pass

def after_extend_hint_information(hint_data: dict[int, dict[int, str]], world: World, multiworld: MultiWorld, player: int) -> None:
    pass
