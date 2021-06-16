def do_math(expression:str, part=1) -> int:
    # substitute parenthesized terms with their result
    # while r := expression.find(')') != -1:
    while expression.find('(') != -1:
        # find inner expression based on first closing paren
        r = expression.find(')')
        l = expression[:r].rfind('(')

        # solve inner expression
        inner = expression[l+1:r]
        sub = solve_simple(inner, part)

        # substitute solution in the expression
        expression = expression[:l] + str(sub) + expression[r+1:]


    # solve remaining expression
    return solve_simple(expression, part)


def solve_simple(expression: str, part=1) -> int:
    """
    Solve a mathematical expression from left to right, 
    ignoring operator precedence in p1 and doing inverted in p2
    """
    assert expression.find('(') == -1
    assert expression.find(')') == -1

    expression = expression.split(' ')

    if part == 1:
        # Deviating first case: read left hand side
        left, *expression = expression
        left = int(left)

        while expression:
            op, right, *expression = expression
            right = int(right)

            if op == '+':
                left = left + right
            elif op == '*':
                left = left * right
            else:
                raise NotImplementedError('Op not implemented in solve_simple!')

            # print(left, expression)
        
        return left


    elif part==2:
        # Solve all + operations first, then use p1 for remainder.
        while '+' in expression:
            i = expression.index('+')
            l = int(expression[i - 1])
            r = int(expression[i + 1])

            res = str(l + r)
            
            if len(expression) == 3:
                break
                
            expression = [*expression[:i-1], res, *expression[i+2:]]

        expression = ' '.join(expression)
        return solve_simple(expression)

            



def part_one():
    with open('day18.txt') as f:
        return sum(do_math(line.strip()) for line in f.readlines())


def part_two():
    with open('day18.txt') as f:
        return sum(do_math(line.strip(), part=2) for line in f.readlines())


def tests():
    assert solve_simple('1 + 2 * 3 + 4 * 5 + 6') == 71

    assert do_math('1 + (2 * 3) + (4 * (5 + 6))') == 51
    assert do_math('2 * 3 + (4 * 5)') == 26
    assert do_math('5 + (8 * 3 + 9 + 3 * 4 * 3)') == 437
    assert do_math('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))') == 12240
    assert do_math('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2') == 13632

    print('Passed assertions for P1!')


    assert solve_simple('1 + 2 * 3 + 4 * 5 + 6', part=2) == 231

    assert do_math('1 + (2 * 3) + (4 * (5 + 6))', part=2) == 51
    assert do_math('2 * 3 + (4 * 5)', part=2) == 46
    assert do_math('5 + (8 * 3 + 9 + 3 * 4 * 3)', part=2) == 1445
    assert do_math('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))', part=2) == 669060
    assert do_math('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', part=2) == 23340

    print('Passed assertions for P2!')
