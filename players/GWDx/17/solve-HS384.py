from hashlib import sha384
# longest common substring
import pylcs


def check_equals(left, right):
    # check whether left == right or not
    if left != right:
        print(left)
        print(right)


secret = b'ustc.edu.cn'

allConsonant = 'bcdfghjklmnpqrstvwxyz'


# split N into M parts, each part is at least 1
# return all possible ways
# for example, split(4, 2) returns [[1, 3], [2, 2], [3, 1]]
def split(N, M):
    if M == 1:
        return [[N]]
    else:
        return [[i] + j for i in range(1, N) for j in split(N - i, M - 1)]


# given a string and length, return all possible ways to repeat consonant letters
# for example, repeat('abc', 4) returns ['abbc', 'abcc']
# repeat('abc', 5) returns ['abccc', 'abbcc', 'abbbc']
def repeat(string, length):
    consonantChar = [i for i in string if i in allConsonant]
    vowelChar = [i for i in string if i not in consonantChar]
    consonantCount = len(consonantChar)
    vowelCount = len(vowelChar)
    consonantTarget = length - vowelCount

    allPossible = split(consonantTarget, consonantCount)
    # print(allPossible)
    result = []
    for allRepeatTime in allPossible:
        temp = ''
        consonantCharIndex = 0
        for char in string:
            if char in consonantChar:
                temp += char * allRepeatTime[consonantCharIndex]
                consonantCharIndex += 1
            else:
                temp += char
        result.append(temp)

    # print(result)
    return result


# repeat('abec', 6)
allPossibleSecret = repeat('ustce.edu.cn', 39)

for possibleSecret in allPossibleSecret:
    possibleSecret = possibleSecret.encode()
    check_equals(len(possibleSecret), 39)
    # check secret hash
    secret_sha384 = 'ec18f9dbc4aba825c7d4f9c726db1cb0d0babf47fa170f33d53bc62074271866a4e4d1325dc27f644fdad'

    # check_equals(sha384(secret).hexdigest(), secret_sha384)

    fullSHA = sha384(possibleSecret).hexdigest()

    # if lcs > 32, print it
    if pylcs.lcs(fullSHA, secret_sha384) > 48:
        print(fullSHA)
        print(secret_sha384)
        print(possibleSecret)
