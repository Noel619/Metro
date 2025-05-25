# Basic structure for a text-based RPG
import random 
import json # For saving and loading
import copy # For deepcopying game state

# --- Game World ---
world = {
    "station_entrance": {
        "description": "You are at the entrance of a dimly lit metro station. Stairs lead down into the darkness. The air is stale and a faint metallic scent hangs in the air. An old man in greasy overalls, Engineer Elias, tinkers with a flickering lamp nearby.",
        "exits": {"down": "platform", "east": "security_checkpoint"},
        "items": ["rusty_pipe"],
        "details": {
            "stairs": "The stairs are made of cracked concrete, disappearing into the gloom below.",
            "lamp": "The lamp sputters, casting dancing shadows. Elias seems focused on fixing it."
        },
        "npcs": {
            "elias": { 
                "name": "Engineer Elias",
                "description": "Engineer Elias is an old but sturdy man. He looks weary but his eyes show a spark of determination.",
                "dialogue": {
                    "greeting": "Hmph. Another wanderer. Most just scavenge these days. Are you looking for something more?",
                    "offer_main_quest": "This old station... it's dying. But there's a communication array in the old Control Room, deep in the tunnels. If someone could reach it, maybe... just maybe, we could send a signal, find out if there's anyone else out there. The way is through the old Engine Room, south of the main platform. Will you try to reach the Control Room?",
                    "quest_accepted": "Good. Be careful. The tunnels are treacherous. Find the Engine Room, which has a door to the Control Room.", # Changed this line
                    "quest_reminder": "You need to get to the Control Room. It should be accessible from the Engine Room.",
                    "quest_completed_already": "You've done well with the array. There's nothing more I can ask of you for that.",
                    "default": "Keep your wits about you in those tunnels."
                },
                "quest_id": "main_comms_array" 
            }
        }
    },
    "platform": {
        "description": "You are on a dusty platform. An old, stationary train rests here. Faint echoes of dripping water can be heard.",
        "exits": {"up": "station_entrance", "train": "train_car", "south": "flooded_tunnel", "west": "market_station"},
        "items": ["old_ticket"]
    },
    "train_car": {
        "description": "You are inside a graffiti-covered train car. The seats are torn and the floor is littered with debris. The doors are jammed open to the platform.",
        "exits": {"platform": "platform"},
        "items": ["newspaper", "empty_bottle"]
    },
    "market_station": {
        "description": "This section of the tunnels has been converted into a makeshift market. Stalls made of scrap metal line the walls, dimly lit by flickering lanterns. A gruff-looking Vendor eyes you from behind a counter.",
        "exits": {"east": "platform", "north": "abandoned_depot"},
        "items": ["ration_pack", "rope"],
        "npcs": {
            "vendor": { # Changed to new NPC structure
                "name": "Vendor",
                "description": "The Vendor is a burly figure with a scarred face. He doesn't say much, just watches your every move.",
                "dialogue": {
                    "greeting": "Need something or just browsing?",
                    "default": "Don't cause any trouble."
                }
                # No quest_id for the vendor for now
            }
        }
    },
    "flooded_tunnel": {
        "description": "Water pools ankle-deep in this tunnel, and the air is damp and cold. Strange fungi glow faintly on the walls. A narrow, slippery walkway skirts the edge of the deeper water. You hear faint skittering sounds and sometimes catch a glimpse of something moving in the shadows.",
        "exits": {"north": "platform", "south": "engine_room"},
        "items": ["glowing_fungus", "scrap_metal"],
        "enemies": [
            {"name": "Giant Rat", "description": "A large, aggressive rodent, common in these tunnels.", "health": 8, "attack_power": 3, "agility": 2, "loot": ["rat_tail"], "xp_value": 25}, # Made loot a list, adjusted XP
            {"name": "Lurker", "description": "A shadowy figure that seems to blend with the dim light. Its eyes glint, and it moves with an unsettling speed, making it hard to get a clear shot.", "health": 35, "attack_power": 6, "loot": ["ammo_scraps", "mutant_claws"], "xp_value": 75}
        ]
    },
    "abandoned_depot": {
        "description": "An old train depot, filled with rusting hulks of metro cars. Cobwebs hang thick as curtains, and the silence is unnerving. A faint scurrying sound and the occasional clatter of metal echoes from deeper within. It feels like you're being watched by desperate eyes.",
        "exits": {"south": "market_station"},
        "items": ["crowbar", "old_map_fragment", "antique_glasses"], 
        "enemies": [
            {"name": "Feral Human Scavenger", "description": "A gaunt Feral Human, darting between shadows, clutching a rusty shiv.", "health": 18, "attack_power": 7, "loot": ["scrap_metal", "bandage"], "xp_value": 45},
            {"name": "Feral Human Bruiser", "description": "A larger, more imposing Feral Human, wielding a heavy pipe with menace.", "health": 25, "attack_power": 9, "loot": ["scrap_metal", "bandage", "moldy_bread"], "xp_value": 60}
        ]
    },
    "security_checkpoint": {
        "description": "A deserted security checkpoint. Barricades are pushed aside, and a guard booth stands empty, its window cracked. Warning posters about mutants are peeling from the walls. Guard Captain Dimitri stands watch, looking grim.",
        "exits": {"west": "station_entrance", "east": "makeshift_library"},
        "items": ["ammo_clip", "first_aid_kit"],
        "npcs": {
            "dimitri": {
                "name": "Guard Captain Dimitri",
                "description": "Dimitri is a stern-faced man in worn guard armor. He has the weary look of someone who's seen too much.",
                "dialogue": {
                    "greeting": "Halt! State your business. This checkpoint is on high alert.",
                    "offer_tunnel_clearing_quest": "The old depot nearby has become a nest for Feral Humans. They're getting bolder, threatening our perimeter. We need someone to go in there and... discourage them. Permanently. Clear out two of them, and I can make it worth your while. Interested?",
                    "quest_accepted": "Good. Watch yourself. They're fast and desperate. Two less of them will make this area safer for everyone.",
                    "quest_reminder_incomplete": "The Feral Human problem in the depot isn't resolved yet. I need you to take down {remaining} more of them.",
                    # "quest_reminder_complete" removed as it's confusing; completion is direct.
                    "completion": "You've thinned out those Ferals? Good work. Not many would take that risk. Here's your payment - a cache of military-grade rounds. And you've earned this.", # Changed reward description
                    "quest_completed_already": "Thanks again for clearing out that nest. Things have been quieter.",
                    "default": "Stay vigilant. The tunnels are never truly safe."
                },
                "quest_id": "tunnel_clearing_quest",
                "reward_item": "cache_of_military_rounds", # Changed to a single item string
                # "reward_item_qty" removed, as it's now a single item.
                "xp_reward": 100
            }
        }
    },
    "engine_room": {
        "description": "The air hums with the sound of ancient generators. The room is hot and filled with the smell of oil and ozone. Catwalks crisscross above massive, chugging machinery. A reinforced door is set into the far wall, marked 'CONTROL ROOM'.",
        "exits": {"north": "flooded_tunnel", "south": "control_room"}, # New exit to control_room
        "items": ["battery", "copper_wire"]
    },
    "makeshift_library": {
        "description": "Someone has turned this quiet alcove into a small library. Shelves made of crates hold a surprisingly large collection of pre-war books. Librarian Agnes, an elderly woman, is meticulously organizing scrolls.",
        "exits": {"west": "security_checkpoint"},
        "items": ["old_book", "reading_glasses"], 
        "npcs": {
            "agnes": { 
                "name": "Librarian Agnes", 
                "description": "Librarian Agnes is a thin, elderly woman with kind eyes. She seems worried about something.",
                "dialogue": {
                    "greeting": "Oh, hello dear. Welcome to our little sanctuary of knowledge.",
                    "offer_side_quest": "I seem to have misplaced my antique reading glasses. They're not very good for reading anymore, but they have... sentimental value. I think I might have left them in the old Abandoned Depot when I was looking for salvage. Could you possibly keep an eye out for them if you're heading that way?",
                    "quest_accepted": "Oh, thank you, dear! That would be wonderful. They are a pair of simple, wire-rimmed glasses.",
                    "quest_reminder": "Have you found my antique glasses? I believe they might be in the Abandoned Depot.",
                    "quest_item_not_found": "Oh, you don't seem to have them with you. Well, do keep looking if you can. I'd be ever so grateful.",
                    "completion": "My glasses! Oh, thank you, thank you! I know they're just old things, but they meant a lot to me. Please, take this valuable book as a token of my gratitude. It's a rare pre-war edition.",
                    "quest_completed_already": "Thank you again for finding my glasses, dear. That book I gave you is quite special."
                },
                "quest_id": "side_librarian_glasses",
                "quest_item_needed": "antique_glasses", 
                "reward_item": "valuable_book",
                "xp_reward": 75  # XP reward for completing this side quest
            }
        },
        "details": {
            "shelves": "The shelves are crammed with books of all kinds, from technical manuals to tattered novels."
        }
    },
    "control_room": {
        "description": "This must be the Control Room Elias mentioned. Dust-covered consoles line the walls, their screens dark. A large central terminal hums faintly. There's a panel here that looks like it could be activated.",
        "exits": {"north": "engine_room"},
        "items": ["circuit_board", "log_entry_1"], # Added a log entry for flavor
        "details": {
            "consoles": "Most consoles are dead, but a few flicker with residual power. One displays a garbled message: '...SYSTEM OFFLINE...AUX_POWER_LOW...MAIN_ARRAY_STATUS: UNKNOWN...'",
            "terminal": "The main terminal seems to be drawing power. A small maintenance hatch is open on its side.",
            "panel": "A large, inviting button on the panel glows faintly green. It's labeled 'COMM_ARRAY_ACTIVATION'."
        },
        "on_enter_event": "main_quest_control_room_entry" # For main quest completion logic in handle_go
    }
}

# --- Player ---
player_inventory = []
player_stats = {
    "name": "Survivor",
    "max_health": 20,
    "current_health": 20,
    "strength": 5, 
    "agility": 3,
    "level": 1,
    "xp": 0,
    "xp_to_next_level": 100,
    "first_aid_skill": 1 # Base first aid skill
}
player_quests = {
    "main_comms_array": "inactive", 
    "side_librarian_glasses": "inactive",
    "tunnel_clearing_quest": "inactive" # Added new quest
}
current_location = "station_entrance"

# --- Enemy Definitions (can be expanded) ---
# Enemies will be placed directly in the location data.
# Example structure for an enemy in a location's 'enemies' list:
# {'name': 'Mutant Rat', 'health': 5, 'attack_power': 2, 'agility': 1, 'loot': 'rat_tail'}


# --- Command Handlers ---
def handle_stats(args):
    """Handles the 'stats' command."""
    print(f"\n--- {player_stats['name']}'s Stats ---")
    print(f"Level: {player_stats['level']}")
    print(f"XP: {player_stats['xp']}/{player_stats['xp_to_next_level']}")
    print(f"Health: {player_stats['current_health']}/{player_stats['max_health']}")
    print(f"Strength: {player_stats['strength']}")
    print(f"Agility: {player_stats['agility']}")
    print(f"First Aid Skill: {player_stats['first_aid_skill']}")
    print("--------------------")

# --- XP and Leveling System ---
def handle_level_up_stat_increase():
    """Allows player to choose a stat to increase upon leveling up."""
    global player_stats
    print("\nCongratulations! You feel more experienced. Choose a stat to improve:")
    print("  1. Vigor (+5 Max Health, heal +5 HP or to full)")
    print("  2. Prowess (+1 Strength)")
    print("  3. Finesse (+1 Agility)")

    while True:
        choice = input("Enter your choice (1-3): ").strip()
        if choice == "1":
            player_stats["max_health"] += 5
            # Heal player by the amount gained, or to full, whichever is less on top of current.
            # More simply, just set current_health to max_health after increase.
            player_stats["current_health"] = player_stats["max_health"] 
            print(f"Your maximum health increased to {player_stats['max_health']}! You feel more resilient and are fully healed.")
            break
        elif choice == "2":
            player_stats["strength"] += 1
            print(f"Your strength increased to {player_stats['strength']}! You feel more powerful.")
            break
        elif choice == "3":
            player_stats["agility"] += 1
            print(f"Your agility increased to {player_stats['agility']}! You feel quicker.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")
    handle_stats([]) # Display updated stats

def check_level_up():
    """Checks if the player has enough XP to level up and handles the process."""
    global player_stats
    if player_stats["xp"] >= player_stats["xp_to_next_level"]:
        player_stats["level"] += 1
        player_stats["xp"] -= player_stats["xp_to_next_level"] # Carry over remaining XP
        player_stats["xp_to_next_level"] = player_stats["level"] * 100 # Example: Next level needs Level * 100 XP
        
        print(f"\n*** LEVEL UP! You reached Level {player_stats['level']}! ***")
        handle_level_up_stat_increase()
        # In case of multiple level ups from a large XP gain, recursively check
        # This is a simple way; a loop in gain_xp would be more robust for massive XP gains.
        check_level_up() 

def gain_xp(amount):
    """Grants XP to the player and triggers a level-up check."""
    global player_stats
    if amount <= 0:
        return
    
    print(f"\nYou gained {amount} XP.")
    player_stats["xp"] += amount
    check_level_up()
# --- End XP and Leveling System ---

def handle_help(args):
    """Handles the 'help' command."""
    print("\n--- Available Commands ---")
    print("  look              - Describe your current location, including items, NPCs, and enemies.")
    print("  look at [thing]   - Describe a specific item, NPC, or detail in your location.")
    print("  go [direction]    - Move in the specified direction (e.g., 'go north').")
    print("  take [item]       - Pick up an item from your location and add it to your inventory.")
    print("  inventory / inv   - Show the items you are currently carrying.")
    print("  stats             - Display your character's current health and attributes.")
    print("  attack [target]   - Attack an enemy in your current location (e.g., 'attack rat').")
    print("  fight [target]    - Alias for 'attack'.")
    print("  talk to [npc]     - Speak with an NPC in your current location (e.g., 'talk to elias').")
    print("  quests / journal  - View the status of your current quests.")
    print("  use [item]        - Use an item from your inventory (e.g., 'use first_aid_kit').")
    print("  save              - Save your current game progress.")
    print("  load              - Load your previously saved game.")
    print("  help              - Show this list of commands.")
    print("  quit / exit       - Exit the game.")
    print("--------------------")

# --- Save/Load Game Functionality ---
SAVE_FILE_NAME = "metro_savegame.json"

def handle_save_game(args):
    """Saves the current game state to a file."""
    global player_stats, player_inventory, current_location, player_quests, world
    
    game_state = {
        "player_stats": copy.deepcopy(player_stats),
        "player_inventory": copy.deepcopy(player_inventory),
        "current_location": current_location, # String, so direct copy is fine
        "player_quests": copy.deepcopy(player_quests),
        "world": copy.deepcopy(world) # Save the entire world state
    }
    
    try:
        with open(SAVE_FILE_NAME, 'w') as f:
            json.dump(game_state, f, indent=4) # indent for readability if opened manually
        print("Game saved.")
    except IOError:
        print("Error: Could not save game.")

def handle_load_game(args):
    """Loads the game state from a file."""
    global player_stats, player_inventory, current_location, player_quests, world
    
    try:
        with open(SAVE_FILE_NAME, 'r') as f:
            game_state = json.load(f)
            
            # Restore game state
            player_stats = game_state["player_stats"]
            player_inventory = game_state["player_inventory"]
            current_location = game_state["current_location"]
            player_quests = game_state["player_quests"]
            world = game_state["world"] # Crucial: restore the modified world
            
            print("\nGame loaded.")
            handle_look([]) # Show current location after loading
    except FileNotFoundError:
        print("No saved game found.")
    except IOError:
        print("Error: Could not load game.")
    except json.JSONDecodeError:
        print("Error: Save file is corrupted.")


# --- Item Usage Handler ---
def handle_use_item(args):
    """Handles the 'use [item]' command."""
    global player_stats
    global player_inventory

    if not args:
        print("Use what? (e.g., 'use first_aid_kit')")
        return

    item_to_use = "_".join(args).lower() # Allow for multi-word items like "first_aid_kit"

    if item_to_use not in player_inventory:
        print(f"You don't have a {item_to_use} in your inventory.")
        return

    if item_to_use == "first_aid_kit":
        if player_stats["current_health"] >= player_stats["max_health"]:
            print("You are already at full health. No need to use a first_aid_kit.")
            return

        base_heal = 15
        skill_bonus = player_stats.get("first_aid_skill", 1) * 5 # Default to skill 1 if somehow not set
        total_heal = base_heal + skill_bonus
        
        healed_amount = 0
        if player_stats["current_health"] + total_heal > player_stats["max_health"]:
            healed_amount = player_stats["max_health"] - player_stats["current_health"]
            player_stats["current_health"] = player_stats["max_health"]
        else:
            healed_amount = total_heal
            player_stats["current_health"] += total_heal
            
        player_inventory.remove("first_aid_kit") # Remove one kit
        print(f"You used a first_aid_kit and healed for {healed_amount} HP.")
        print(f"Your current health is now {player_stats['current_health']}/{player_stats['max_health']}.")
    
    
    elif item_to_use == "bandage":
        if player_stats["current_health"] >= player_stats["max_health"]:
            print("You are already at full health. No need to use a bandage.")
            return
        
        heal_amount = 10 # Bandages heal a fixed amount
        
        actual_healed = 0
        if player_stats["current_health"] + heal_amount > player_stats["max_health"]:
            actual_healed = player_stats["max_health"] - player_stats["current_health"]
            player_stats["current_health"] = player_stats["max_health"]
        else:
            actual_healed = heal_amount
            player_stats["current_health"] += heal_amount
            
        player_inventory.remove("bandage")
        print(f"You apply a bandage and heal for {actual_healed} HP.")
        print(f"Your current health is now {player_stats['current_health']}/{player_stats['max_health']}.")

    # Example for ration_pack if it becomes usable
    # elif item_to_use == "ration_pack":
    #     print("You eat the ration pack. It's not great, but it's filling.")
    #     # Potentially restore a small amount of health or hunger if that was a mechanic
    #     player_inventory.remove("ration_pack")
    #     # gain_xp(5) # Small XP for using an item? (Optional)

    else:
        print(f"You can't use the {item_to_use} in that way (or it's not usable).")


def handle_quests(args):
    """Handles the 'quests' or 'journal' command."""
    global player_quests
    print("\n--- Your Quests ---")
    active_quests_found = False
    completed_quests_found = False

    # Main Quest: Comms Array
    if player_quests.get("main_comms_array") == "active":
        print("- (Active) The Signal: Reach the Control Room to investigate the old communication array. Elias mentioned it's accessible via the Engine Room.")
        active_quests_found = True
    elif player_quests.get("main_comms_array") == "completed":
        print("- (Completed) The Signal: You reached the Control Room and activated the communication array panel.")
        completed_quests_found = True
    
    # Side Quest: Librarian's Glasses
    if player_quests.get("side_librarian_glasses") == "active":
        print("- (Active) Lost & Found: Find Librarian Agnes's antique_glasses. She thinks they are in the Abandoned Depot.")
        active_quests_found = True
    elif player_quests.get("side_librarian_glasses") == "completed":
        print("- (Completed) Lost & Found: You returned the antique_glasses to Librarian Agnes and received a valuable_book.")
        completed_quests_found = True

    # Tunnel Clearing Quest
    tunnel_quest_data = player_quests.get("tunnel_clearing_quest")
    if isinstance(tunnel_quest_data, dict): # Quest is active or completed and has data
        defeated = tunnel_quest_data.get('humans_defeated', 0)
        required = tunnel_quest_data.get('humans_required', 2)
        if tunnel_quest_data.get('status') == "active":
            print(f"- (Active) Tunnel Clearing: Defeat Feral Humans in the Abandoned Depot for Captain Dimitri. ({defeated}/{required} defeated)")
            active_quests_found = True
        elif tunnel_quest_data.get('status') == "completed":
            print(f"- (Completed) Tunnel Clearing: You cleared out the Feral Humans for Captain Dimitri.")
            completed_quests_found = True
    elif tunnel_quest_data == "inactive": # Standard inactive string state
        # Not usually shown unless no other quests are active/completed
        pass


    if not active_quests_found and not completed_quests_found:
        # Check if there are any quests at all, even if all are inactive
        if any(status == "inactive" for status in player_quests.values()):
             print("You have potential quests available. Try talking to people in the stations.")
        else: # This case should ideally not be hit if quests are defined
            print("You have no quests at this time.")
    elif not active_quests_found and completed_quests_found:
        print("You have no active quests, only completed ones.")
    elif active_quests_found and not completed_quests_found:
        pass # Already printed active quests
    # If both are true, both sections are printed.
    print("--------------------")

def handle_look(args):
    """Handles the 'look' command."""
    global current_location
    global player_quests
    location_data = world.get(current_location)
    if not location_data:
        print("Error: Unknown location!")
        return

    print(location_data["description"])

    if location_data.get("npcs"):
        for npc_id, npc_data_val in location_data["npcs"].items():
            if isinstance(npc_data_val, dict): # New NPC structure
                npc_name_display = npc_data_val.get("name", npc_id.capitalize())
                base_desc = npc_data_val.get("description", f"You see {npc_name_display}.")
                
                quest_hint = ""
                npc_quest_id = npc_data_val.get("quest_id")
                # Only show "wants to talk" hint if there's an actual quest to offer
                dialogues = npc_data_val.get("dialogue", {})
                has_offer_dialogue = any(key.startswith("offer_") for key in dialogues)

                if npc_quest_id and player_quests.get(npc_quest_id) == "inactive" and has_offer_dialogue:
                    quest_hint = f" {npc_name_display} looks like they might want to talk. (Try 'talk to {npc_id}')"
                print(base_desc + quest_hint)
            else: # Old format NPC description (just a string)
                print(f"You see {npc_id.capitalize()}. {npc_data_val}") # Should be less common now

    if location_data.get("enemies"):
        print("Enemies present:")
        for enemy in location_data["enemies"]:
            enemy_name = enemy.get('name', 'Unknown Enemy')
            enemy_health = enemy.get('health', 'N/A')
            print(f"- {enemy_name} (Health: {enemy_health})")

    if location_data.get("items"):
        print("Items here: " + ", ".join(location_data["items"]))
    else:
        print("You see no items here.")

    available_exits = ", ".join(location_data["exits"].keys())
    if available_exits:
        print(f"Exits: {available_exits}")
    else:
        print("There are no obvious exits.")

    # Placeholder for looking at specific details
    if len(args) > 0 and args[0] == "at":
        if len(args) > 1:
            detail_name = args[1].lower() # e.g. "elias" or "stairs"
            if "details" in location_data and detail_name in location_data["details"]:
                print(location_data["details"][detail_name])
            # Looking AT an NPC
            elif "npcs" in location_data and detail_name in location_data["npcs"]:
                npc_data_val = location_data["npcs"][detail_name]
                if isinstance(npc_data_val, dict):
                    npc_name_display = npc_data_val.get("name", detail_name.capitalize())
                    desc = npc_data_val.get("description", f"You see {npc_name_display}.")
                    
                    quest_hint = ""
                    npc_quest_id = npc_data_val.get("quest_id")
                    if npc_quest_id: # Check if NPC is related to any quest
                        quest_status = player_quests.get(npc_quest_id, "unavailable")
                        if quest_status == "inactive":
                            quest_hint = f" They seem to want to discuss something. (Try 'talk to {detail_name}')"
                        elif quest_status == "active":
                            quest_hint = f" You have an ongoing task for them."
                        elif quest_status == "completed":
                            quest_hint = f" You've already helped them."
                    print(desc + quest_hint)
                else: # Old format
                    print(npc_data_val) # Show original string desc
            elif "items" in location_data and detail_name in location_data["items"]:
                 print(f"It's a {detail_name}.") 
            else:
                print(f"You don't see any specific details about '{detail_name}' here.")
        else:
            print("Look at what?")


def handle_talk(args):
    """Handles the 'talk to [npc]' command."""
    global current_location
    global player_quests
    global player_inventory # Needed for quest item checks & rewards

    if not args:
        print("Talk to whom?")
        return

    npc_target_name_part = args[0].lower()
    location_data = world.get(current_location)

    if not location_data.get("npcs"):
        print("There's no one to talk to here.")
        return

    found_npc_id = None
    npc_data_to_use = None 

    for current_npc_id, current_npc_data_val in location_data["npcs"].items():
        if npc_target_name_part in current_npc_id.lower(): # e.g. "elias" in "elias"
            if isinstance(current_npc_data_val, dict): # Make sure we're dealing with new NPC structure
                found_npc_id = current_npc_id
                npc_data_to_use = current_npc_data_val
                break
            else: # Should not happen if all NPCs are converted
                print(f"DEBUG: NPC {current_npc_id} is not in the new format.") 
                return
    
    if not npc_data_to_use:
        print(f"You don't see anyone called '{npc_target_name_part}' here to talk to like that.")
        return

    npc_display_name = npc_data_to_use.get("name", found_npc_id.capitalize())
    dialogue = npc_data_to_use.get("dialogue", {})
    quest_id = npc_data_to_use.get("quest_id")
    
    print(f"\nYou approach {npc_display_name}.")

    if quest_id: # NPC is related to a quest
        quest_status = player_quests.get(quest_id, "unavailable") 

        if quest_status == "inactive":
            offer_dialogue_key = None
            # Generalized way to find offer dialogue key
            for key in dialogue:
                if key.startswith("offer_") and quest_id in key : # e.g. "offer_main_comms_array_quest" or "offer_tunnel_clearing_quest"
                     # Simplified: assume quest_id is part of the offer key or directly "offer_main_quest", "offer_side_quest"
                    if quest_id == "main_comms_array" and key == "offer_main_quest": offer_dialogue_key = key; break
                    if quest_id == "side_librarian_glasses" and key == "offer_side_quest": offer_dialogue_key = key; break
                    if quest_id == "tunnel_clearing_quest" and key == "offer_tunnel_clearing_quest": offer_dialogue_key = key; break
            
            if offer_dialogue_key:
                print(f"{npc_display_name}: \"{dialogue[offer_dialogue_key]}\"")
                accept_input = input(f"Help {npc_display_name}? (yes/no): ").strip().lower()
                if accept_input == "yes" or accept_input == "y":
                    if quest_id == "tunnel_clearing_quest":
                        player_quests[quest_id] = {'status': 'active', 'humans_defeated': 0, 'humans_required': 2}
                    else:
                        player_quests[quest_id] = "active"
                    print(f"{npc_display_name}: \"{dialogue.get('quest_accepted', 'Thank you! Your help is appreciated.')}\"")
                else:
                    print(f"{npc_display_name}: \"{dialogue.get('quest_declined', 'Oh, alright then. Let me know if you change your mind.')}\"")
            else: 
                 print(f"{npc_display_name}: \"{dialogue.get('greeting', 'They look at you but say little.')}\"")
        
        elif quest_status == "active" or (isinstance(quest_status, dict) and quest_status.get('status') == "active"):
            # Side quest: Librarian's Glasses
            if quest_id == "side_librarian_glasses" and npc_data_to_use.get("quest_item_needed"):
                item_needed = npc_data_to_use["quest_item_needed"]
                if item_needed in player_inventory:
                    print(f"{npc_display_name}: \"{dialogue.get('completion', 'You found it! Amazing!')}\"")
                    player_inventory.remove(item_needed)
                    print(f"(You hand over the {item_needed}.)")
                    reward = npc_data_to_use.get("reward_item")
                    if reward: player_inventory.append(reward); print(f"You received a {reward} as a reward!")
                    player_quests[quest_id] = "completed"
                    quest_xp_reward = npc_data_to_use.get("xp_reward", 0)
                    if quest_xp_reward > 0: gain_xp(quest_xp_reward)
                else:
                    print(f"{npc_display_name}: \"{dialogue.get('quest_item_not_found', 'Still looking for it?')}\"")
            
            # New Quest: Tunnel Clearing
            elif quest_id == "tunnel_clearing_quest":
                current_quest_data = player_quests.get(quest_id, {}) # This will be the dict {'status': ..., 'humans_defeated': ...}
                defeated = current_quest_data.get('humans_defeated', 0)
                required = current_quest_data.get('humans_required', 2)
                
                if defeated >= required: # Player has met kill condition
                    print(f"{npc_display_name}: \"{dialogue.get('completion', 'Excellent work clearing them out!')}\"")
                    
                    reward_item_name = npc_data_to_use.get("reward_item")
                    if reward_item_name: # Check if there is a reward item defined
                        # No quantity handling needed now, just add the single item name
                        player_inventory.append(reward_item_name)
                        print(f"You received {reward_item_name}.")
                    
                    quest_xp = npc_data_to_use.get("xp_reward", 0)
                    if quest_xp > 0: gain_xp(quest_xp)
                    
                    # Update quest status within its dictionary
                    current_quest_data['status'] = "completed" 
                    # No need to reassign player_quests[quest_id] if current_quest_data is a direct reference
                else: # Player has not met kill condition yet
                    remaining = required - defeated
                    reminder_text = dialogue.get('quest_reminder_incomplete', "Still work to do.").format(remaining=remaining, defeated=defeated, required=required) # Ensure .format() is robust
                    print(f"{npc_display_name}: \"{reminder_text}\"")

            # Main Quest Reminder
            elif quest_id == "main_comms_array":
                 print(f"{npc_display_name}: \"{dialogue.get('quest_reminder', 'How is it going?')}\"")
            else: 
                print(f"{npc_display_name}: \"{dialogue.get('quest_reminder', 'How is that task coming along?')}\"")
        
        elif quest_status == "completed" or (isinstance(quest_status, dict) and quest_status.get('status') == "completed"):
            print(f"{npc_display_name}: \"{dialogue.get('quest_completed_already', 'Thanks again for your help!')}\"")
        
        else: # Should not happen if quests are initialized correctly
            print(f"{npc_display_name}: \"{dialogue.get('default', 'Nothing more to say right now.')}\"")
    else: # NPC has no quest_id
        print(f"{npc_display_name}: \"{dialogue.get('greeting', dialogue.get('default', 'They nod at you.'))}\"")


def handle_go(args):
    """Handles the 'go' command."""
    global current_location
    global player_quests # Needed for quest events on room entry
    if not args:
        print("Go where?")
        return

    direction = args[0].lower()
    current_room_data = world.get(current_location) # Data of the room we are IN

    if current_room_data and direction in current_room_data["exits"]:
        next_location_id = current_room_data["exits"][direction]
        if next_location_id in world:
            current_location = next_location_id
            print(f"\nYou go {direction}...") # Added newline for better spacing
            
            # --- Main Quest Completion Check ---
            new_location_data = world.get(current_location) # Data for the new room player entered
            if new_location_data and new_location_data.get("on_enter_event") == "main_quest_control_room_entry":
                if player_quests.get("main_comms_array") == "active":
                    print("\n[QUEST COMPLETED] As you step into the Control Room, a panel on the main terminal flickers to life with a soft green glow. You've successfully activated the communication array panel!")
                    print("Elias will be pleased to hear the station's core systems are responsive again.")
                    player_quests["main_comms_array"] = "completed"
                    gain_xp(150) # Grant 150 XP for completing the main quest
                    # To prevent re-triggering, we rely on the quest status check.
            
            handle_look([]) # Automatically look around after moving
        else:
            print(f"Error: The path {direction} leads to an unknown place.")
    else:
        print(f"You can't go {direction}.")


def handle_attack(args):
    """Handles the 'attack' command."""
    global current_location
    global player_stats
    # No need to pass 'world' as global, it's already accessible

    location_data = world.get(current_location)
    if not location_data or not location_data.get("enemies"):
        print("There's nothing to attack here.")
        return

    if not args:
        print("Attack what? (e.g., 'attack rat')")
        return

    target_name_part = args[0].lower()
    target_enemy = None
    enemy_index = -1

    # Find the enemy
    # Allow targeting by full name or parts of it, case insensitively
    # Also, if multiple enemies of same type, target first one found.
    # This could be improved to target specific instances if names are not unique (e.g. "rat 1", "rat 2")
    for i, enemy_data in enumerate(location_data["enemies"]):
        if target_name_part in enemy_data["name"].lower():
            target_enemy = enemy_data
            enemy_index = i
            break
    
    if not target_enemy:
        print(f"You don't see any '{target_name_part}' to attack here.")
        return

    # --- Combat Round ---
    enemy_name_display = target_enemy.get("name", "Mysterious Foe")
    print(f"\n--- Combat with {enemy_name_display} ---")

    # Player's attack
    player_damage = player_stats["strength"] 
    target_enemy["health"] -= player_damage
    print(f"You strike the {enemy_name_display} for {player_damage} damage.")

    if target_enemy["health"] <= 0:
        print(f"You defeated the {enemy_name_display}!")
        
        # Quest Kill Tracking
        if "feral human" in enemy_name_display.lower(): # Check if it's any type of Feral Human
            tunnel_quest = player_quests.get("tunnel_clearing_quest")
            if isinstance(tunnel_quest, dict) and tunnel_quest.get("status") == "active":
                tunnel_quest["humans_defeated"] = tunnel_quest.get("humans_defeated", 0) + 1
                print(f"[Quest Update] Feral Humans defeated: {tunnel_quest['humans_defeated']}/{tunnel_quest['humans_required']}")

        # Handle Loot Drop
        possible_loot = target_enemy.get("loot")
        if possible_loot:
            dropped_item = None
            if isinstance(possible_loot, list) and possible_loot: 
                dropped_item = random.choice(possible_loot)
            elif isinstance(possible_loot, str): 
                dropped_item = possible_loot
            
            if dropped_item:
                if "items" not in location_data: 
                    location_data["items"] = []
                location_data["items"].append(dropped_item)
                print(f"The {enemy_name_display} dropped a {dropped_item}.")
        
        location_data["enemies"].pop(enemy_index) 
        
        if not location_data["enemies"]: 
            del location_data["enemies"] 
        
        xp_from_enemy = target_enemy.get("xp_value", 0)
        if xp_from_enemy > 0:
            gain_xp(xp_from_enemy)
            
        return 

    # Enemy's attack (if still alive)
    # Basic hit chance (optional, can be expanded)
    # For now, enemy always hits if player didn't defeat it.
    enemy_damage = target_enemy["attack_power"]
    player_stats["current_health"] -= enemy_damage
    print(f"The {target_enemy['name']} retaliates, hitting you for {enemy_damage} damage.")

    if player_stats["current_health"] <= 0:
        player_stats["current_health"] = 0 # Prevent negative health display
        print(f"Your health: {player_stats['current_health']}/{player_stats['max_health']}.")
        print("\nYou have succumbed to your wounds. Your adventure ends here.")
        print("Game Over.")
        # The main game loop will catch the zero health and exit.
    else:
        print(f"Your health: {player_stats['current_health']}/{player_stats['max_health']}.")
    print("--------------------")


def handle_take(args):
    """Handles the 'take' command."""
    global current_location
    global player_inventory
    if not args:
        print("Take what?")
        return

    item_name = args[0].lower()
    location_data = world.get(current_location)

    if location_data and item_name in location_data["items"]:
        player_inventory.append(item_name)
        location_data["items"].remove(item_name)
        print(f"You take the {item_name}.")
    else:
        print(f"You don't see a {item_name} here.")

def handle_inventory(args):
    """Handles the 'inventory' command."""
    global player_inventory
    if player_inventory:
        print("You are carrying: " + ", ".join(player_inventory))
    else:
        print("Your inventory is empty.")

def handle_quit(args):
    """Handles the 'quit' command."""
    print("Thanks for playing!")
    exit()

# --- Command Parser ---
commands = {
    "look": handle_look,
    "go": handle_go,
    "take": handle_take,
    "inventory": handle_inventory,
    "stats": handle_stats,
    "attack": handle_attack,
    "fight": handle_attack, # Alias for attack
    "quests": handle_quests,
    "journal": handle_quests, # Alias for quests
    "talk": handle_talk,
    "help": handle_help,
    "use": handle_use_item,
    "save": handle_save_game, # New command
    "load": handle_load_game, # New command
    "quit": handle_quit,
    "exit": handle_quit # Alias for quit
}

# --- Main Game Loop ---
def game_loop():
    """Main loop for the game."""
    global player_stats # Ensure we can modify the global player_stats

    print("Welcome to the Metro Adventure Game!")
    
    # Character Creation
    player_name = input("Enter your character's name (default: Survivor): ").strip()
    if player_name:
        player_stats["name"] = player_name
    
    # Initialize stats 
    player_stats["name"] = player_name 
    player_stats["level"] = 1
    player_stats["xp"] = 0
    player_stats["xp_to_next_level"] = 100 
    player_stats["max_health"] = 20
    player_stats["current_health"] = player_stats["max_health"] 
    player_stats["strength"] = 5
    player_stats["agility"] = 3
    player_stats["first_aid_skill"] = 1 # Initialize first aid skill

    # Initialize Quests
    global player_quests
    player_quests = {
        "main_comms_array": "inactive", 
        "side_librarian_glasses": "inactive",
        "tunnel_clearing_quest": "inactive" # Initialize new quest
    }
    
    print(f"\nWelcome, {player_stats['name']}! Your adventure begins.")
    handle_stats([]) # Show initial stats
    # Initial hint for main quest
    print("\nEngineer Elias, in the station entrance, looks like he has something important to tell you. (Try 'talk to elias')") 
    
    handle_look([]) # Initial look around

    while True:
        # Check for game over condition at the start of each loop iteration
        if player_stats["current_health"] <= 0:
            # This check ensures game ends if health drops to 0 outside of direct combat loop
            # (e.g. future traps or poison)
            # Message is printed by handle_attack or other future damage sources
            break # Exit the main game loop

        try:
            # Update prompt to show current health
            prompt = f"\n({player_stats['current_health']}/{player_stats['max_health']} HP) > "
            player_input = input(prompt).strip().lower()
            if not player_input:
                continue

            parts = player_input.split()
            command = parts[0]
            args = parts[1:]

            if command in commands:
                commands[command](args)
            else:
                print("Unknown command. Type 'help' for a list of commands.") # Updated help hint
        except EOFError:
            print("\nQuitting game (EOF detected).")
            break
        except KeyboardInterrupt:
            print("\nQuitting game (interrupt signal).")
            break

if __name__ == "__main__":
    game_loop()
