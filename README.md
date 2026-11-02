# Python API Automation Framework

A Python-based REST API automation framework built with **Requests, Pytest, JSON Schema, and Allure**, featuring reusable API clients, data-driven testing, error-handling validation, and automated execution with GitHub Actions.

The project demonstrates practical API testing techniques, maintainable automation framework architecture, and an AI-assisted pull request review workflow using **Qodo Code Review**.

## Tech Stack

- **Python 3.13** — Programming language
- **Requests** — HTTP requests and API interactions
- **Pytest** — Test execution, fixtures, assertions, and parameterization
- **JSON Schema** — API response structure validation
- **Allure** — Test reporting, execution steps, and response attachments
- **unittest.mock** — Controlled simulation of HTTP failures
- **GitHub Actions** — Continuous integration and automated test execution
- **Qodo Code Review** — AI-assisted code review on GitHub pull requests
- **Cursor** — AI-assisted development environment

## API Under Test

The framework uses [JSONPlaceholder](https://jsonplaceholder.typicode.com/), a free fake REST API for testing and prototyping.

**Important:** JSONPlaceholder simulates write operations such as POST, PUT, PATCH, and DELETE. Changes are not permanently stored on the server.

## Project Structure

```text
python-api-automation/
├── .github/
│   └── workflows/
│       └── api-tests.yml
├── clients/
│   ├── base_client.py
│   ├── posts_client.py
│   └── users_client.py
├── schemas/
│   ├── post_schema.py
│   └── user_schema.py
├── tests/
│   ├── conftest.py
│   ├── test_base_client.py
│   ├── test_posts.py
│   └── test_users.py
├── utils/
│   └── allure_helpers.py
├── first_api_request.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Framework Architecture

### API Client Layer

The framework separates HTTP communication from test logic.

- `BaseClient` provides shared HTTP request handling, a base URL, a timeout, and request exception diagnostics.
- `PostsClient` implements operations for the `/posts` resource, including retrieving individual posts and the posts collection.
- `UsersClient` implements operations for the `/users` resource.

This design reduces code duplication and keeps tests readable.

### Pytest Fixtures

Reusable API clients are provided to tests through fixtures defined in `tests/conftest.py`.

### JSON Schema Validation

Response schemas validate expected data types, required fields, and nested response structures. The posts collection test validates each returned post against the existing `POST_SCHEMA`.

### Allure Reporting

Tests include Allure metadata, execution steps, and HTTP response attachments. HTTP request exceptions are also documented for easier troubleshooting.

## Test Coverage

The framework currently contains **17 Pytest test cases**, including parameterized scenarios.

| Area | Coverage |
| --- | --- |
| Posts API | Retrieve individual posts and the posts collection; create, update, patch, and delete posts |
| Posts collection | Validate HTTP 200, a non-empty JSON list, and every returned post against `POST_SCHEMA` |
| Negative API scenarios | Non-existing resources and a POST request without a title |
| Users API | Retrieve individual users and user lists |
| Data consistency | Compare a user in the list endpoint with the user details endpoint |
| JSON Schema | Validate post and user response structures |
| Parameterization | Validate multiple post IDs and expected user IDs |
| HTTP error handling | Simulate a timeout and verify exception propagation |

The timeout test uses mocking to simulate a `ReadTimeout` without making a real network request.

**Note:** Because JSONPlaceholder is a fake API, accepting an incomplete POST payload is observed behavior, not proof that the API enforces input validation.

## Getting Started

### Prerequisites

- Python 3.13
- Git
- Allure CLI (optional, for viewing reports locally)

### Clone the Repository

```bash
git clone https://github.com/BenKeidar/python-api-automation.git
cd python-api-automation
```

### Create a Virtual Environment

**Windows (PowerShell):**

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

```bash
python -m pip install -r requirements.txt
```

## Running Tests

Run the complete test suite:

```bash
python -m pytest tests/ -v
```

Run only the Posts API tests:

```bash
python -m pytest tests/test_posts.py -v
```

Run only the Users API tests:

```bash
python -m pytest tests/test_users.py -v
```

Run the BaseClient error-handling test:

```bash
python -m pytest tests/test_base_client.py -v
```

## Allure Reports

Generate Allure result files:

```bash
python -m pytest tests/ -v --alluredir=allure-results --clean-alluredir
```

View the report locally with Allure CLI:

```bash
allure serve allure-results
```

Allure CLI is a separate installation from the `allure-pytest` Python package.

## Continuous Integration

The project includes a GitHub Actions workflow located at:

`.github/workflows/api-tests.yml`

The workflow runs on:

- Push events
- Pull requests
- Manual execution through GitHub Actions

The CI pipeline:

1. Checks out the repository.
2. Configures Python 3.13 on Ubuntu.
3. Installs dependencies from `requirements.txt`.
4. Executes the Pytest suite.
5. Uploads raw Allure results.
6. Generates an Allure HTML report.
7. Uploads the HTML report as a downloadable artifact.

### CI Artifacts

- **allure-results** — Raw Allure test execution data
- **allure-html-report** — Generated HTML report

The HTML report is available as a downloadable GitHub Actions artifact; it is not published as a public website.

The workflow also records Allure environment and executor metadata to identify the test environment and GitHub Actions run.

## AI-Assisted Code Review with Qodo

The repository uses **Qodo Code Review**, integrated with GitHub, to provide automated AI-assisted reviews of pull requests.

The development and review workflow is:

1. Create a dedicated feature branch.
2. Implement changes and run the test suite locally.
3. Push the branch and open a pull request targeting `main`.
4. Review GitHub Actions checks and Qodo's feedback.
5. Address any relevant findings before merging.
6. Merge the pull request and synchronize the local `main` branch.

### Pull Request #1 — Posts Collection Test

The first reviewed pull request, [**Add posts list API test with JSON Schema validation**](https://github.com/BenKeidar/python-api-automation/pull/1), introduced `PostsClient.get_posts()` and a test validating the `/posts` collection.

Qodo generated a pull request summary, an architecture diagram, and a high-level assessment. Its review reported:

| Review category | Findings |
| --- | ---: |
| Bugs | 0 |
| Rule violations | 0 |
| Requirement gaps | 0 |

GitHub displayed **2 successful checks** and no merge conflicts. The pull request was successfully merged into `main`.

Qodo's assessment supported reusing the existing client and post schema rather than introducing an additional collection-level abstraction for this test.

**AI review is an additional quality signal, not a guarantee of defect-free code or a substitute for testing and human judgment.**

## Testing Approach

The project combines API integration tests with an isolated unit test for framework error handling.

Real HTTP requests validate API responses, status codes, response bodies, and schemas.

Mocking is used specifically to test how `BaseClient` handles a simulated network timeout without relying on an actual server failure.

This separation helps keep tests focused, predictable, and easier to diagnose.

## Repository

[GitHub — Python API Automation](https://github.com/BenKeidar/python-api-automation)
