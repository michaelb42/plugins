# w3c_validate
W3C HTML Validator plugin for generated content.

This is a plugin for Nikola that submits generated HTML content to the
[W3C Markup Validation Service](http://validator.w3.org/).

This is a ported and updated version of [José Moreiras](https://github.com/zemanel) Pelican plugin [w3c_validate](https://github.com/getpelican/pelican-plugins/tree/master/w3c_validate).

## Usage

```
    Purpose: validate generated HTML using the W3C HTML Validator service.
    Usage:   nikola w3c_validate [-p, --posts] [-v, --verbose] [-e, --errors-only]

    Options:
      -e, --errors-only         Show only errors.  (config: errors-only)
      -p, --posts               Validate posts and pages only.  (config: posts)
      -v, --verbose             Be more verbose.  (config: verbose)
```

## Dependencies

* [py_w3c](https://pypi.python.org/pypi/py_w3c/), which can be installed with pip:

    $ pip install py_w3c

or from this plugins directory

    $ pip install -r requirements.txt
