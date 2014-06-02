import re

"""
Parse entity strings.

"""

__all__ = (
        'parse',
)

class BadEntsString(Exception):
    pass

class _InvalidKeyValue(Exception):
    pass

_LINE_RE = r'"([^"]*)" "([^"]*)"'

def _parse_key_value(line):
    m = re.match(_LINE_RE, line)

    if not m:
        raise _InvalidKeyValue("Does not match {}".format(_LINE_RE))

    return m.groups()

def _ents_gen(ents_lines):
    """
    Generate entities, each of which is a mapping of strings onto strings.

    """
    it = iter(enumerate(ents_lines))

    line = None
    num = -1

    def step():
        nonlocal line, num
        num, line = next(it)
        while line is None or line == '' or line == '\x00':
            num, line = next(it)
            num += 1
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
            if line == '}':
                yield item
                step()
                break
            else:
                try:
                    key, value = _parse_key_value(line)
                    item[key] = value
                    step()
                except _InvalidKeyValue as e:
                    err(str(e))

def _fix_types_for_ent(ent):
    """
    Convert values of the given entity from strings to more appropriate types.

    For example, make `origin` a tuple of floats.

    """
    def vec(s):
        return tuple(float(x) for x in s.split(' '))

    key_types = {
        'origin': vec,
        'angle': float,
        'radius': float,
        'light': float,
        'spawnflags': int,
        '_color': vec
    }

    return { key: key_types.get(key, lambda x: x)(value) 
                for key, value in ent.items() }

def parse(ents_str):
    """
    Parse an ents string into an iterable of dicts.

    """
    ents_lines = ents_str.splitlines()
    return [_fix_types_for_ent(ent) for ent in _ents_gen(ents_lines)]

