from risk.game_setup import setup_new_game

def main():
    """
    Main function to run the Risk game.
    """
    print("--- Setting up a new game of Risk ---")
    game_map, players = setup_new_game()

    print("\n--- Initial Game State ---")
    print(f"Players: {[player.name for player in players]}")

    print("\nTerritories:")
    for territory_name in sorted(game_map.territories.keys()):
        territory = game_map.get_territory(territory_name)
        print(f"- {territory}")

    print("\n--- Game setup complete ---")

if __name__ == "__main__":
    main()
