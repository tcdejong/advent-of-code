def read_data():
    with open('day6.txt') as file:
        return file.read().split('\n\n')


def part_one():
    data = read_data()
    group_answer_count = (len(set(answers.replace('\n',""))) for answers in data)
    print(sum(n for n in group_answer_count))
    

def part_two():
    data = read_data()
    
    res = 0

    for group_answers in data:
        answers = group_answers.strip().splitlines()

        if len(answers) == 1:
            res += len(answers[0])
            continue

        for answer in answers[0]:
            if all(answer in individual_answers for individual_answers in answers[1:]):
                res += 1

    print(res)




if __name__ == '__main__':
    part_one()
    part_two()