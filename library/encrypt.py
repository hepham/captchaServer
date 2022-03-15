import random
import string


def random_string(letter_count, digit_count):
    str1 = ''.join((random.choice(string.ascii_letters) for x in range(letter_count)))
    str1 += ''.join((random.choice(string.digits) for x in range(digit_count)))

    sam_list = list(str1)
    random.shuffle(sam_list)
    final_string = ''.join(sam_list)
    return final_string


def encrypt(t):
    chars = list(t)
    allowed_characters = list(" dfikmnVopq7rsjtGuvwMxhHyazA-eBCEcFDIJQ*KlN5OPb:2RSgTUWXYZ013468L9,.?!@$%&")
    temp = ''
    for char in chars:
        for i in allowed_characters:
            if char == i:
                chars[chars.index(char)] = allowed_characters.index(i)
                temp = temp + str(allowed_characters.index(i))
    return temp
