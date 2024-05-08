import random


def generateRule(a, b):
    """
    Generate a rule for a given range of length.

    Args:
        a (int): Minimum length of the rule.
        b (int): Maximum length of the rule.

    Returns:
        str: Generated rule.
    """
    vocab = ['F', '-', '+', '[', ']']
    prob = [0.2, 0.2, 0.2, 0.2, 0.2]
    cumulative = updateCumulative(prob)
    

    countopen = 0
    rule = ''
    termination = False
    while not termination:
        r = random.random()
        for i in range(1, len(cumulative)):
            if r >= cumulative[i-1] and r < cumulative[i]:
                index = i-1
                letter = vocab[index]
                break
        if letter in isValid(rule, countopen):
            rule += letter
            if letter == '[':
                countopen += 1
            elif letter == ']':
                countopen -= 1

        if len(rule) >= a:
            if countopen != 0:
                pass
            else:
                termination = True

        if len(rule) > b:
            rule = ''
            countopen = 0
        # print(rule)
    return rule

def isValid(rule, countopen):
    """
    Check if a rule is valid given the current state.

    Args:
        rule (str): The rule to check.
        countopen (int): Count of open brackets in the rule.

    Returns:
        list: List of valid characters.
    """
    if helper(rule) < 3:
        valid = ['F']
    else:
        valid = []
    if '[' in rule and countopen != 0 and rule[-1] != '[' and helper(rule) != 0:
        valid.append(']')
    if 'F' in rule:
        if rule[-1] in ['F', '[', ']']:
            valid += list("+-")
        if countopen == 0:
            valid.append('[')

    return valid

def validChromosome(chromosome):
    """
    Check if a chromosome is valid.

    Args:
        chromosome (str): The chromosome to check.

    Returns:
        bool: True if the chromosome is valid, False otherwise.
    """
    nOpen = 0
    nClose = 0
    stack = []
    if 'F' not in chromosome:
        return False
    if len(chromosome) < 1:
        return False
    for i in chromosome:
        if i == '[':
            nOpen += 1
        if i == ']':
            nClose += 1

        if i == '[':
            stack.append(i)
        elif i == ']':
            if len(stack) != 0:
                stack.pop(-1)
            else:
                return False

    return nOpen == nClose and len(stack) == 0


def helper(s):
    """
    Helper function to count the number of 'F's in a string.

    Args:
        s (str): The string to count 'F's.

    Returns:
        int: Number of 'F's in the string.
    """
    count = 0
    for i in range(len(s)-1, -1, -1):
        if s[i] == 'F':
            count += 1
        if s[i] == '[':
            return count
    return count

def updateCumulative(prob):
    """
    Update cumulative probabilities.

    Args:
        prob (list): List of probabilities.

    Returns:
        list: Cumulative probabilities.
    """
    count = 0
    cumulative = [0]
    for i in prob:
        count += i
        cumulative.append(count)
    return cumulative


def Substitution_init(d, order):
    """
    Initialize substitution.

    Args:
        d (dict): Dictionary of substitutions.
        order (int): Order of substitution.

    Returns:
        str: Initialized substitution string.
    """
    s = 'F'
    d = {'F': d}
    for _ in range(order):
        s = Substitution_helper(d, s)
    return s


def Substitution_helper(d, s):
    """
    Helper function for substitution.

    Args:
        d (dict): Dictionary of substitutions.
        s (str): String to substitute.

    Returns:
        str: Substituted string.
    """
    return ''.join([d.get(c) or c for c in s])
