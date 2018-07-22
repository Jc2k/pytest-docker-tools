from setuptools import setup

setup(
    name='pytest-docker-tools',
    version='0.0.2.dev0',
    description='py.test fixture factories for Docker integration testing',
    packages = ['pytest_docker_tools'],
    entry_points = {
        'pytest11': [
            'docker_tools = pytest_docker_tools.plugin',
        ]
    },
    install_requires = [
        'docker',
    ],
    classifiers=[
        'Framework :: Pytest',
    ],
)
