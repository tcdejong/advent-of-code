NUM_DIGITS = 6
ERR_DESCENDING = -1
ERR_NO_GROUP = -2
OK = 1

def meetsCriteria(password, part=1):
    digits = [int(i) for i in str(password)]

    last = -1
    groups = set()
    groupLen = 1

    for d in digits:
        if d < last:
            return ERR_DESCENDING
        elif d == last:
            groupLen += 1
        else:
            groups.add(groupLen)
            groupLen = 1
            last = d
    else:
        groups.add(groupLen)

    if part == 1:
        if 1 in groups:
            groups.remove(1)
        
        if len(groups) == 0:        
            return ERR_NO_GROUP

    elif 2 not in groups:
        return ERR_NO_GROUP
    
    return OK


def nextPassword(password, res):
    if res == ERR_DESCENDING:
        digits = [int(i) for i in str(password)]
        last = -1

        for i, d in enumerate(digits):
            if d < last:
               break
            else:
                last = d
        
        newPassword = [*digits[:i], *[last for _ in range(NUM_DIGITS-i)]]
        return int(''.join(map(str,newPassword)))
    else:
        return password + 1

     
def countValidPasswords(password, ubound, part):
    n = 0

    while password <= ubound:
        res = meetsCriteria(password, part)
        if res == OK:
            n += 1    
        password = nextPassword(password, res)

    return n
        

assert meetsCriteria(111111, 1) == OK
assert meetsCriteria(223450, 1) == ERR_DESCENDING
assert meetsCriteria(123789, 1) == ERR_NO_GROUP
print(f"Part one: {countValidPasswords(168630, 718098, 1)}")


assert meetsCriteria(112233, 2) == OK
assert meetsCriteria(123444, 2) == ERR_NO_GROUP
assert meetsCriteria(111122, 2) == OK
print(f"Part two: {countValidPasswords(168630, 718098, 2)}")