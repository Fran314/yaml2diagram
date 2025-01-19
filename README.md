# yaml2diagram

`yaml2diagram` builds pretty diagrams declared in YAML, into html files

## How to use

Assuming that `input.yml` is a YAML file using the `yaml2diagram` syntax to
represent the desired diagram, convert this diagram into an html file
`output.html` with

```bash
yaml2diagram input.yml output.html
```

to convert the `input.yml` file to a diagram into `output.html`

## `yaml2diagram` file syntax

Here is an example of a `yaml` file using the syntax for `yaml2diagram`

```yaml
root:
    .box.dotted&label=homelab:
        .box: nested
        .: content
        .icon.abs.bottom.red: lock
    .folder: |
        multiline
        string
        here!
    .box.skew.b-red.t-blue: colored skewed box!

links: !TODO
```

A `yaml2diagram` file is composed of 2 main objects:

-   `root`, which will contain the components of the diagram
-   `links`, which will contain the arrows of the diagram

### Labels

Each object has its own key. Some examples of object keys are:

```
root
.folder
.box.dashed&label=homelab
root.c2
.icon.abs
&label=server
.
```

A key is composed of an `id`, some `classes` and some `attributes`. In most
cases, these map 1:1 to html DOMs.

Keys are formatted as follows:

```
ID.CLASS1.CLASS2.CLASSn&ATTR1=VAL1&ATTR2=VAL2&ATTR3=VALn
```

A key can have at most one `id`, while it can have as many (or as few) `classes`
and `attributes` as one whishes.

None of the components of a key (`id`, `classes` and `attributes`) is required:
a key could be only an `id` (eg `root`), only a `class` (eg `.box`), only an
attribute (eg `&label=server`) or completely empty (read note below).

> [!NOTE]  
> "Empty" keys are allowed, and they get mapped to a `<div>...</div>`, but since
> empty keys are not allowed in YAML, one must use a single dot `.` when
> intending an object without id, classes nor attributes

### Root

The `root` object is the root of the diagram and contains every object that gets
displayed. Its `id` MUST be exactly `root`, but it can have class modifiers.
These class modifiers are special and work only on the `root` object.

Without any class modifier, `root` displays as a list of its content from top to
bottom, that is it uses `display: flex` with `flex-direction: column`

The currently supported class modifiers are:

| Class                   | Effect                                                                                                          | CSS                                                    |
| ----------------------- | --------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| `.flex-row`             | makes `root` display from left to right instead of top to bottom                                                | `flex-direction: row`                                  |
| `.col-1`, ..., `.col-8` | makes `root` display as a grid with `n` columns, instead of a list, where `n` refers to the number in the class | `display: grid; grid-template-columns: repeat(n, 1fr)` |

### Classes

Classes for regular objects are divided in containers, modifiers and
meta-classes.

A container class specifies the overall shape of object it applies to. The
container classes are:

| Class     | Shape                            |
| --------- | -------------------------------- |
| `.box`    | a rectangle with rounded corners |
| `.folder` | a folder                         |

Next, modifier classes modify the appearence of the object, either of the
container or of its content. The modifier classes are:

| Class        | Effect                                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------------------------------ |
| `.dashed`    | makes the border of the container dotted instead of solid                                                          |
| `.skew`      | skews the container (`.box` becomes a parallelogram)                                                               |
| `.<color>`   | makes the container and its content of color `<color>`, where `<color>` can be chosen between: `red`, `blue`       |
| `.b-<color>` | makes the container (but not its content) of color `<color>`, where `<color>` can be chosen between: `red`, `blue` |
| `.t-<color>` | makes the content (but not the container) of color `<color>`, where `<color>` can be chosen between: `red`, `blue` |

### Meta-clsasses

#### `.icon`

The `.icon` meta-class is used to draw Material Icons in the diagram. An `.icon`
object MUST contain only a string, which will be converted to the corresponding
Material Icon.

All the `.<color>` modifier classes work on icons, and additionally, `.icon`
objects can use the following modifying classes:

| Class     | Effect                                                                                                                             |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `.abs`    | detaches the icon from the container, making its position absolute (by default, positione in the absolute center of the container) |
| `.top`    | when in combination with `.abs`, aligns the icon to the top                                                                        |
| `.bottom` | when in combination with `.abs`, aligns the icon to the bottom                                                                     |
| `.left`   | when in combination with `.abs`, aligns the icon to the left                                                                       |
| `.right`  | when in combination with `.abs`, aligns the icon to the right                                                                      |

### Attributes

Here is a list of supported attributes:

| Attribute | Effect                                                      |
| --------- | ----------------------------------------------------------- |
| `label`   | displays the label above the container, aligned to the left |

### Links

Links don't currently work

## Developement

<details>

<summary>Developement tips</summary>

For a quick and dirty hot-reload developement, add the following tag to the
index.html head:

```html
<meta http-equiv="refresh" content="1" />
```

And then run the following command

```bash
ls -A1 | grep -v 'index.local.html' | entr -r bash -c './yaml2diagram diagram.local.yml index.local.html'
```

This is really a terrible way to do this, but it works and it doesn't require
any fancy setup (except having installed entr I guess)

</details>
