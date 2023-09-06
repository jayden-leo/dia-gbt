import re


def test_pattern_demo1():
    text = "sdfasdf grab the package sdf as"
    pattern = "(seiz|pick up|grab).*(part|package)"
    match = re.search(pattern, text, re.IGNORECASE)
    intents = []
    if match:
        print(match.group())
        for part in match.groups():
            intents.append(part)
        print(str(intents))


def test_pattern_demo2():
    """
        <demo>complete the whole cooking process</demo>
        <intent>(complete the whole cooking process)</intent>
        <pattern></pattern>
    """
    text = "grab the parts"
    pattern = '^(seiz|pick.*up|grab|grasp|obtain|get).*(component|part|element|piece)'
    if pattern is not None and len(pattern) != 0 and re.search(pattern, text, re.IGNORECASE):
        match = re.search(pattern, text, re.IGNORECASE)
        intents = []
        if match:
            print(match.group())
            for part in match.groups():
                intents.append(part)
            print(str(intents))


if __name__ == '__main__':
    # test_pattern_demo1()
    test_pattern_demo2()
