import json
import random
import string


class Block(object):
    def __init__(self, typ, depth=0):
        self.type = typ
        self.depth = depth
        self.text = ""
        self.key = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5))
        self.inline_style_ranges = []

    def as_dict(self):
        return {
            'key': self.key,
            'type': self.type,
            'depth': self.depth,
            'text': self.text,
            'inlineStyleRanges': [isr.as_dict() for isr in self.inline_style_ranges]
        }


class InlineStyleRange(object):
    def __init__(self, style):
        self.style = style
        self.offset = None
        self.length = None

    def as_dict(self):
        return {
            'offset': self.offset,
            'length': self.length,
            'style': self.style
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
