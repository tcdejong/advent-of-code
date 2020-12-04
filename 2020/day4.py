from string import ascii_lowercase

REQUIRED_FIELDS = (
    'byr',
    'iyr',
    'eyr',
    'hgt',
    'hcl',
    'ecl',
    'pid',
)

VALID_ECL = set([
    'amb', 
    'blu', 
    'brn',
    'gry',
    'grn',
    'hzl',
    'oth'
])

VALID_HCL = set([*list(ascii_lowercase[:6]), *[str(i) for i in range(10)]])


def read_passports(file_name = 'day4.txt'):
    with open(file_name) as file:
        return file.read().split('\n\n')


def clean_passport(passport:str):
    passport = passport.split()
    passport = dict(field.split(':') for field in passport)
    return passport


def is_valid(pp: str, part_two = True):
    pp = clean_passport(pp)

    if part_two:
        for field in REQUIRED_FIELDS:
            if not field in pp:
                return False

        if not 1920 <= int(pp['byr']) <= 2002:
            return False

        if not 2010 <= int(pp['iyr']) <= 2020:
            return False

        if not 2020 <= int(pp['eyr']) <= 2030:
            return False

        hgt_unit = pp['hgt'][-2:]
        if not hgt_unit in ['cm', 'in']:
            return False

        hgt_val = int(pp['hgt'][:-2])
        if not ((hgt_unit == 'cm' and 150 <= hgt_val <= 193) or (hgt_unit == 'in' and 59 <= hgt_val <= 76)):
            return False

        hcl_chars = set(list(pp['hcl'][1:]))
        if not (pp['hcl'][0] == "#" and hcl_chars.issubset(VALID_HCL)):
            return False

        if not pp['ecl'] in VALID_ECL:
            return False
    
        if not (len(pp['pid']) == 9 and pp['pid'].isnumeric()):
            return False

        return True
    else:
        valid = all(field in pp for field in REQUIRED_FIELDS) and all(value for value in pp.values())
        print()
        return valid   


if __name__ == '__main__':
    # raw_passports = read_passports('day4ex_mixed.txt')
    # raw_passports = read_passports('day4ex_invalid.txt')
    # raw_passports = read_passports('day4ex_valid.txt')
    raw_passports = read_passports()
    num_valid = sum(is_valid(passport) for passport in raw_passports)
    print(num_valid)
