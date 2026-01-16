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
    # Use this hook to remove locations from the world
    locationNamesToRemove: list[str] = [] # List of location names

    # Add your code here to calculate which locations to remove

    for region in multiworld.regions:
        if region.player == player:
            for location in list(region.locations):
                if location.name in locationNamesToRemove:
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

    # Yaml option values
    game_mode = get_option_value(multiworld, player, "mode")
    endings_required = get_option_value(multiworld, player, "endings_required")
    story_difficulty_mid = get_option_value(multiworld, player, "story_difficulty_mid")
    story_difficulty_end = get_option_value(multiworld, player, "story_difficulty_end")
    match_difficulty = get_option_value(multiworld, player, "match_difficulty")
    ayamedi_difficulty = get_option_value(multiworld, player, "ayamedi_difficulty")
    # th_prac = get_option_value(multiworld, player, "thprac")

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

    # Goal access rules
    ending = multiworld.get_location("Resolve Incident", player)
    ending.access_rule = lambda state: (state.count_group("Endings", world.player) >= endings_required)

    # Story Mode access rules
    if game_mode == 0:
        if story_difficulty_mid == 0:
            s6access = 0
            s7access = 0
            s8access = 0
        else:
            s6access = 1
            if story_difficulty_mid == 1:
                s7access = 1
                s8access = 1
            else:
                s7access = 2
                if story_difficulty_mid == 2:
                    s8access = 2
                else:
                    s8access = 3

        if story_difficulty_mid >= story_difficulty_end:
            s9access = story_difficulty_mid + 1
        else:
            s9access = story_difficulty_end

        if enable_reimu == True:
            s6reimu = multiworld.get_location("[Reimu] Stage 6 Clear", player)
            s7reimu = multiworld.get_location("[Reimu] Stage 7 Clear", player)
            s8reimu = multiworld.get_location("[Reimu] Stage 8 Clear", player)
            s9reimu = multiworld.get_location("[Reimu] Stage 9 Clear", player)
            s6reimu.access_rule = lambda state: (state.count("+1 Life - Reimu", world.player) >= s6access)
            s7reimu.access_rule = lambda state: (state.count("+1 Life - Reimu", world.player) >= s7access)
            s8reimu.access_rule = lambda state: (state.count("+1 Life - Reimu", world.player) >= s8access)
            s9reimu.access_rule = lambda state: (state.count("+1 Life - Reimu", world.player) >= s9access)
        if enable_marisa == True:
            s6marisa = multiworld.get_location("[Marisa] Stage 6 Clear", player)
            s7marisa = multiworld.get_location("[Marisa] Stage 7 Clear", player)
            s8marisa = multiworld.get_location("[Marisa] Stage 8 Clear", player)
            s9marisa = multiworld.get_location("[Marisa] Stage 9 Clear", player)
            s6marisa.access_rule = lambda state: (state.count("+1 Life - Marisa", world.player) >= s6access)
            s7marisa.access_rule = lambda state: (state.count("+1 Life - Marisa", world.player) >= s7access)
            s8marisa.access_rule = lambda state: (state.count("+1 Life - Marisa", world.player) >= s8access)
            s9marisa.access_rule = lambda state: (state.count("+1 Life - Marisa", world.player) >= s9access)
        if enable_sakuya == True:
            s6sakuya = multiworld.get_location("[Sakuya] Stage 6 Clear", player)
            s7sakuya = multiworld.get_location("[Sakuya] Stage 7 Clear", player)
            s8sakuya = multiworld.get_location("[Sakuya] Stage 8 Clear", player)
            s9sakuya = multiworld.get_location("[Sakuya] Stage 9 Clear", player)
            s6sakuya.access_rule = lambda state: (state.count("+1 Life - Sakuya", world.player) >= s6access)
            s7sakuya.access_rule = lambda state: (state.count("+1 Life - Sakuya", world.player) >= s7access)
            s8sakuya.access_rule = lambda state: (state.count("+1 Life - Sakuya", world.player) >= s8access)
            s9sakuya.access_rule = lambda state: (state.count("+1 Life - Sakuya", world.player) >= s9access)
        if enable_youmu == True:
            s6youmu = multiworld.get_location("[Youmu] Stage 6 Clear", player)
            s7youmu = multiworld.get_location("[Youmu] Stage 7 Clear", player)
            s8youmu = multiworld.get_location("[Youmu] Stage 8 Clear", player)
            s9youmu = multiworld.get_location("[Youmu] Stage 9 Clear", player)
            s6youmu.access_rule = lambda state: (state.count("+1 Life - Youmu", world.player) >= s6access)
            s7youmu.access_rule = lambda state: (state.count("+1 Life - Youmu", world.player) >= s7access)
            s8youmu.access_rule = lambda state: (state.count("+1 Life - Youmu", world.player) >= s8access)
            s9youmu.access_rule = lambda state: (state.count("+1 Life - Youmu", world.player) >= s9access)
        if enable_reisen == True:
            s6reisen = multiworld.get_location("[Reisen] Stage 6 Clear", player)
            s7reisen = multiworld.get_location("[Reisen] Stage 7 Clear", player)
            s8reisen = multiworld.get_location("[Reisen] Stage 8 Clear", player)
            s9reisen = multiworld.get_location("[Reisen] Stage 9 Clear", player)
            s6reisen.access_rule = lambda state: (state.count("+1 Life - Reisen", world.player) >= s6access)
            s7reisen.access_rule = lambda state: (state.count("+1 Life - Reisen", world.player) >= s7access)
            s8reisen.access_rule = lambda state: (state.count("+1 Life - Reisen", world.player) >= s8access)
            s9reisen.access_rule = lambda state: (state.count("+1 Life - Reisen", world.player) >= s9access)
        if enable_cirno == True:
            s6cirno = multiworld.get_location("[Cirno] Stage 6 Clear", player)
            s7cirno = multiworld.get_location("[Cirno] Stage 7 Clear", player)
            s8cirno = multiworld.get_location("[Cirno] Stage 8 Clear", player)
            s9cirno = multiworld.get_location("[Cirno] Stage 9 Clear", player)
            s6cirno.access_rule = lambda state: (state.count("+1 Life - Cirno", world.player) >= s6access)
            s7cirno.access_rule = lambda state: (state.count("+1 Life - Cirno", world.player) >= s7access)
            s8cirno.access_rule = lambda state: (state.count("+1 Life - Cirno", world.player) >= s8access)
            s9cirno.access_rule = lambda state: (state.count("+1 Life - Cirno", world.player) >= s9access)
        if enable_lyrica == True:
            s6lyrica = multiworld.get_location("[Lyrica] Stage 6 Clear", player)
            s7lyrica = multiworld.get_location("[Lyrica] Stage 7 Clear", player)
            s8lyrica = multiworld.get_location("[Lyrica] Stage 8 Clear", player)
            s9lyrica = multiworld.get_location("[Lyrica] Stage 9 Clear", player)
            s6lyrica.access_rule = lambda state: (state.count("+1 Life - Lyrica", world.player) >= s6access)
            s7lyrica.access_rule = lambda state: (state.count("+1 Life - Lyrica", world.player) >= s7access)
            s8lyrica.access_rule = lambda state: (state.count("+1 Life - Lyrica", world.player) >= s8access)
            s9lyrica.access_rule = lambda state: (state.count("+1 Life - Lyrica", world.player) >= s9access)
        if enable_mystia == True:
            s6mystia = multiworld.get_location("[Mystia] Stage 6 Clear", player)
            s7mystia = multiworld.get_location("[Mystia] Stage 7 Clear", player)
            s8mystia = multiworld.get_location("[Mystia] Stage 8 Clear", player)
            s9mystia = multiworld.get_location("[Mystia] Stage 9 Clear", player)
            s6mystia.access_rule = lambda state: (state.count("+1 Life - Mystia", world.player) >= s6access)
            s7mystia.access_rule = lambda state: (state.count("+1 Life - Mystia", world.player) >= s7access)
            s8mystia.access_rule = lambda state: (state.count("+1 Life - Mystia", world.player) >= s8access)
            s9mystia.access_rule = lambda state: (state.count("+1 Life - Mystia", world.player) >= s9access)
        if enable_tewi == True:
            s6tewi = multiworld.get_location("[Tewi] Stage 6 Clear", player)
            s7tewi = multiworld.get_location("[Tewi] Stage 7 Clear", player)
            s8tewi = multiworld.get_location("[Tewi] Stage 8 Clear", player)
            s9tewi = multiworld.get_location("[Tewi] Stage 9 Clear", player)
            s6tewi.access_rule = lambda state: (state.count("+1 Life - Tewi", world.player) >= s6access)
            s7tewi.access_rule = lambda state: (state.count("+1 Life - Tewi", world.player) >= s7access)
            s8tewi.access_rule = lambda state: (state.count("+1 Life - Tewi", world.player) >= s8access)
            s9tewi.access_rule = lambda state: (state.count("+1 Life - Tewi", world.player) >= s9access)
        if enable_yuuka == True:
            s6yuuka = multiworld.get_location("[Yuuka] Stage 6 Clear", player)
            s7yuuka = multiworld.get_location("[Yuuka] Stage 7 Clear", player)
            s8yuuka = multiworld.get_location("[Yuuka] Stage 8 Clear", player)
            s9yuuka = multiworld.get_location("[Yuuka] Stage 9 Clear", player)
            s6yuuka.access_rule = lambda state: (state.count("+1 Life - Yuuka", world.player) >= s6access)
            s7yuuka.access_rule = lambda state: (state.count("+1 Life - Yuuka", world.player) >= s7access)
            s8yuuka.access_rule = lambda state: (state.count("+1 Life - Yuuka", world.player) >= s8access)
            s9yuuka.access_rule = lambda state: (state.count("+1 Life - Yuuka", world.player) >= s9access)
        if enable_komachi == True:
            s6komachi = multiworld.get_location("[Komachi] Stage 6 Clear", player)
            s7komachi = multiworld.get_location("[Komachi] Stage 7 Clear", player)
            s8komachi = multiworld.get_location("[Komachi] Stage 8 Clear", player)
            s9komachi = multiworld.get_location("[Komachi] Stage 9 Clear", player)
            s6komachi.access_rule = lambda state: (state.count("+1 Life - Komachi", world.player) >= s6access)
            s7komachi.access_rule = lambda state: (state.count("+1 Life - Komachi", world.player) >= s7access)
            s8komachi.access_rule = lambda state: (state.count("+1 Life - Komachi", world.player) >= s8access)
            s9komachi.access_rule = lambda state: (state.count("+1 Life - Komachi", world.player) >= s9access)
        if enable_shikieiki == True:
            s6shikieiki = multiworld.get_location("[Shikieiki] Stage 6 Clear", player)
            s7shikieiki = multiworld.get_location("[Shikieiki] Stage 7 Clear", player)
            s8shikieiki = multiworld.get_location("[Shikieiki] Stage 8 Clear", player)
            s9shikieiki = multiworld.get_location("[Shikieiki] Stage 9 Clear", player)
            s6shikieiki.access_rule = lambda state: (state.count("+1 Life - Shikieiki", world.player) >= s6access)
            s7shikieiki.access_rule = lambda state: (state.count("+1 Life - Shikieiki", world.player) >= s7access)
            s8shikieiki.access_rule = lambda state: (state.count("+1 Life - Shikieiki", world.player) >= s8access)
            s9shikieiki.access_rule = lambda state: (state.count("+1 Life - Shikieiki", world.player) >= s9access)
        if enable_aya == True:
            s6aya = multiworld.get_location("[Aya] Stage 6 Clear", player)
            s7aya = multiworld.get_location("[Aya] Stage 7 Clear", player)
            s8aya = multiworld.get_location("[Aya] Stage 8 Clear", player)
            s9aya = multiworld.get_location("[Aya] Stage 9 Clear", player)
            if ayamedi_difficulty == False:
                s6aya.access_rule = lambda state: (state.count("+1 Life - Aya", world.player) >= 0)
                s7aya.access_rule = lambda state: (state.count("+1 Life - Aya", world.player) >= 0)
                s8aya.access_rule = lambda state: (state.count("+1 Life - Aya", world.player) >= 0)
                s9aya.access_rule = lambda state: (state.count("+1 Life - Aya", world.player) >= 0)
            else:
                s6aya.access_rule = lambda state: (state.count("+1 Life - Aya", world.player) >= s6access)
                s7aya.access_rule = lambda state: (state.count("+1 Life - Aya", world.player) >= s7access)
                s8aya.access_rule = lambda state: (state.count("+1 Life - Aya", world.player) >= s8access)
                s9aya.access_rule = lambda state: (state.count("+1 Life - Aya", world.player) >= s9access)
        if enable_medicine == True:
            s6medicine = multiworld.get_location("[Medicine] Stage 6 Clear", player)
            s7medicine = multiworld.get_location("[Medicine] Stage 7 Clear", player)
            s8medicine = multiworld.get_location("[Medicine] Stage 8 Clear", player)
            s9medicine = multiworld.get_location("[Medicine] Stage 9 Clear", player)
            if ayamedi_difficulty == False:
                s6medicine.access_rule = lambda state: (state.count("+1 Life - Medicine", world.player) >= 0)
                s7medicine.access_rule = lambda state: (state.count("+1 Life - Medicine", world.player) >= 0)
                s8medicine.access_rule = lambda state: (state.count("+1 Life - Medicine", world.player) >= 0)
                s9medicine.access_rule = lambda state: (state.count("+1 Life - Medicine", world.player) >= 0)
            else:
                s6medicine.access_rule = lambda state: (state.count("+1 Life - Medicine", world.player) >= s6access)
                s7medicine.access_rule = lambda state: (state.count("+1 Life - Medicine", world.player) >= s7access)
                s8medicine.access_rule = lambda state: (state.count("+1 Life - Medicine", world.player) >= s8access)
                s9medicine.access_rule = lambda state: (state.count("+1 Life - Medicine", world.player) >= s9access)
    
    # Match Mode access rules
    if game_mode == 1:
        m1access = match_difficulty - 6
        m2access = match_difficulty - 4
        m3access = match_difficulty - 2
        m4access = match_difficulty

        if enable_reimu == True:
            m3rei = multiworld.get_location("[Reimu] VS Lyrica - 2:00", player)
            m4rei = multiworld.get_location("[Reimu] VS Youmu - 2:00", player)
            m5rei = multiworld.get_location("[Reimu] VS Sakuya - 4:00", player)
            m6rei = multiworld.get_location("[Reimu] VS Marisa - 4:00", player)
            m7rei = multiworld.get_location("[Reimu] VS Aya - 6:00", player)
            m8rei = multiworld.get_location("[Reimu] VS Komachi - 6:00", player)
            m9rei = multiworld.get_location("[Reimu] Finale: VS Shikieiki - 8:00", player)
            m3rei.access_rule = lambda state: (state.count("-1 Minute - Reimu", world.player) >= m1access)
            m4rei.access_rule = lambda state: (state.count("-1 Minute - Reimu", world.player) >= m1access)
            m5rei.access_rule = lambda state: (state.count("-1 Minute - Reimu", world.player) >= m2access)
            m6rei.access_rule = lambda state: (state.count("-1 Minute - Reimu", world.player) >= m2access)
            m7rei.access_rule = lambda state: (state.count("-1 Minute - Reimu", world.player) >= m3access)
            m8rei.access_rule = lambda state: (state.count("-1 Minute - Reimu", world.player) >= m3access)
            m9rei.access_rule = lambda state: (state.count("-1 Minute - Reimu", world.player) >= m4access)
        if enable_marisa == True:
            m3mar = multiworld.get_location("[Marisa] VS Tewi - 2:00", player)
            m4mar = multiworld.get_location("[Marisa] VS Reisen - 2:00", player)
            m5mar = multiworld.get_location("[Marisa] VS Youmu - 4:00", player)
            m6mar = multiworld.get_location("[Marisa] VS Reimu - 4:00", player)
            m7mar = multiworld.get_location("[Marisa] VS Aya - 6:00", player)
            m8mar = multiworld.get_location("[Marisa] VS Komachi - 6:00", player)
            m9mar = multiworld.get_location("[Marisa] Finale: VS Shikieiki - 8:00", player)
            m3mar.access_rule = lambda state: (state.count("-1 Minute - Marisa", world.player) >= m1access)
            m4mar.access_rule = lambda state: (state.count("-1 Minute - Marisa", world.player) >= m1access)
            m5mar.access_rule = lambda state: (state.count("-1 Minute - Marisa", world.player) >= m2access)
            m6mar.access_rule = lambda state: (state.count("-1 Minute - Marisa", world.player) >= m2access)
            m7mar.access_rule = lambda state: (state.count("-1 Minute - Marisa", world.player) >= m3access)
            m8mar.access_rule = lambda state: (state.count("-1 Minute - Marisa", world.player) >= m3access)
            m9mar.access_rule = lambda state: (state.count("-1 Minute - Marisa", world.player) >= m4access)
        if enable_sakuya == True:
            m3sak = multiworld.get_location("[Sakuya] VS Lyrica - 2:00", player)
            m4sak = multiworld.get_location("[Sakuya] VS Reisen - 2:00", player)
            m5sak = multiworld.get_location("[Sakuya] VS Reimu - 4:00", player)
            m6sak = multiworld.get_location("[Sakuya] VS Tewi - 4:00", player)
            m7sak = multiworld.get_location("[Sakuya] VS Medicine - 6:00", player)
            m8sak = multiworld.get_location("[Sakuya] VS Komachi - 6:00", player)
            m9sak = multiworld.get_location("[Sakuya] Finale: VS Shikieiki - 8:00", player)
            m3sak.access_rule = lambda state: (state.count("-1 Minute - Sakuya", world.player) >= m1access)
            m4sak.access_rule = lambda state: (state.count("-1 Minute - Sakuya", world.player) >= m1access)
            m5sak.access_rule = lambda state: (state.count("-1 Minute - Sakuya", world.player) >= m2access)
            m6sak.access_rule = lambda state: (state.count("-1 Minute - Sakuya", world.player) >= m2access)
            m7sak.access_rule = lambda state: (state.count("-1 Minute - Sakuya", world.player) >= m3access)
            m8sak.access_rule = lambda state: (state.count("-1 Minute - Sakuya", world.player) >= m3access)
            m9sak.access_rule = lambda state: (state.count("-1 Minute - Sakuya", world.player) >= m4access)
        if enable_youmu == True:
            m3you = multiworld.get_location("[Youmu] VS Lyrica - 2:00", player)
            m4you = multiworld.get_location("[Youmu] VS Marisa - 2:00", player)
            m5you = multiworld.get_location("[Youmu] VS Reisen - 4:00", player)
            m6you = multiworld.get_location("[Youmu] VS Sakuya - 4:00", player)
            m7you = multiworld.get_location("[Youmu] VS Aya - 6:00", player)
            m8you = multiworld.get_location("[Youmu] VS Komachi - 6:00", player)
            m9you = multiworld.get_location("[Youmu] Finale: VS Shikieiki - 8:00", player)
            m3you.access_rule = lambda state: (state.count("-1 Minute - Youmu", world.player) >= m1access)
            m4you.access_rule = lambda state: (state.count("-1 Minute - Youmu", world.player) >= m1access)
            m5you.access_rule = lambda state: (state.count("-1 Minute - Youmu", world.player) >= m2access)
            m6you.access_rule = lambda state: (state.count("-1 Minute - Youmu", world.player) >= m2access)
            m7you.access_rule = lambda state: (state.count("-1 Minute - Youmu", world.player) >= m3access)
            m8you.access_rule = lambda state: (state.count("-1 Minute - Youmu", world.player) >= m3access)
            m9you.access_rule = lambda state: (state.count("-1 Minute - Youmu", world.player) >= m4access)
        if enable_reisen == True:
            m3udo = multiworld.get_location("[Reisen] VS Tewi - 2:00", player)
            m4udo = multiworld.get_location("[Reisen] VS Marisa - 2:00", player)
            m5udo = multiworld.get_location("[Reisen] VS Youmu - 4:00", player)
            m6udo = multiworld.get_location("[Reisen] VS Sakuya - 4:00", player)
            m7udo = multiworld.get_location("[Reisen] VS Medicine - 6:00", player)
            m8udo = multiworld.get_location("[Reisen] VS Komachi - 6:00", player)
            m9udo = multiworld.get_location("[Reisen] Finale: VS Shikieiki - 8:00", player)
            m3udo.access_rule = lambda state: (state.count("-1 Minute - Reisen", world.player) >= m1access)
            m4udo.access_rule = lambda state: (state.count("-1 Minute - Reisen", world.player) >= m1access)
            m5udo.access_rule = lambda state: (state.count("-1 Minute - Reisen", world.player) >= m2access)
            m6udo.access_rule = lambda state: (state.count("-1 Minute - Reisen", world.player) >= m2access)
            m7udo.access_rule = lambda state: (state.count("-1 Minute - Reisen", world.player) >= m3access)
            m8udo.access_rule = lambda state: (state.count("-1 Minute - Reisen", world.player) >= m3access)
            m9udo.access_rule = lambda state: (state.count("-1 Minute - Reisen", world.player) >= m4access)
        if enable_cirno == True:
            m3cir = multiworld.get_location("[Cirno] VS Marisa - 2:00", player)
            m4cir = multiworld.get_location("[Cirno] VS Sakuya - 2:00", player)
            m5cir = multiworld.get_location("[Cirno] VS Reimu - 4:00", player)
            m6cir = multiworld.get_location("[Cirno] VS Reisen - 4:00", player)
            m7cir = multiworld.get_location("[Cirno] VS Aya - 6:00", player)
            m8cir = multiworld.get_location("[Cirno] VS Yuuka - 6:00", player)
            m9cir = multiworld.get_location("[Cirno] Finale: VS Shikieiki - 8:00", player)
            m3cir.access_rule = lambda state: (state.count("-1 Minute - Cirno", world.player) >= m1access)
            m4cir.access_rule = lambda state: (state.count("-1 Minute - Cirno", world.player) >= m1access)
            m5cir.access_rule = lambda state: (state.count("-1 Minute - Cirno", world.player) >= m2access)
            m6cir.access_rule = lambda state: (state.count("-1 Minute - Cirno", world.player) >= m2access)
            m7cir.access_rule = lambda state: (state.count("-1 Minute - Cirno", world.player) >= m3access)
            m8cir.access_rule = lambda state: (state.count("-1 Minute - Cirno", world.player) >= m3access)
            m9cir.access_rule = lambda state: (state.count("-1 Minute - Cirno", world.player) >= m4access)
        if enable_lyrica == True:
            m3lyr = multiworld.get_location("[Lyrica] VS Tewi - 2:00", player)
            m4lyr = multiworld.get_location("[Lyrica] VS Reisen - 2:00", player)
            m5lyr = multiworld.get_location("[Lyrica] VS Marisa - 4:00", player)
            m6lyr = multiworld.get_location("[Lyrica] VS Youmu - 4:00", player)
            m7lyr = multiworld.get_location("[Lyrica] VS Aya - 6:00", player)
            m8lyr = multiworld.get_location("[Lyrica] VS Yuuka - 6:00", player)
            m9lyr = multiworld.get_location("[Lyrica] Finale: VS Shikieiki - 8:00", player)
            m3lyr.access_rule = lambda state: (state.count("-1 Minute - Lyrica", world.player) >= m1access)
            m4lyr.access_rule = lambda state: (state.count("-1 Minute - Lyrica", world.player) >= m1access)
            m5lyr.access_rule = lambda state: (state.count("-1 Minute - Lyrica", world.player) >= m2access)
            m6lyr.access_rule = lambda state: (state.count("-1 Minute - Lyrica", world.player) >= m2access)
            m7lyr.access_rule = lambda state: (state.count("-1 Minute - Lyrica", world.player) >= m3access)
            m8lyr.access_rule = lambda state: (state.count("-1 Minute - Lyrica", world.player) >= m3access)
            m9lyr.access_rule = lambda state: (state.count("-1 Minute - Lyrica", world.player) >= m4access)
        if enable_merlin == True:
            m3mer = multiworld.get_location("[Merlin] VS Tewi - 2:00", player)
            m4mer = multiworld.get_location("[Merlin] VS Reisen - 2:00", player)
            m5mer = multiworld.get_location("[Merlin] VS Sakuya - 4:00", player)
            m6mer = multiworld.get_location("[Merlin] VS Youmu - 4:00", player)
            m7mer = multiworld.get_location("[Merlin] VS Aya - 6:00", player)
            m8mer = multiworld.get_location("[Merlin] VS Yuuka - 6:00", player)
            m9mer = multiworld.get_location("[Merlin] Finale: VS Shikieiki - 8:00", player)
            m3mer.access_rule = lambda state: (state.count("-1 Minute - Merlin", world.player) >= m1access)
            m4mer.access_rule = lambda state: (state.count("-1 Minute - Merlin", world.player) >= m1access)
            m5mer.access_rule = lambda state: (state.count("-1 Minute - Merlin", world.player) >= m2access)
            m6mer.access_rule = lambda state: (state.count("-1 Minute - Merlin", world.player) >= m2access)
            m7mer.access_rule = lambda state: (state.count("-1 Minute - Merlin", world.player) >= m3access)
            m8mer.access_rule = lambda state: (state.count("-1 Minute - Merlin", world.player) >= m3access)
            m9mer.access_rule = lambda state: (state.count("-1 Minute - Merlin", world.player) >= m4access)
        if enable_lunasa == True:
            m3lun = multiworld.get_location("[Lunasa] VS Tewi - 2:00", player)
            m4lun = multiworld.get_location("[Lunasa] VS Reisen - 2:00", player)
            m5lun = multiworld.get_location("[Lunasa] VS Reimu - 4:00", player)
            m6lun = multiworld.get_location("[Lunasa] VS Youmu - 4:00", player)
            m7lun = multiworld.get_location("[Lunasa] VS Aya - 6:00", player)
            m8lun = multiworld.get_location("[Lunasa] VS Yuuka - 6:00", player)
            m9lun = multiworld.get_location("[Lunasa] Finale: VS Shikieiki - 8:00", player)
            m3lun.access_rule = lambda state: (state.count("-1 Minute - Lunasa", world.player) >= m1access)
            m4lun.access_rule = lambda state: (state.count("-1 Minute - Lunasa", world.player) >= m1access)
            m5lun.access_rule = lambda state: (state.count("-1 Minute - Lunasa", world.player) >= m2access)
            m6lun.access_rule = lambda state: (state.count("-1 Minute - Lunasa", world.player) >= m2access)
            m7lun.access_rule = lambda state: (state.count("-1 Minute - Lunasa", world.player) >= m3access)
            m8lun.access_rule = lambda state: (state.count("-1 Minute - Lunasa", world.player) >= m3access)
            m9lun.access_rule = lambda state: (state.count("-1 Minute - Lunasa", world.player) >= m4access)
        if enable_mystia == True:
            m3mys = multiworld.get_location("[Mystia] VS Lyrica - 2:00", player)
            m4mys = multiworld.get_location("[Mystia] VS Marisa - 2:00", player)
            m5mys = multiworld.get_location("[Mystia] VS Sakuya - 4:00", player)
            m6mys = multiworld.get_location("[Mystia] VS Reimu - 4:00", player)
            m7mys = multiworld.get_location("[Mystia] VS Medicine - 6:00", player)
            m8mys = multiworld.get_location("[Mystia] VS Yuuka - 6:00", player)
            m9mys = multiworld.get_location("[Mystia] Finale: VS Shikieiki - 8:00", player)
            m3mys.access_rule = lambda state: (state.count("-1 Minute - Mystia", world.player) >= m1access)
            m4mys.access_rule = lambda state: (state.count("-1 Minute - Mystia", world.player) >= m1access)
            m5mys.access_rule = lambda state: (state.count("-1 Minute - Mystia", world.player) >= m2access)
            m6mys.access_rule = lambda state: (state.count("-1 Minute - Mystia", world.player) >= m2access)
            m7mys.access_rule = lambda state: (state.count("-1 Minute - Mystia", world.player) >= m3access)
            m8mys.access_rule = lambda state: (state.count("-1 Minute - Mystia", world.player) >= m3access)
            m9mys.access_rule = lambda state: (state.count("-1 Minute - Mystia", world.player) >= m4access)
        if enable_tewi == True:
            m3tew = multiworld.get_location("[Tewi] VS Lyrica - 2:00", player)
            m4tew = multiworld.get_location("[Tewi] VS Sakuya - 2:00", player)
            m5tew = multiworld.get_location("[Tewi] VS Marisa - 4:00", player)
            m6tew = multiworld.get_location("[Tewi] VS Reisen - 4:00", player)
            m7tew = multiworld.get_location("[Tewi] VS Medicine - 6:00", player)
            m8tew = multiworld.get_location("[Tewi] VS Komachi - 6:00", player)
            m9tew = multiworld.get_location("[Tewi] Finale: VS Shikieiki - 8:00", player)
            m3tew.access_rule = lambda state: (state.count("-1 Minute - Tewi", world.player) >= m1access)
            m4tew.access_rule = lambda state: (state.count("-1 Minute - Tewi", world.player) >= m1access)
            m5tew.access_rule = lambda state: (state.count("-1 Minute - Tewi", world.player) >= m2access)
            m6tew.access_rule = lambda state: (state.count("-1 Minute - Tewi", world.player) >= m2access)
            m7tew.access_rule = lambda state: (state.count("-1 Minute - Tewi", world.player) >= m3access)
            m8tew.access_rule = lambda state: (state.count("-1 Minute - Tewi", world.player) >= m3access)
            m9tew.access_rule = lambda state: (state.count("-1 Minute - Tewi", world.player) >= m4access)
        if enable_yuuka == True:
            m3yuu = multiworld.get_location("[Yuuka] VS Marisa - 2:00", player)
            m4yuu = multiworld.get_location("[Yuuka] VS Sakuya - 2:00", player)
            m5yuu = multiworld.get_location("[Yuuka] VS Youmu - 4:00", player)
            m6yuu = multiworld.get_location("[Yuuka] VS Reimu - 4:00", player)
            m7yuu = multiworld.get_location("[Yuuka] VS Aya - 6:00", player)
            m8yuu = multiworld.get_location("[Yuuka] VS Komachi - 6:00", player)
            m9yuu = multiworld.get_location("[Yuuka] Finale: VS Shikieiki - 8:00", player)
            m3yuu.access_rule = lambda state: (state.count("-1 Minute - Yuuka", world.player) >= m1access)
            m4yuu.access_rule = lambda state: (state.count("-1 Minute - Yuuka", world.player) >= m1access)
            m5yuu.access_rule = lambda state: (state.count("-1 Minute - Yuuka", world.player) >= m2access)
            m6yuu.access_rule = lambda state: (state.count("-1 Minute - Yuuka", world.player) >= m2access)
            m7yuu.access_rule = lambda state: (state.count("-1 Minute - Yuuka", world.player) >= m3access)
            m8yuu.access_rule = lambda state: (state.count("-1 Minute - Yuuka", world.player) >= m3access)
            m9yuu.access_rule = lambda state: (state.count("-1 Minute - Yuuka", world.player) >= m4access)
        if enable_komachi == True:
            m3kom = multiworld.get_location("[Komachi] VS Sakuya - 2:00", player)
            m4kom = multiworld.get_location("[Komachi] VS Tewi - 2:00", player)
            m5kom = multiworld.get_location("[Komachi] VS Youmu - 4:00", player)
            m6kom = multiworld.get_location("[Komachi] VS Marisa - 4:00", player)
            m7kom = multiworld.get_location("[Komachi] VS Yuuka - 6:00", player)
            m8kom = multiworld.get_location("[Komachi] VS Reimu - 6:00", player)
            m9kom = multiworld.get_location("[Komachi] Finale: VS Shikieiki - 8:00", player)
            m3kom.access_rule = lambda state: (state.count("-1 Minute - Komachi", world.player) >= m1access)
            m4kom.access_rule = lambda state: (state.count("-1 Minute - Komachi", world.player) >= m1access)
            m5kom.access_rule = lambda state: (state.count("-1 Minute - Komachi", world.player) >= m2access)
            m6kom.access_rule = lambda state: (state.count("-1 Minute - Komachi", world.player) >= m2access)
            m7kom.access_rule = lambda state: (state.count("-1 Minute - Komachi", world.player) >= m3access)
            m8kom.access_rule = lambda state: (state.count("-1 Minute - Komachi", world.player) >= m3access)
            m9kom.access_rule = lambda state: (state.count("-1 Minute - Komachi", world.player) >= m4access)
        if enable_shikieiki == True:
            m3shi = multiworld.get_location("[Shikieiki] VS Tewi - 2:00", player)
            m4shi = multiworld.get_location("[Shikieiki] VS Reisen - 2:00", player)
            m5shi = multiworld.get_location("[Shikieiki] VS Sakuya - 4:00", player)
            m6shi = multiworld.get_location("[Shikieiki] VS Marisa - 4:00", player)
            m7shi = multiworld.get_location("[Shikieiki] VS Aya - 6:00", player)
            m8shi = multiworld.get_location("[Shikieiki] VS Komachi - 6:00", player)
            m9shi = multiworld.get_location("[Shikieiki] Finale: VS Reimu - 8:00", player)
            m3shi.access_rule = lambda state: (state.count("-1 Minute - Shikieiki", world.player) >= m1access)
            m4shi.access_rule = lambda state: (state.count("-1 Minute - Shikieiki", world.player) >= m1access)
            m5shi.access_rule = lambda state: (state.count("-1 Minute - Shikieiki", world.player) >= m2access)
            m6shi.access_rule = lambda state: (state.count("-1 Minute - Shikieiki", world.player) >= m2access)
            m7shi.access_rule = lambda state: (state.count("-1 Minute - Shikieiki", world.player) >= m3access)
            m8shi.access_rule = lambda state: (state.count("-1 Minute - Shikieiki", world.player) >= m3access)
            m9shi.access_rule = lambda state: (state.count("-1 Minute - Shikieiki", world.player) >= m4access)
        if enable_aya == True:
            m3ay = multiworld.get_location("[Aya] VS Lyrica - 2:00", player)
            m4ay = multiworld.get_location("[Aya] VS Reimu - 2:00", player)
            m5ay = multiworld.get_location("[Aya] VS Reisen - 4:00", player)
            m6ay = multiworld.get_location("[Aya] VS Marisa - 4:00", player)
            m7ay = multiworld.get_location("[Aya] VS Medicine - 6:00", player)
            m8ay = multiworld.get_location("[Aya] VS Komachi - 6:00", player)
            m9ay = multiworld.get_location("[Aya] Finale: VS Shikieiki - 8:00", player)
            if ayamedi_difficulty == False:
                m3ay.access_rule = lambda state: (state.count("-1 Minute - Aya", world.player) >= 0)
                m4ay.access_rule = lambda state: (state.count("-1 Minute - Aya", world.player) >= 0)
                m5ay.access_rule = lambda state: (state.count("-1 Minute - Aya", world.player) >= 0)
                m6ay.access_rule = lambda state: (state.count("-1 Minute - Aya", world.player) >= 0)
                m7ay.access_rule = lambda state: (state.count("-1 Minute - Aya", world.player) >= 0)
                m8ay.access_rule = lambda state: (state.count("-1 Minute - Aya", world.player) >= 0)
                m9ay.access_rule = lambda state: (state.count("-1 Minute - Aya", world.player) >= 0)
            else:
                m3ay.access_rule = lambda state: (state.count("-1 Minute - Aya", world.player) >= m1access)
                m4ay.access_rule = lambda state: (state.count("-1 Minute - Aya", world.player) >= m1access)
                m5ay.access_rule = lambda state: (state.count("-1 Minute - Aya", world.player) >= m2access)
                m6ay.access_rule = lambda state: (state.count("-1 Minute - Aya", world.player) >= m2access)
                m7ay.access_rule = lambda state: (state.count("-1 Minute - Aya", world.player) >= m3access)
                m8ay.access_rule = lambda state: (state.count("-1 Minute - Aya", world.player) >= m3access)
                m9ay.access_rule = lambda state: (state.count("-1 Minute - Aya", world.player) >= m4access)
        if enable_medicine == True:
            m3med = multiworld.get_location("[Medicine] VS Tewi - 2:00", player)
            m4med = multiworld.get_location("[Medicine] VS Reimu - 2:00", player)
            m5med = multiworld.get_location("[Medicine] VS Reisen - 4:00", player)
            m6med = multiworld.get_location("[Medicine] VS Sakuya - 4:00", player)
            m7med = multiworld.get_location("[Medicine] VS Yuuka - 6:00", player)
            m8med = multiworld.get_location("[Medicine] VS Komachi - 6:00", player)
            m9med = multiworld.get_location("[Medicine] Finale: VS Shikieiki - 8:00", player)
            if ayamedi_difficulty == False:
                m3med.access_rule = lambda state: (state.count("-1 Minute - Medicine", world.player) >= 0)
                m4med.access_rule = lambda state: (state.count("-1 Minute - Medicine", world.player) >= 0)
                m5med.access_rule = lambda state: (state.count("-1 Minute - Medicine", world.player) >= 0)
                m6med.access_rule = lambda state: (state.count("-1 Minute - Medicine", world.player) >= 0)
                m7med.access_rule = lambda state: (state.count("-1 Minute - Medicine", world.player) >= 0)
                m8med.access_rule = lambda state: (state.count("-1 Minute - Medicine", world.player) >= 0)
                m9med.access_rule = lambda state: (state.count("-1 Minute - Medicine", world.player) >= 0)
            else:
                m3med.access_rule = lambda state: (state.count("-1 Minute - Medicine", world.player) >= m1access)
                m4med.access_rule = lambda state: (state.count("-1 Minute - Medicine", world.player) >= m1access)
                m5med.access_rule = lambda state: (state.count("-1 Minute - Medicine", world.player) >= m2access)
                m6med.access_rule = lambda state: (state.count("-1 Minute - Medicine", world.player) >= m2access)
                m7med.access_rule = lambda state: (state.count("-1 Minute - Medicine", world.player) >= m3access)
                m8med.access_rule = lambda state: (state.count("-1 Minute - Medicine", world.player) >= m3access)
                m9med.access_rule = lambda state: (state.count("-1 Minute - Medicine", world.player) >= m4access)

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
