import pytest


class MarkdownFile(pytest.File):

    # https://docs.pytest.org/en/latest/example/nonpython.html#yaml-plugin
    # https://github.com/pytest-dev/pytest/blob/master/src/_pytest/doctest.py#L344
    # https://github.com/pytest-dev/pytest/blob/master/src/_pytest/python.py

    def collect(self):
        print('collect')
        mode = None
        output = []
        fp = self.fspath.open()
        for i, line in enumerate(fp.readlines()):
            output.append('\n')
            if mode is None and line.strip() == '```python':
                mode = 'first_line'
                continue
            elif mode is 'first_line':
                if line.strip() == '':
                    mode = None
                    continue
                mode = 'test'
            elif mode == 'test':
                output.append(line)
            elif line.strip() == '```':
                if mode == 'test':
                    print('emit module')
                    yield ModuleItem(name, self, spec)
                mode = None
                continue


def pytest_collect_file(parent, path):
    if path.ext == '.md':
        print(path, path.ext)
        return MarkdownFile(path, parent)
