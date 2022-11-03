import re
import hashlib
import itertools
import functools

from typing import Sequence, Iterator

from tqdm import tqdm


AEIOU = frozenset("AEIOUaeiou")


def XZRJify_word(word):
    if len(word) > 1 and word[-1] in "Ee" and word[-2] not in AEIOU:
        word = word[:-1]

    result = []
    for c, c_next in itertools.pairwise(list(word) + [""]):
        if c not in AEIOU and c == c_next:
            continue
        result.append(c)

    return "".join(result)


def XZRJify(string):
    pos = 0
    result = []
    for match in re.finditer(r"[A-Za-z]{2,}", string):
        result.append(string[pos:match.start()])
        result.append(XZRJify_word(match.group()))
        pos = match.end()
    result.append(string[pos:])

    return "".join(result)


@functools.cache
def has_consonant(word: str) -> bool:
    return any(c not in AEIOU for c in word)


@functools.cache
def unXZRJify_word(word: str, length: int) -> Sequence[str]:
    assert 0 < len(word) <= length, f"{word=}, {length=}"

    if len(word) == length:
        return [word]

    assert has_consonant(word)

    c = word[0]
    if len(word) == 1:
        assert c not in AEIOU
        return [c * length, c*(length-1) + "e"]

    rest = word[1:]
    if c in AEIOU:
        return [c + x for x in unXZRJify_word(rest, length-1)]

    if not has_consonant(rest):
        return [c * (length-len(rest)) + rest]

    # 至此，c 是辅音且 rest 里一定有辅音，这意味着 rest 可以任意长
    return [c * (length-rest_len) + expanded_rest
            for rest_len in range(len(rest), length)
            for expanded_rest in unXZRJify_word(rest, rest_len)]


def unXZRJify_ustc_edu_cn() -> Iterator[str]:
    length = 39 - 2

    for ustc_len in range(4, length - len("edu") - len("cn") + 1):
        for edu_len in range(3, length - ustc_len - len("cn") + 1):
            cn_len = length - ustc_len - edu_len
            for ustc, edu, cn in itertools.product(
                unXZRJify_word("ustc", ustc_len),
                unXZRJify_word("edu", edu_len),
                unXZRJify_word("cn", cn_len),
            ):
                value = f"{ustc}.{edu}.{cn}"
                assert len(value) == 39, (ustc_len, edu_len, cn_len, value)
                yield value


def main() -> None:
    for ustc_edu_cn in tqdm(list(unXZRJify_ustc_edu_cn())):
        digest = hashlib.sha384(ustc_edu_cn.encode("ascii")).hexdigest()
        assert len(digest) == 96
        for i in range(42, 53):
            if (
                XZRJify(digest[:i])     == "ec18f9dbc4aba825c7d4f9c726db1cb0d0babf47f"
                and XZRJify(digest[i:]) == "a170f33d53bc62074271866a4e4d1325dc27f644fdad"
            ):
                print()
                print(ustc_edu_cn)
                print("digest:", digest)
                print("i:", i)
                return


if __name__ == "__main__":
    main()
