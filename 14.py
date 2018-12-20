#!/usr/bin/python

# 2018-12-19 thehungryturnip@gmail.com

import sys

if __name__ == '__main__':
    target = sys.argv[1]
    print(f'recipe min: {target}')

    recipes = [3, 7]
    index_0 = 0
    index_1 = 1
    
    def create_new_recipes(recipes, index_0, index_1):
        new_recipes = recipes[index_0] + recipes[index_1]
        # assumes that recipe scores are between 0 and 18
        if new_recipes >= 10:
            recipes.append(1)
            new_recipes -= 10
        recipes.append(new_recipes)

    def get_next_index(recipes, index):
        index += recipes[index] + 1
        while index >= len(recipes):
            index -= len(recipes)
        return index

    while len(recipes) < int(target) + 10:
        create_new_recipes(recipes, index_0, index_1)
        index_0 = get_next_index(recipes, index_0)
        index_1 = get_next_index(recipes, index_1)

    next_10 = ''.join([str(r) for r in recipes[int(target):int(target) + 10]])
    print(f'[14a] The next 10 scroes after {int(target)} are {next_10}')

    recipes = [3, 7]
    index_0 = 0
    index_1 = 1
    
    # not the most efficient search:
    # 1. in many cases could be checking once instead of twice
    # 2. could be reusing previous search string
    def check_2(target, recipes):
        if len(target) > len(recipes):
            return None
        index_start = len(recipes) - len(target) - 1
        index_end = index_start + len(target)
        compare_to = ''.join([str(r) for r in recipes[index_start:index_end]])
        if target == compare_to:
            return index_start
        if target == compare_to[1:] + str(recipes[index_end]):
            return index_start + 1
        return None

    target_found_at = None
    while not target_found_at:
        create_new_recipes(recipes, index_0, index_1)
        index_0 = get_next_index(recipes, index_0)
        index_1 = get_next_index(recipes, index_1)
        target_found_at = check_2(target, recipes)

    print(f'[14b] The target {target} is found after {target_found_at}' +
          ' recipes.')
