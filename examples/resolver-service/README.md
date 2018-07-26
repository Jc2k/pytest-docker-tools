# Example IP Resolver Microservice

This folder contains a microservice that resolves example.com. It is implemented in Python 3 and is tested using `pytest-docker-tools`.

The `api` folder contains the actual microservice. It's a simple `http.server` based service that runs on port 8080.

The `dns` folder contains a fake dns server so we can test 'real' DNS resolves from our test environment.
