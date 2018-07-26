import imp

import pytest
from _pytest.python import Module
from _pytest import nodes


class MarkdownItem(Module):

    def __init__(self, name, file, code, nodeid=None):
        self._code_obj = imp.new_module(name)
        exec(code, self._code_obj.__dict__)
        super().__init__(name, file, nodeid=nodeid)

    def _getobj(self):
        return self._code_obj


class MarkdownFile(pytest.File):

    def collect(self):
        print(self.nodeid)
        mode = None
        stack = [(0, self, self.name)]
        output = []
        fp = self.fspath.open()
        for i, line in enumerate(fp.readlines()):
            if mode is None and line.strip() == '```python':
                mode = 'first_line'
                continue

            elif mode is None:
                if line.startswith('#'):
                    level, name = line.split(' ', 1)
                    name = name.strip().lower().replace(' ', '-')
                    level_count = len(level)

                    while stack[-1][0] >= level_count:
                        stack.pop()

                    nodeid = '::'.join(s[2] for s in stack if s[2]) + '::' + name
                    stack.append((level_count, pytest.Item(name, stack[-1][1], nodeid=nodeid), name))
                    print(stack[-1][1].nodeid)

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
                    if output[0].lower().strip() == '# conftest.py':
                        nodeid = stack[-1][1].nodeid
                    else:
                        nodeid = stack[-1][1].nodeid + '::' + name
                    mi = MarkdownItem(name, stack[-1][1], '\n'.join(output), nodeid=nodeid)
                    print(mi.nodeid)
                    yield mi

                output = []
                mode = None
                continue

            elif mode == 'test':
                output.append(line)


def pytest_collect_file(parent, path):
    if path.ext == '.md':
        return MarkdownFile(path, parent)
