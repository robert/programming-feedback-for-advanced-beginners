EXTRA_POWER_NEEDED_TO_DEFEAT_ENEMY = 5

def player_has_enough_power_to_defeat_enemy(player_stats, enemy_stats):
    # Subtract the enemy power from the
    # player power and make sure that
    # the difference is more than 5.
    player_stats['power'] = player_stats['power'] - enemy_stats['power']

    if player_stats['power'] > EXTRA_POWER_NEEDED_TO_DEFEAT_ENEMY:
        return True
    else:
        return False

if __name__ == "__main__":
    # In our game, the player defeats an
    # enemy if they have more than
    # 5 greater power than the enemy.
    player_stats = {
        'name': 'Horatio',
        'power': 35,
    }

    enemy1_stats = {
        'name': 'Death Face',
        'power': 27,
    }
    enemy2_stats = {
        'name': 'Brain Eater',
        'power': 20,
    }

    # TODO: since our player has more than
    # 5 extra power than both Death Face
    # and Brain Eater, we expect them to
    # defeat both enemies. However, this
    # is not happening! We should figure
    # out what the bug is and fix it.
    if player_has_enough_power_to_defeat_enemy(player_stats, enemy1_stats):
        print("Player DEFEATS Enemy 1!")
    else:
        print("Player LOSES to Enemy 1!")
        exit(0)

    if player_has_enough_power_to_defeat_enemy(player_stats, enemy2_stats):
        print("Player DEFEATS Enemy 2!")
    else:
        print("Player LOSES to Enemy 2!")
        exit(0)
