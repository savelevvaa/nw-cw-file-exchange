import math

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


def main():
    print('Введите информационный вектор')
    InfVect = list(map(lambda x: int(x), input()))
    print(InfVect)
    Moved_InfVect = [None] * 15
    for i in range(0, 15, 1):
        if i < 11:
            Moved_InfVect[i] = InfVect[i]
        else:
            Moved_InfVect[i] = 0
    Birth_Poly = [1, 0, 0, 1, 1]
    Remain_vect = [0] * 4
    xorVec(Remain_vect, Moved_InfVect, Birth_Poly)
    Circle_code = [None] * 15
    for i in range(0, 15, 1):
        if i < 11:
            Circle_code[i] = Moved_InfVect[i]
        else:
            Circle_code[i] = Remain_vect[i - 11]
    print("===========================================================")
    print("___________________________________________________________")
    print("||   i || Сочетания ||   N0   ||    Nk     ||    Ck      ||")
    print("===========================================================")
    for index in range(1, 16, 1):
        No = 0
        Nk = 0
        Corrupted_vec = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        Error_array = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        Error = ((1 << index) - 1) << (15 - index)
        Cnk = combination(15, index)
        for i in range(0, Cnk, 1):
            ErrorToArray(Error, Error_array)
            for j in range(0, 15, 1):
                Corrupted_vec[j] = Circle_code[j] ^ Error_array[j]
            Check_error = [0, 0, 0, 0]
            xorVec(Check_error, Corrupted_vec, Birth_Poly)
            if not Check_error[0] and not Check_error[1] and not Check_error[2] and not Check_error[3]:
                Error = GetNextError(Error)
                continue
            No = No + 1
            Check_position = (8 * Check_error[0] + 4 * Check_error[1] + 2*Check_error[2]+Check_error[3])
            Error_pos = Error_table[Check_position]
            Corrupted_vec[Error_pos] = not Corrupted_vec[Error_pos]
            for j in range(0, 15, 1):
                if Corrupted_vec[j] != Circle_code[j]:
                    break
                if j == 14:
                    Nk = Nk + 1

            Error = GetNextError(Error)

        #print(index, "          ", Cnk, "         ", No, "          ", Nk, "               ", Nk/Cnk)
        print("||  %s%d ||    %s%d %s  ||   %s%d%s ||     %d %s   ||      %d%s   ||" % (
        "" if index > 9 else " ",index, "" if Cnk>1000 else " ", Cnk, "" if Cnk>99 else " ", "" if No>1000 else " ",No, " " if No < 100 else "", Nk, " " if Nk < 10 else "", Nk / Cnk * 100, "" if Nk / Cnk * 100 > 99 else "  "))
    print("============================================================")


if __name__ == "__main__":
    main()
