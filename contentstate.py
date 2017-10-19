import json
import random
import string


class Block(object):
    def __init__(self, typ, depth=0):
        self.type = typ
        self.depth = depth
        self.text = ""
        self.key = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5))

    def as_dict(self):
        return {
            'key': self.key,
            'type': self.type,
            'depth': self.depth,
            'text': self.text
        }


class ContentState(object):
    """Pythonic representation of a draft.js contentState structure"""
    def __init__(self):
        self.blocks = []

    def as_dict(self):
        return {
            'blocks': [block.as_dict() for block in self.blocks],
            'entityMap': {},
        }

    def as_json(self):
        return json.dumps(self.as_dict())
