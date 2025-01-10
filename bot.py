import math

from game_message import *
import numpy as np
import random


class Bot:
    def __init__(self):
        print("Initializing your super mega duper bot")
        self.wall_positions = []

    def get_next_move(self, game_message: TeamGameState):
        """
        Here is where the magic happens, for now the moves are not very good. I bet you can do better ;)
        """
        actions = []

        if game_message.tick == 1:
            for line in range(len(game_message.map.tiles)):
                for column in range(len(game_message.map.tiles[line])):
                    if game_message.map.tiles[line][column] == TileType.WALL:
                        self.wall_positions.append((line, column))

        print(self.wall_positions)

        grid = np.zeros((game_message.map.width, game_message.map.height))
        grid_size = (game_message.map.width, game_message.map.height)

        enemy_position = []
        for threat in game_message.threats:
            enemy_position.append((threat.position.x, threat.position.y))

        for wall in self.wall_positions:
            grid[wall] = -1

        max_distance = 2

        for enemy in enemy_position:
            enemy_row, enemy_col = enemy
            for i in range(grid_size[0]):
                for j in range(grid_size[1]):
                    if grid[i, j] == -1:
                        continue

                    distance = np.sqrt((enemy_row - i) ** 2 + (enemy_col - j) ** 2)

                    if distance <= max_distance:
                        grid[i, j] += max(0, max_distance - distance)

        print(grid)

        grid_zeros = []
        min_value = math.inf
        min_case = ()

        for i in range(grid_size[0]):
            for j in range(grid_size[1]):
                if grid[i, j] == -1:
                    continue

                if grid[i, j] == 0:
                    grid_zeros.append((i, j))
                elif grid[i, j] < min_value:
                    min_value = grid[i, j]
                    min_case = (i, j)

        if len(grid_zeros) != 0:
            actions.append(MoveToAction(Position(grid_zeros[0][0], grid_zeros[0][1])))
        else:
            actions.append(MoveToAction(Position(min_case[0], min_case[1])))

        # You can clearly do better than the random actions above! Have fun!
        return actions
