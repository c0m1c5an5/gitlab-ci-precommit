import pytest


@pytest.fixture
def gitlab_ci_valid() -> str:
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
