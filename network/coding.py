Error_table = {
    1: 14,
    2: 13,
    4: 12,
    8: 11,
    3: 10,
    6: 9,
    12: 8,
    11: 7,
    5: 6,
    10: 5,
    7: 4,
    14: 3,
    15: 2,
    13: 1,
    9: 0,
}


def xorVec(result, info, birth):
    k = 5

    buff = [0] * 5
    for i in range(0, 5):
        buff[i] = info[i]
    while k < 16:
        if buff[0] == 0 and k < 15:
            for j in range(0, 4):
                buff[j] = buff[j + 1]
            buff[4] = info[k]
            k = k + 1

            continue
        if buff[0] == 0:
            break
        for j in range(0, 5):
            buff[j] ^= birth[j]
    for i in range(4):
        result[i] = buff[i + 1]
    return result


def fact(x):
    result = 1
    for i in range(2, x+1, 1):
        result *= i
    return result


def combination(n, k):
    x = fact(n) / (fact(k) * fact(n - k))
    x = int(x)
    return x


def MoveOne(a):
    x=a-1
    m = (a ^ x)
    n = (m>>2)
    s=x^n
    return s


def AddOne(a):
    x=a-1
    m = (a^x)
    n = (m+1)>>2
    s=a|n
    return s


def GetNextError(a):
    if (a & (a + 1)) == 0:
        return 0
    if a & 1:
        return AddOne(GetNextError(a >> 1) << 1)
    else:
        return MoveOne(a)


def ErrorToArray(error, error_array):
    for i in range(14, -1, -1):
        error_array[14 - i] = (error >> i) & 1

def encoding(byte: None):
    byte = bin(byte)
    byte = byte.replace('0b','')
    inf_vector = list(map(lambda x: int(x), byte))
    while inf_vector.__len__() != 8:
        inf_vector.insert(0, 0)

    while inf_vector.__len__() < 11:
        inf_vector.append(0)
    moved_inf_vector = [None] * 15
    for i in range(0, 15, 1):
        if i < 11:
            moved_inf_vector[i] = inf_vector[i]
        else:
            moved_inf_vector[i] = 0
    birth_polynom = [1, 0, 0, 1, 1]
    remain_vector = [0] * 4
    xorVec(remain_vector, moved_inf_vector, birth_polynom)
    circle_code = [None] * 15
    for i in range(0, 15, 1):
        if i < 11:
            circle_code[i] = moved_inf_vector[i]
        else:
            circle_code[i] = remain_vector[i - 11]
    to_list = [str(i) for i in circle_code]
    to_string = "".join(to_list)
    to_bytes = to_string.encode() + b'\n'
    return to_bytes

def decoding(income_str: None):
    birth_polynom = [1, 0, 0, 1, 1]
    income_str = income_str.decode().replace('\n', '')
    income_vector = list(map(lambda x: int(x), income_str))
    check_error = [0, 0, 0, 0]
    xorVec(check_error, income_vector, birth_polynom)
    if not check_error[0] and not check_error[1] and not check_error[2] and not check_error[3]:
        for i in range(0, 7, 1):
            income_vector.pop()
        while income_vector[0] == 0:
            income_vector.pop(0)
        to_list = [str(i) for i in income_vector]
        to_string = "".join(to_list)
        to_int = int(to_string, 2)
        to_byte = to_int.to_bytes(1, 'big')
        return to_byte
