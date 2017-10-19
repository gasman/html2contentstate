import io
import xml.sax

from contentstate import Block, ContentState, InlineStyleRange


LIST_ELEMENTS = {
    'ol': 'ordered-list-item',
    'ul': 'unordered-list-item'
}
BLOCK_ELEMENTS = {
    'h1': 'header-one',
    'h2': 'header-two',
    'h3': 'header-three',
    'h4': 'header-four',
    'h5': 'header-five',
    'h6': 'header-six',
    'p': 'unstyled',
    'img': 'atomic',
    'li': None
}
INLINE_STYLE_ELEMENTS = {
    'i': 'ITALIC',
    'em': 'ITALIC',
    'b': 'BOLD',
    'strong': 'BOLD',
}


class HtmlToContentStateHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.contentstate = ContentState()
        self.current_block = None

        self.previous_states = []
        self.state = {
            'depth': 0,
            'list-item-type': None
        }
        self.current_inline_styles = []

        super(HtmlToContentStateHandler, self).__init__()

    def push_state(self, new_state):
        self.previous_states.append(self.state)
        self.state = new_state

    def pop_state(self):
        self.state = self.previous_states.pop()

    def add_block(self, block):
        self.contentstate.blocks.append(block)
        self.current_block = block

    def startElement(self, name, attrs):
        if name in LIST_ELEMENTS:
            # A <ul> or <ol> element does not create any new blocks itself;
            # it merely updates the state so that any <li> elements we subsequently
            # encounter will have the appropriate list element type and depth assigned
            # on the resulting block
            if self.state['list-item-type'] is None:
                # this is not nested in another list => depth remains unchanged
                new_depth = self.state['depth']
            else:
                # start the next nesting level
                new_depth = self.state['depth'] + 1

            self.push_state({
                'depth': new_depth,
                'list-item-type': LIST_ELEMENTS[name]
            })

        elif name in BLOCK_ELEMENTS:
            # start a new block

            if name == 'li':
                assert self.state['list-item-type'] is not None, "<li> found outside of an enclosing list element"
                self.add_block(Block(
                    self.state['list-item-type'],
                    depth=self.state['depth']
                ))

            else:
                assert self.state['depth'] == 0, "%s tag found nested inside a list" % name
                self.add_block(Block(
                    BLOCK_ELEMENTS[name],
                    depth=self.state['depth']
                ))

        elif name in INLINE_STYLE_ELEMENTS:
            assert self.current_block is not None, "%s tag found at the top level" % name
            inline_style_range = InlineStyleRange(INLINE_STYLE_ELEMENTS[name])
            inline_style_range.offset = len(self.current_block.text)
            self.current_block.inline_style_ranges.append(inline_style_range)
            self.current_inline_styles.append(inline_style_range)

        else:
            print("[%s]" % name)

    def endElement(self, name):
        if name in LIST_ELEMENTS:
            assert LIST_ELEMENTS[name] == self.state['list-item-type']
            self.pop_state()

        elif name in BLOCK_ELEMENTS:
            assert not self.current_inline_styles, "End of block reached without closing inline style elements"
            self.current_block = None

        elif name in INLINE_STYLE_ELEMENTS:
            inline_style_range = self.current_inline_styles.pop()
            assert inline_style_range.style == INLINE_STYLE_ELEMENTS[name]
            inline_style_range.length = len(self.current_block.text) - inline_style_range.offset

        else:
            print("[/%s]" % name)

    def characters(self, content):
        if self.current_block is None:
            assert not content.strip(), "Bare text content found at the top level: %r" % content

        else:
            self.current_block.text += content


def convert(html):
    parser = xml.sax.make_parser()
    handler = HtmlToContentStateHandler()
    parser.setContentHandler(handler)

    # need to wrap input (which may contain multiple top-level elements) in a single
    # container element so that sax will accept it as a valid XML document
    parser.parse(io.StringIO("<rich-text-document>%s</rich-text-document>" % html))

    return handler.contentstate.as_json()
