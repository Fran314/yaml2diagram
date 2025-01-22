from os import path
import sass

from material_icons import MaterialIcons

icon_manager = MaterialIcons()


def opening_tag(tag, id, classes, attributes):
    opening_tag_content = [ tag ]

    if id != '':
        opening_tag_content.append(f'id="{id}"')
    if len(classes) > 0:
        class_list = ' '.join(classes)
        opening_tag_content.append(f'class="{class_list}"')
    if len(attributes) > 0:
        for (key, val) in attributes:
            opening_tag_content.append(f'{key}="{val}"')


    return ' '.join(opening_tag_content)


def tag(tag, id, classes, attributes, content):
    o_tag = opening_tag(tag, id, classes, attributes)
    c_tag = f'/{tag}'

    return f'<{o_tag}>{content}<{c_tag}>'


def div(id='', classes=[], attributes=[], content=''):
    return tag('div', id, classes, attributes, content)


def pre(content):
    return tag('pre', '', [], [], content)


def span(content):
    return tag('span', '', [ 'material-icons' ], [], content)


def style(content):
    return tag('style', '', [], [], content)


def render_obj(obj):
    if isinstance(obj, list):
        output = ""
        for entry in obj:
            output += render_obj(entry)
        return output

    elif isinstance(obj, dict):
        if obj['type'] == 'empty':
            return div()
        elif obj['type'] == 'string':
            return pre(obj['content'])
        elif obj['type'] == 'container':
            return div(
                    obj['id'],
                    ['container'] + obj['classes'],
                    obj['attributes'],
                    render_obj(obj['content'])
                    )
        elif obj['type'] == 'icon':
            icon_names = obj['content'].split(' ')
            icons = [icon_manager.get(i) for i in icon_names]
            return div(
                    obj['id'],
                    ['icon'] + obj['classes'],
                    obj['attributes'],
                    ''.join(icons)
                    )
        else:
            raise Exception("Impossible object found, unknown type")

    else:
        raise Exception("Impossible object found (parsed diagram element must be either list or object)")


def render_diagram(diagram):
    return div(
            '',
            ['diagram'] + diagram['classes'],
            diagram['attributes'],
            render_obj(diagram['content'])
            )


with open(path.join(path.abspath(path.dirname(__file__)), 'index.html'), 'r') as file:
    INDEX = file.read()
with open(path.join(path.abspath(path.dirname(__file__)), 'style.scss'), 'r') as file:
    STYLE = sass.compile(string=file.read(), output_style='compressed')


def handle(name):
    return '<!-- {{' + name + '}} -->'


def render(diagram):
    return INDEX \
        .replace(handle('style'), style(STYLE)) \
        .replace(handle('diagram'), render_diagram(diagram))

