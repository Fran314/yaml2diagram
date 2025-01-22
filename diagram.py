import sys
import yaml

# Supported diagram classes
DIAGRAM_CLASSES = [ 'row' ] + [ f'col-{i}' for i in range(1, 8+1) ]
# Supported diagram attributes
DIAGRAM_ATTRIBUTES = []

COLORS = [ 'red', 'orange', 'yellow', 'green', 'light-blue', 'blue', 'purple' ]
# Supported container classes
CONTAINER_CLASSES = [ 
                     # Container types
                     'box', 'folder', 'pad',

                     # Modifiers
                     'row', 'dashed', 'skew',
                     'abs', 'top', 'bottom', 'right', 'left',
                     ]
CONTAINER_CLASSES += COLORS 
CONTAINER_CLASSES += [ 't-' + c for c in COLORS  ]
CONTAINER_CLASSES += [ 'b-' + c for c in COLORS  ]
# SPECIAL_CLASSES = [ 'icon' ]
# Supported container attributes
CONTAINER_ATTRIBUTES = [ 'label' ]

def parse_key(key):
    head, *tail = key.split('&')
    id, *classes = head.split('.')
    classes = [ c for c in classes if c != "" ]

    def split_attribute(attribute):
        attr_key, attr_val = attribute.split('=', maxsplit=1)
        return (attr_key, attr_val)
    attributes = [split_attribute(a) for a in tail]

    return id, classes, attributes

def parse_dict(key, value):
    id, classes, attributes = parse_key(key)

    if 'icon' in classes:
        if not isinstance(value, str):
            raise Exception(f'Invalid icon at {key}: content is not of type string but of type {type(value)}')

        classes = [ c for c in classes if c != "icon" ]

        invalid_classes = [ c not in CONTAINER_CLASSES for c in classes ]
        if any(invalid_classes):
            issue = invalid_classes.index(True)
            raise Exception(f'Invalid class ("{classes[issue]}") in container element ("{key}")')

        invalid_attributes = [ a[0] not in CONTAINER_ATTRIBUTES for a in attributes ]
        if any(invalid_attributes):
            issue = invalid_attributes.index(True)
            raise Exception(f'Invalid attribute ("{attributes[issue][0]}={attributes[issue][1]}") in container element ("{key}")')

        return {
                'type': 'icon',
                'id': id,
                'classes': classes,
                'attributes': attributes,
                'content': value
                }

    invalid_classes = [ c not in CONTAINER_CLASSES for c in classes ]
    if any(invalid_classes):
        issue = invalid_classes.index(True)
        raise Exception(f'Invalid class ("{classes[issue]}") in container element ("{key}")')

    invalid_attributes = [ a[0] not in CONTAINER_ATTRIBUTES for a in attributes ]
    if any(invalid_attributes):
        issue = invalid_attributes.index(True)
        raise Exception(f'Invalid attribute ("{attributes[issue][0]}={attributes[issue][1]}") in container element ("{key}")')

    return {
            'type': 'container',
            'id': id,
            'classes': classes,
            'attributes': attributes,
            'content': parse_obj(value)
            }

def parse_obj(obj):
    if obj is None:
        return {
                'type': 'empty'
                }

    elif isinstance(obj, str) or isinstance(obj, int) or isinstance(obj, float):
        return {
                'type': 'string',
                'content': str(obj)
                }

    elif isinstance(obj, list):
        output = []
        for entry in obj:
            parsed_entry = parse_obj(entry)
            if isinstance(parsed_entry, list):
                # Avoid false positive when child is dict with multiple entries
                if isinstance(entry, list):
                    print("WARNING: Nested lists found", file = sys.stderr)
                output += parsed_entry
            else:
                output.append(parsed_entry)
        return output

    elif isinstance(obj, dict):
        if len(obj) == 0:
            # Assuming that parse_obj is called from an object obtained from
            # YAML parsed file, it is not possible to have an object which is
            # empty dictionary, because if something is empty then it's a None
            raise Exception("Impossible dict length found (can't have empty dict)")

        if len(obj) == 1:
            key = list(obj)[0]
            return parse_dict(key, obj[key])

        else:
            print("WARNING: dictionary with multiple entries found", file = sys.stderr)
            output = []
            for key in obj:
                output.append(parse_dict(key, obj[key]))
            return output
    else:
        raise Exception(f'Unrecognised type "{type(obj)}" of object {obj}')


def parse_diagram(obj):
    if not isinstance(obj, dict):
        raise Exception("Input YAML file is not of type dictionary")

    if len(obj) != 1:
        raise Exception("Input YAML is a dictionary with too many entries. Only one entry (diagram) is allowed")

    key = list(obj)[0]
    id, classes, attributes = parse_key(key)
    if id != "diagram":
        raise Exception(f'Input does not contain diagram entry ("{key}" found)')

    invalid_classes = [ c not in DIAGRAM_CLASSES for c in classes ]
    if any(invalid_classes):
        issue = invalid_classes.index(True)
        raise Exception(f'Invalid class ("{classes[issue]}") in diagram root element')

    invalid_attributes = [ a[0] not in DIAGRAM_ATTRIBUTES for a in attributes ]
    if any(invalid_attributes):
        issue = invalid_attributes.index(True)
        raise Exception(f'Invalid attribute ("{attributes[issue][0]}={attributes[issue][1]}") in diagram root element')

    return {
            'type': 'diagram',
            'classes': classes,
            'attributes': attributes,
            'content': parse_obj(obj[key])
            }


def get_diagram(source):
    with open(source,'r') as file:
        diagram = yaml.safe_load(file)

    return parse_diagram(diagram)
