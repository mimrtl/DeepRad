import os

def listOfStr2Str(str_list, seperator = ""):
    string = ""
    for item in str_list:
        string += seperator
        string += item
    return string


def isValidPath(path):
    return os.path.exists(path)

def isAllFalseMultiChoice(list):
    return sum(list) == 0

def isValidRelation(min, max):
    return min <= max

def isValidNumber(number, min = -float('inf'), max = float('inf')):
    return number >= min and number <= max

def isValidIntNumberString(string, min = -float('inf'), max = float('inf')):
    try:
        number = int(string)
        return isValidNumber(number = number, min = min, max = max)
    except ValueError:
        return False

def isValidFloatNumberString(string, min = -float('inf'), max = float('inf')):
    try:
        number = float(string)
        return isValidNumber(number = number, min = min, max = max)
    except ValueError:
        return False

def isEmptyString(string):
    return len(string) == 0

def str2int(string):
    return int(string)

def str2float(string):
    return float(string)