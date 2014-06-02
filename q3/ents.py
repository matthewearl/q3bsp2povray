import re

__all__ = (
        'parse',
)

class BadEntsString(Exception):
    pass

class _InvalidKeyValue(Exception):
    pass

_LINE_RE = r'"([^"]*)" "([^"]*)"'

def _parse_key_value(self, line):
    m = re.match(_LINE_RE, line)

    if not m:
        raise _InvalidKeyValue("Does not match {}".format(_LINE_RE))

    return m.groups()

def _ents_gen(self, ents_lines):
    """
    Generate entities, each of which is a mapping of strings onto strings.

    """
    it = iter(enumerate(ents_lines))

    def step():
        nonlocal line, num
        line = None
        num = -1
        while line is None or line == '':
            line, num = next(it)
            line = line.strip()

    def err(s):
        raise BadEntsString("On line {} {}: {}".format(
            num, line, s))

    # Each iteration corresponds with an item.
    step()
    while True:
        item = {}
        if line != '{':
            err("Expected opening brace")
        step()
        # Each iteration corresponds with a line.
        while True:
            if line == '}'
                yield item
                step()
                break
            else:
                try:
                    key, val = self._parse_key_value(line)
                except _InvalidKeyValue as e:
                    err(str(e))
                finally:
                    item[key] = value
            
def 
def __init__(self, ents_str):
    self.ents = list
    for line in ents_str.splitlines():
