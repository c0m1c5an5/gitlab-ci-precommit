import pytest


@pytest.fixture
def simple_yml_unsorted() -> str:
    return """
x-ray:
  oscar: 1
  papa: 2
alfa:
  lima: 4
  quebec: 5
""".lstrip()


@pytest.fixture
def simple_yml_sorted() -> str:
    return """
alfa:
  lima: 4
  quebec: 5
x-ray:
  oscar: 1
  papa: 2
""".lstrip()


@pytest.fixture
def gitlab_ci_unformatted() -> str:
    return """
image: golang:latest

stages:
  - test
  - build
  - deploy

format:
  stage: test
  script:
    - go fmt $(go list ./... | grep -v /vendor/)
    - go vet $(go list ./... | grep -v /vendor/)
    - go test -race $(go list ./... | grep -v /vendor/)

compile:
  script:
    - mkdir -p mybinaries
    - go build -o mybinaries ./...
  artifacts:
    paths:
      - mybinaries
  stage: build

deploy:
  stage: deploy
  script: echo "Define your deployment script!"
  environment: production
""".lstrip()


@pytest.fixture
def gitlab_ci_formatted() -> str:
    return """
stages:
  - test
  - build
  - deploy
image: golang:latest
format:
  stage: test
  script:
    - go fmt $(go list ./... | grep -v /vendor/)
    - go vet $(go list ./... | grep -v /vendor/)
    - go test -race $(go list ./... | grep -v /vendor/)
compile:
  stage: build
  artifacts:
    paths:
      - mybinaries
  script:
    - mkdir -p mybinaries
    - go build -o mybinaries ./...
deploy:
  stage: deploy
  environment: production
  script: echo "Define your deployment script!"
""".lstrip()
