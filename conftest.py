import imp

import pytest
from _pytest.python import PyCollector
from _pytest import nodes


class MarkdownItem(nodes.File, PyCollector):

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
        output = []
        fp = self.fspath.open()
        for i, line in enumerate(fp.readlines()):
            if mode is None and line.strip() == '```python':
                mode = 'first_line'
                continue
            elif mode is 'first_line':
                if line.strip() == '':
                    mode = None
                    continue
                mode = 'test'
                output.append(line)
            elif line.strip() == '```':
                if mode == 'test':
                    yield MarkdownItem(f'line_{i}', self, '\n'.join(output))
                output = []
                mode = None
                continue
            elif mode == 'test':
                output.append(line)


def pytest_collect_file(parent, path):
    if path.ext == '.md':
        print(path, path.ext)
        return MarkdownFile(path, parent)
