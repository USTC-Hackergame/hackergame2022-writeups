def main() -> None:
    with open('getflag.hei.py', 'r') as f, open('out.py', 'w') as out:
        for line in f:
            if line.startswith('a['):
                indices = line.partition('[')[2].partition(']')[0].split(' | ')
                rhs = line.rpartition(' ')[2]
                for index in indices:
                    out.write(f'a[{index}] = {rhs}')
            else:
                out.write(line)


if __name__ == "__main__":
    main()
