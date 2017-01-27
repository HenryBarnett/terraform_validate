import re

def matches_regex_pattern(variable, regex):
    return not (get_regex_matches(regex, variable) is None)


def get_regex_matches(regex, variable):
    if regex[-1:] != "$":
        regex += "$"

    if regex[0] != "^":
        regex = "^" + regex

    variable = str(variable)
    if '\n' in variable:
        return re.match(regex, variable, re.DOTALL)
    return re.match(regex, variable)