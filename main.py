from html.parser import HTMLParser


class Tag:
    def __init__(self, name: str):
        self.name = name
        self.is_closed = False
        self.parent: Tag | None = None

        self.children: list['Tag'] = []

    def move_to_first_closed_parent(self):
        current_parent = self.parent
        while current_parent:
            if current_parent.is_closed:
                self.parent = current_parent
                break
            current_parent = current_parent.parent

    def close(self) -> None:
        self.is_closed = True

    @property
    def index(self) -> int:
        if not self.parent or not self.parent.children:
            return 0
        index = 0
        for child in self.parent.children:
            if child is self:
                return index
            if child.name == self.name:
                index += 1
        return index

    def __repr__(self):
        # Не виводимо індекс, якщо тег не має parent або це тег html, head, body (які зустрічаються лише один раз)
        # Щоб вивід відповідав прикладу
        if self.name in ('html', 'head', 'body') or not self.parent:
            return f'{self.name}'
        else:
            return f'{self.parent}.{self.name}[{self.index}]'


class UnclosedTagFinder(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags: list[Tag] = []
        self.last_open_tag: Tag | None = None

    def handle_starttag(self, tag, attrs):
        new_tag = Tag(tag)
        self.tags.append(new_tag)
        new_tag.parent = self.last_open_tag
        self.last_open_tag = new_tag

    def handle_endtag(self, tag):
        for tag_in_list in reversed([tag for tag in self.tags if not tag.is_closed]):
            if tag_in_list.name == tag:
                tag_in_list.close()
                self.last_open_tag = tag_in_list.parent
                return

    def format_dom_tree(self):
        for tag in reversed(self.tags):
            if tag.parent and not tag.parent.is_closed:
                tag.move_to_first_closed_parent()

    def initialize_children(self):
        for tag in self.tags:
            if tag.parent:
                tag.parent.children.append(tag)

    def get_unclosed_tags(self) -> list[Tag]:
        self.format_dom_tree()
        self.initialize_children()

        unclosed_tags = [tag for tag in self.tags if not tag.is_closed]
        return unclosed_tags


html_content = """
<body>
<div>Some text
<div>Some text2
<div><div>Lorem</div></div>
</body>
"""

parser = UnclosedTagFinder()
parser.feed(html_content)
print(parser.get_unclosed_tags())
