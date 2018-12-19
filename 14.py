#!/usr/bin/python

# 2018-12-19 thehungryturnip@gmail.com

import sys

if __name__ == '__main__':
    recipe_min = int(sys.argv[1])
    print(f'recipe min: {recipe_min}')

    recipes = [3, 7]
    index_0 = 0
    index_1 = 1
    
    def create_new_recipes(recipes, index_0, index_1):
        new_recipes = recipes[index_0] + recipes[index_1]
        if new_recipes >= 10:
            recipes.append(1)
            new_recipes -= 10
        recipes.append(new_recipes)

    def get_next_index(recipes, index):
        index += recipes[index] + 1
        while index >= len(recipes):
            index -= len(recipes)
        return index

    while len(recipes) < recipe_min + 10:
        create_new_recipes(recipes, index_0, index_1)
        index_0 = get_next_index(recipes, index_0)
        index_1 = get_next_index(recipes, index_1)

    next_10 = ''.join([str(r) for r in recipes[recipe_min:recipe_min + 10]])
    print(f'[14a] The next 10 scroes after {recipe_min} are {next_10}')
