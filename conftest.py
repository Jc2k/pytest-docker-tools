import imp

import pytest
from _pytest.python import Module
from _pytest import nodes


class MarkdownItem(Module):

    def __init__(self, name, file, code):
        self._code_obj = imp.new_module(name)
        exec(code, self._code_obj.__dict__)
        super().__init__(name, file)

    def _getobj(self):
        return self._code_obj


class MarkdownFile(pytest.File):

    # https://docs.pytest.org/en/latest/example/nonpython.html#yaml-plugin
    # https://github.com/pytest-dev/pytest/blob/master/src/_pytest/doctest.py#L344
    # https://github.com/pytest-dev/pytest/blob/master/src/_pytest/python.py

    def collect(self):
        mode = None
        stack = [(0, self, '')]
        output = []
        fp = self.fspath.open()
        for i, line in enumerate(fp.readlines()):
            if mode is None and line.strip() == '```python':
                mode = 'first_line'
                continue

            elif mode is None:
                if line.startswith('#'):
                    level, name = line.split(' ', 1)
                    level_count = len(level)

                    while stack[-1][0] >= level_count:
                        stack.pop()

                    nodeid = '/'.join(s[2] for s in stack) + '/' + name.strip()
                    stack.append((level_count, pytest.Item(nodeid, stack[-1][1]), name.strip()))
                    
                    current_level = level_count
 
            elif mode is 'first_line':
                if line.strip() == '':
                    mode = None
                    continue
                mode = 'test'
                output.append(line)

            elif line.strip() == '```':
                if mode == 'test':
                    name = f'line_{i}'
                    mi = MarkdownItem(f'line_{i}', stack[-1][1], '\n'.join(output))
                    yield mi
                output = []
                mode = None
                continue

            elif mode == 'test':
                output.append(line)


def pytest_collect_file(parent, path):
    if path.ext == '.md':
        return MarkdownFile(path, parent)
