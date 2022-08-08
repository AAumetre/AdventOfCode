from functions import *
import re

def verify_part1(passport: str) -> bool:
    for token in ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]:
        if token not in passport:
            return False
    return True

def verify_passport(passport: str) -> int:
    tokens = {
        "byr": [re.compile(r"\d{4}"), (1920, 2002)],
        "iyr": [re.compile(r"\d{4}"), (2010, 2020)],
        "eyr": [re.compile(r"\d{4}"), (2020, 2030)],
        "hgt": [re.compile(r"(\d+)(cm|in)"), {"cm": (150, 193), "in": (59, 76)}],
        "hcl": [re.compile(r"#[0-9a-f]{6}")],
        "ecl": [re.compile(r"(amb|blu|brn|gry|grn|hzl|oth)")],
        "pid": [re.compile(r"\d{9}")],
        "cid": [re.compile(r".*")]
    }
    if not verify_part1(passport):
        return 0
    for element in passport.split(" "):
        if element == "": continue
        code = element.split(":")[0]
        value = element.split(":")[1]
        if not tokens[code][0].fullmatch(value):
            logging.debug(f"\t{element} invalid because regex does not match {value}")
            return 0
        if code in ["byr", "iyr", "eyr"]:
            if int(value) not in range(tokens[code][1][0], tokens[code][1][1]+1):
                logging.debug(f"\t{element} invalid because {value} not in [{tokens[code][1][0]}, {tokens[code][1][1]}]")
                return 0
        elif code == "hgt" and value[-2:] == "cm":
            if int(value[:-2]) not in range(tokens["hgt"][1]["cm"][0], tokens["hgt"][1]["cm"][1]+1):
                logging.debug(f"\t{element} invalid because {value} not in range")
                return 0
        elif code == "hgt" and value[-2:] == "in":
            if int(value[:-2]) not in range(tokens["hgt"][1]["in"][0], tokens["hgt"][1]["in"][1]+1):
                logging.debug(f"\t{element} invalid because {value} not in range")
                return 0
    return 1


def main():
    logging.basicConfig(level=logging.INFO)
    data = read_file("data/04.in")
    data.append("")
    valid_passports = 0
    passport = ""
    for line in data:
        if line == "":
            valid_passports += verify_part1(passport)
            passport = ""
        else:
            passport += (" " + line)
    logging.info(valid_passports)

    valid_passports = 0
    passport = ""
    for line in data:
        if line == "":
            valid_passports += verify_passport(passport)
            passport = ""
        else:
            passport += (" " + line)
    logging.info(valid_passports)

main()