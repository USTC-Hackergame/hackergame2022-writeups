import re
import typing

from hashlib import sha384


def is_consonant(c: str) -> bool:
    return c.lower() not in 'aeiou'


def XZRJification_word(word: str) -> str:
    result = []
    for c in word:
        if len(result) > 0 and c.lower() == result[-1].lower() and is_consonant(c):
            continue
        result.append(c)
    if len(result) >= 2 and is_consonant(result[-2]) and result[-1].lower() == 'e':
        result.pop()
    return ''.join(result)

def XZRJification(s: str) -> str:
    result = []
    last_end = 0
    for word_match in re.finditer('[A-Za-z]+', s):
        result.append(s[last_end: word_match.span()[0]])
        result.append(XZRJification_word(word_match.group(0)))
        last_end = word_match.span()[1]
    result.append(s[last_end:])
    return ''.join(result)

# print(XZRJification('aabbcddde'))
# exit()

def num_possibilities_word(word: str, length_growth: int) -> int:
    num_consonants = sum(1 for c in word if is_consonant(c))
    num_possibilities_of_length_growth = [0] * (length_growth + 1)
    num_possibilities_of_length_growth[0] = 1
    # dynamic programming
    print(num_possibilities_of_length_growth)
    for _ in range(num_consonants):
        num_possibilities_of_length_growth = [
            sum(
                num_possibilities_of_length_growth[sum_length_growth - this_letter_growth]
                for this_letter_growth in range(sum_length_growth + 1)
            )
            for sum_length_growth in range(length_growth + 1)
        ]
        print(num_possibilities_of_length_growth)
    return (
        (num_possibilities_of_length_growth[length_growth] + num_possibilities_of_length_growth[length_growth - 1])
        if length_growth > 0 and len(word) > 0 and is_consonant(word[-1])
        else num_possibilities_of_length_growth[length_growth]
    )

# print(num_possibilities_word('a', 1))
# print(num_possibilities_word('x', 1))
# print(num_possibilities_word('x', 2))
# print(num_possibilities_word('xy', 1))
# print(num_possibilities_word('ustc', 16))
# 1600
# exit()

def num_possibilities(s: str, origin_length: int) -> int:
    length_difference = origin_length - len(s)
    words = re.findall('[A-Za-z]+', s)
    # dynamic programming
    num_possibilities_of_length_growth = [0] * (length_difference + 1)
    num_possibilities_of_length_growth[0] = 1
    for word in words:
        new_num_possibilities_of_length_growth = []
        this_word_possibilities = [num_possibilities_word(word, l) for l in range(length_difference + 1)]
        for sum_length_growth in range(length_difference + 1):
            new_num_possibilities_of_length_growth.append(sum(
                num_possibilities_of_length_growth[sum_length_growth - this_word_growth]
                * this_word_possibilities[this_word_growth]
                for this_word_growth in range(sum_length_growth + 1)
            ))
        num_possibilities_of_length_growth = new_num_possibilities_of_length_growth
    return new_num_possibilities_of_length_growth[length_difference]


def recover_word_recur(
    char_index: int,
    final_consonant_index: int,
    parts: typing.List[str],
    remaining_length_growth: int,
    origin_length: int,
) -> typing.Generator[str, None, None]:
    if char_index == final_consonant_index:
        parts[char_index] = parts[char_index][0] * (1 + remaining_length_growth)
        yield ''.join(parts)
        if char_index == origin_length - 1 and remaining_length_growth > 0:
            parts[char_index] = parts[char_index][0] * (1 + remaining_length_growth - 1) + 'e'
            yield ''.join(parts)
        # raise StopIteration
        return
    for this_char_growth in range((remaining_length_growth if is_consonant(parts[char_index][0]) else 0) + 1):
        parts[char_index] = parts[char_index][0] * (1 + this_char_growth)
        yield from recover_word_recur(
            char_index + 1,
            final_consonant_index,
            parts,
            remaining_length_growth - this_char_growth,
            origin_length
        )


def recover_word(word: str, length_growth: int) -> typing.Generator[str, None, None]:
    final_consonant_index = max(
        i for i in range(len(word))
        if is_consonant(word[i])
    )
    parts = list(word)
    yield from recover_word_recur(
        0,
        final_consonant_index,
        parts,
        length_growth,
        len(word),
    )

# print(list(recover_word('ustc', 0)))
# print(list(recover_word('ustc', 1)))
# print(list(recover_word('ustc', 1)))
# print(len(list(recover_word('ustc', 2))))
# print(len(list(recover_word('ustc', 39))))
# print(len(set(recover_word('ustc', 39))))
# exit()

def recover_string_recur(
    word_index: int,
    num_words: int,
    parts: typing.List[str],
    grown_words: typing.List[typing.List[str]],
    remaining_length_growth: int,
) -> typing.Generator[str, None, None]:
    if word_index == num_words - 1:
        for grown_word in grown_words[word_index][remaining_length_growth]:
            parts[word_index * 2 + 1] = grown_word
            yield ''.join(parts)
        # raise StopIteration
        return
    for this_word_growth in range(remaining_length_growth + 1):
        for grown_word in grown_words[word_index][this_word_growth]:
            parts[word_index * 2 + 1] = grown_word
            yield from recover_string_recur(
                word_index + 1,
                num_words,
                parts,
                grown_words,
                remaining_length_growth - this_word_growth,
            )


def recover_string(s: str, target_length: int) -> typing.Generator[str, None, None]:
    # XXX: Ignore cases that there is no consonant in the word to simplify
    # implementation.
    total_length_growth = target_length - len(s)
    words = re.findall('[A-Za-z]+', s)
    # [word_index][length] = [words_grown_by_length]
    grown_words = [
        (
            [list(recover_word(word, g)) for g in range(total_length_growth + 1)]
            if any(is_consonant(c) for c in word)
            else [word]
        )
        for word in words
    ]

    last_end = 0
    # words are at index 1, 3, 5... Empty strings are kept
    parts = []
    for word_match in re.finditer('[A-Za-z]+', s):
        parts.append(s[last_end: word_match.span()[0]])
        parts.append(word_match.group(0))
        last_end = word_match.span()[1]
    parts.append(s[last_end:])
    # print(parts)
    # ['', 'ustc', '.', 'edu', '.', 'cn', '']

    yield from recover_string_recur(0, len(words), parts, grown_words, total_length_growth)

# print(list(recover_string('ustc.edu.cn', 11)))
# print(len(list(recover_string('ustc.edu.cn', 39))))


def brute_force(s: str, origin_length: int) -> int:
    first_half = 'ec18f9dbc4aba825c7d4f9c726db1cb0d0babf47f'
    second_half = 'a170f33d53bc62074271866a4e4d1325dc27f644fdad'
    first_possible_xzrj = first_half + second_half
    second_possible_xzrj = first_half + 'e' + second_half
    counter = 0
    for secret in recover_string(s, origin_length):
        # if counter % 1000 == 0:
        #     print(counter)
        counter += 1
        # if XZRJification(sha384(secret.encode()).hexdigest()) == secret_sha384:
        digest = sha384(secret.encode()).hexdigest()
        xzrjed = XZRJification(digest)
        # print(f'{digest=}\n{xzrjed=}')
        # if xzrjed.startswith(first_half):
        if xzrjed == first_possible_xzrj or xzrjed == second_possible_xzrj:
            print(secret)
            print(xzrjed)


def main() -> None:
    xzrjed_secret = b'ustc.edu.cn'
    # print(num_possibilities('a.a', 3))
    # print(num_possibilities('a.a', 4))
    # print(num_possibilities('a.x', 4))
    # print(num_possibilities('x.x', 4))
    # print(num_possibilities(xzrjed_secret.decode(), 39))
    # 809999
    # Looks brute-force-able if my calculation is right
    brute_force(xzrjed_secret.decode(), 39)


if __name__ == "__main__":
    main()
