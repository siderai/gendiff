[![Hexlet Status](https://github.com/siderai/python-project-lvl2/workflows/hexlet-check/badge.svg)](https://github.com/siderai/gendiff/actions/workflows/CI.yml)
[![gendiff-check](https://github.com/siderai/gendiff/actions/workflows/CI.yml/badge.svg)](https://github.com/siderai/gendiff/actions/workflows/CI.yml)
<a href="https://codeclimate.com/github/siderai/gendiff/test_coverage"><img src="https://api.codeclimate.com/v1/badges/7a99cbe3b491ee26aa28/test_coverage" /></a>

# Difference calculator for JSON/YAML

A Python CLI tool that compares two data structures and creates human-friendly output

```
gendiff --help
usage: gendiff [-h] [-f FORMAT] first_file second_file

Generate diff

positional arguments:
  first_file
  second_file

optional arguments:
  -h, --help            show this help message and exit
  -f FORMAT, --format FORMAT
                        set format of output
```

**_Codebase info_**: 

In logic.py there is a decoding and comparison functionality.

In formatters.py there are functions to generate output from internal comparison data.

In gendiff.py there is "generate_diff" function, which creates data pipeline, connecting all the pieces together. Running this module as a script will provide CLI. In case you need a direct access, the whole functionality can easily be imported to your project with "generate_diff" as a library function. 

Training project at hexlet.io.

## Stack:

Python3
• Pytest
• Poetry
• JSON
• PyYAML
• Argparse
• Linux
• Git
• Github Actions (CI)
• MyPy
• Flake8
• CodeClimate
• Make

## Acquired skills: 
1. Working with complex data structures
2. Parsing and formatting using Python
3. Building an effective data pipeline with CLI
4. Using recursive algorithms for tree traversal
5. Testing and coding within short development cycle (TDD)


## Quickstart:

``` 
git clone https://github.com/siderai/gendiff
cd gendiff
make package-install
make test
gendiff --help
```

### Supports different output formats:
### stylish
``` bash
{
  - follow: false
    host: hexlet.io
  - proxy: 123.234.53.22
  - timeout: 50
  + timeout: 20
  + verbose: true
}
```

### plain
``` bash
Property 'follow' was removed
Property 'proxy' was removed
Property 'timeout' was updated. From 50 to 20
Property 'verbose' was added with value: true
```

### JSON
``` bash
{"  host": "hexlet.io", "- timeout": 50, "+ timeout": 20, "- follow": false, "- proxy": "123.234.53.22", "+ verbose": true}
```
