import re


def main():
    with open("getflag.hei.py", encoding="utf-8") as f:
        heilang = f.readlines()

    py = []
    for line in heilang:
        match = re.search(
            r"^a\[(\s*\d+\s*(\|\s*\d+\s*)*)\]\s*=\s*(\d+)",
            line,
            re.ASCII,
        )
        if match is None:
            py.append(line)
            continue

        indexes = match.group(1)
        value = match.group(3)
        new_line = []
        for index in indexes.split("|"):
            new_line.append(f"a[{index.strip()}] = ")
        new_line.append(f"{value}\n")

        py.append("".join(new_line))

    with open("getflag.py", "w", encoding="utf-8") as f:
        f.writelines(py)


if __name__ == "__main__":
    main()
