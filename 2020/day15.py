from collections import defaultdict

def numbers_game(numbers: list[int], end_turn = 2020) -> int:
    numbers = [i for i in numbers]
    last_spoken = defaultdict(lambda: (-1,-1))
    number = -1
    turn = 1

    for turn in range(1, end_turn + 1):
        if numbers:
            number = numbers.pop(0)

        elif number in last_spoken:
            forelast, last = last_spoken[number]
            number = 0 if forelast == -1 else last - forelast
        
        forelast, last = last_spoken[number]
        last_spoken[number] = (last, turn)
    
    return number


if __name__ == '__main__':
    numbers = [19,20,14,0,9,1]

    assert numbers_game([0,3,6], 10) == 0
    assert numbers_game([1,3,2]) == 1
    assert numbers_game([2,1,3]) == 10
    assert numbers_game([1,2,3]) == 27
    assert numbers_game([2,3,1]) == 78
    assert numbers_game([3,2,1]) == 438
    assert numbers_game([3,1,2]) == 1836

    print(numbers_game(numbers))
    print(numbers_game(numbers, 30000000))