#! /bin/sh
set -e
alias python="poetry run python"
poetry run find . -name '*.py' -exec pyupgrade --py36-plus {} +
python -m black tests pytest_docker_tools
python -m isort tests pytest_docker_tools
python -m black tests pytest_docker_tools --check --diff
python -m flake8 tests pytest_docker_tools
python -m pytest
