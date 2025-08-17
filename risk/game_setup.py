from risk.models import Player, Territory, Map

def setup_new_game():
    """
    Sets up a new game with a simple map, players, and initial army distribution.
    """
    # 1. Create players
    player1 = Player("Player 1")
    player2 = Player("Player 2")
    players = [player1, player2]

    # 2. Create territories
    t1 = Territory("Westeros")
    t2 = Territory("Essos")
    t3 = Territory("Sothoryos")
    t4 = Territory("Ulthos")

    all_territories = [t1, t2, t3, t4]

    # 3. Create map and add territories
    game_map = Map()
    for territory in all_territories:
        game_map.add_territory(territory)

    # 4. Add connections
    game_map.add_connection("Westeros", "Essos")
    game_map.add_connection("Essos", "Sothoryos")
    game_map.add_connection("Sothoryos", "Westeros")
    game_map.add_connection("Essos", "Ulthos")

    # 5. Assign territories and armies
    t1.owner = player1
    t1.armies = 5
    player1.territories.append(t1)

    t2.owner = player2
    t2.armies = 5
    player2.territories.append(t2)

    t3.owner = player1
    t3.armies = 3
    player1.territories.append(t3)

    t4.owner = player2
    t4.armies = 3
    player2.territories.append(t4)

    return game_map, players
