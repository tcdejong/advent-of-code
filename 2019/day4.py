num_digits = 6


def meetsCriteria(password, part=1):

    pwdAsList = []
    critNeverDecreases = True
    critSameAdjacent = False

    for i in range(num_digits-1, -1, -1):
        cur = password // (10 ** i)
        if len(pwdAsList) > 0:
            if cur < pwdAsList[-1]:
                critNeverDecreases = False
            elif part == 1 and cur == pwdAsList[-1]:
                critSameAdjacent = True

        password -= cur * (10 ** i)
        pwdAsList.append(cur)

    # A password of length i has (i-1) adjacent digits
    # check if digit i and i+1 form a pair
    if part == 2:
        for i in range(num_digits - 1):
            if i == 0:
                if pwdAsList[i] == pwdAsList[i+1] != pwdAsList[i+2]:
                    critSameAdjacent = True
                    break
            elif i == (num_digits - 2):
                if pwdAsList[i-1] != pwdAsList[i] == pwdAsList[i+1]:
                    critSameAdjacent = True
                    break
            elif pwdAsList[i-1] != pwdAsList[i] == pwdAsList[i+1] != pwdAsList[i+2]:
                critSameAdjacent = True
                break

    return (critSameAdjacent and critNeverDecreases)


def day4(lbound, rbound, part):

    validPasswords = []
    for pwd in range(lbound, rbound):
        if meetsCriteria(pwd, part):
            validPasswords.append(pwd)

    return len(validPasswords)


print(day4(168630, 718098, 1))
print(day4(168630, 718098, 2))

# print(list(str(123456)))
