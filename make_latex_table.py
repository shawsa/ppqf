from itertools import zip_longest


with open("weight_table.html", "r") as f:
    lines = f.readlines()

remove_list = ["\t", "<td>", "</td>", "<tr>", "</tr>", "\n"]


def remove_all(string: str, substrings: list[str]) -> str:
    my_str = string
    for substr in substrings:
        my_str = my_str.replace(substr, "")
    return my_str


lines = [remove_all(line, remove_list) for line in lines]
lines = [line for line in lines if line != ""]

rules = []
rule = [lines[0]]
for line in lines[1:]:
    if "mathcal" in line:
        rules.append(rule)
        rule = []
    rule.append(line)
rules.append(rule)


def transpose(rules):
    def none_filter(string):
        if string is None:
            return ""
        return string

    rows = [[none_filter(val) for val in col] for col in zip_longest(*rules)]
    return rows


def make_table(rows):
    return "\\\\ \\hline \n".join(" & ".join(val for val in row) for row in rows)


print(make_table(transpose(rules[:9])))
print(make_table(transpose(rules[9:])))
