from functions import *

@dataclass()
class Interval:
    low: int
    high: int

    def is_in(self, val_: int) -> bool:
        return val_ >= self.low and val_ <= self.high


class Rule:
    name: str
    interval1: Interval
    interval2: Interval
    registry: Dict[int, bool]

    def __init__(self, name: str, int1: Interval, int2: Interval):
        self.name = name
        self.interval1 = int1
        self.interval2 = int2
        self.registry = {}

    def __hash__(self):
        return hash(self.name)

    def complies(self, val_: int) -> bool:
        """ Memoized checking. """
        if val_ in self.registry:
            return self.registry[val_]
        status = self.interval1.is_in(val_) or self.interval2.is_in(val_)
        self.registry[val_] = status
        return status


class Ticket:
    fields: List[int]

    def __init__(self, ticket_str: str):
        self.fields = [int(e) for e in ticket_str.split(",")]


@dataclass()
class TicketChecker:
    rules: List[Rule]

    def __init__(self, rules_: List[Rule]):
        self.rules = rules_

    def complies(self, val_: int) -> bool:
        for rule in self.rules:
            if rule.complies(val_):
                return True


def main():
    start_time = time.time_ns()
    logging.basicConfig(level=logging.INFO)
    data = read_file("data/16.in")
    line_index = 0
    # read rules
    rules = []
    line = data[line_index]
    while line != "":
        name = line.split(": ")[0]
        conds = line.split(": ")[1].split(" or ")
        int1 = Interval(int(conds[0].split("-")[0]), int(conds[0].split("-")[1]))
        int2 = Interval(int(conds[1].split("-")[0]), int(conds[1].split("-")[1]))
        rules.append(Rule(name, int1, int2))
        logging.debug(f"{rules[-1]}")
        line_index += 1
        line = data[line_index]
    # read my ticket
    line_index += 2
    my_ticket = Ticket(data[line_index])
    # read other tickets
    checker = TicketChecker(rules)
    sum_invalids = 0
    tickets = []
    for line in data[line_index+3:]:
        ticket = Ticket(line)
        tickets.append(ticket)
        for val in ticket.fields:
            if not checker.complies(val):
                logging.debug(f"{val} does not comply")
                sum_invalids += val
                tickets = tickets[:-1]
                break
    logging.info(f"Part 1, invalid fields sum is {sum_invalids}.")

    rule_to_field: Dict[str, int] = {}
    open_indexes: List[int] = [i for i in range(len(my_ticket.fields))]
    open_rules: List[Rule] = rules.copy()
    fields: List[Tuple[int, List[int]]] = []
    # transpose tickets' information
    for i in range(len(my_ticket.fields)):
        values: List[int] = []
        for ticket in tickets:
            values.append(ticket.fields[i])
        fields.append((i, values))
    # find the correspondence between rules and fields
    checks_all_elements = lambda rule, fields: all([rule.complies(val) for val in fields[1]])
    try_rules = lambda rules, fields: [checks_all_elements(rule, fields) for rule in rules]
    while len(open_indexes) > 0:
        for index in open_indexes:
            verifies_all_fields = try_rules(open_rules, fields[index])
            if sum(verifies_all_fields) == 1:
                rule_index = 0
                for i in range(len(verifies_all_fields)):
                    if verifies_all_fields[i] == 1:
                        rule_index = i
                        break
                # assign rule to field index
                rule_to_field[open_rules[rule_index].name] = index
                # clean-up
                open_indexes.remove(index)
                open_rules.remove(open_rules[rule_index])
    # compute the product
    departure_product = 1
    for rule_str, index in rule_to_field.items():
        if "departure" in rule_str:
            departure_product *= my_ticket.fields[index]
    logging.info(f"Part 2, the product of the departure fields is {departure_product}.")

    logging.info(f"Duration: {(time.time_ns()-start_time) / 10 ** 9} s")

main()