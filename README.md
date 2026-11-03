# Python API Automation Framework

A Python-based REST API automation framework built with **Requests, Pytest, JSON Schema, and Allure**, featuring reusable API clients, data-driven testing, error-handling validation, automated execution with GitHub Actions, and real-time CI failure notifications through **n8n and Telegram**.

The project demonstrates practical API testing techniques, maintainable automation framework architecture, CI/CD integration, and an AI-assisted pull request review workflow using **Qodo Code Review**.

## Tech Stack

- **Python 3.13** — Programming language
- **Requests** — HTTP requests and API interactions
- **Pytest** — Test execution, fixtures, assertions, and parameterization
- **JSON Schema** — API response structure validation
- **Allure** — Test reporting, execution steps, and response attachments
- **unittest.mock** — Controlled simulation of HTTP failures
- **GitHub Actions** — Continuous integration and automated test execution
- **n8n** — Workflow automation and CI execution monitoring
- **Telegram Bot API** — Automated CI failure notifications
- **Qodo Code Review** — AI-assisted code review on GitHub pull requests
- **Cursor** — AI-assisted development environment

## API Under Test

The framework uses [JSONPlaceholder](https://jsonplaceholder.typicode.com/), a free fake REST API for testing and prototyping.

**Important:** JSONPlaceholder simulates write operations such as POST, PUT, PATCH, and DELETE. Changes are not permanently stored on the server.

## Project Structure

```
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

| Area                   | Coverage                                                                                    |
| ---------------------- | ------------------------------------------------------------------------------------------- |
| Posts API              | Retrieve individual posts and the posts collection; create, update, patch, and delete posts |
| Posts collection       | Validate HTTP 200, a non-empty JSON list, and every returned post against `POST_SCHEMA`     |
| Negative API scenarios | Non-existing resources and a POST request without a title                                   |
| Users API              | Retrieve individual users and user lists                                                    |
| Data consistency       | Compare a user in the list endpoint with the user details endpoint                          |
| JSON Schema            | Validate post and user response structures                                                  |
| Parameterization       | Validate multiple post IDs and expected user IDs                                            |
| HTTP error handling    | Simulate a timeout and verify exception propagation                                         |

The timeout test uses mocking to simulate a `ReadTimeout` without making a real network request.

**Note:** Because JSONPlaceholder is a fake API, accepting an incomplete POST payload is observed behavior, not proof that the API enforces input validation.

## Getting Started

### Prerequisites

- Python 3.13
- Git
- Allure CLI (optional, for viewing reports locally)

### Clone the Repository

```
git clone https://github.com/BenKeidar/python-api-automation.git
cd python-api-automation
```

### Create a Virtual Environment

**Windows (PowerShell):**

```
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```
python3 -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

```
python -m pip install -r requirements.txt
```

## Running Tests

Run the complete test suite:

```
python -m pytest tests/ -v
```

Run only the Posts API tests:

```
python -m pytest tests/test_posts.py -v
```

Run only the Users API tests:

```
python -m pytest tests/test_users.py -v
```

Run the BaseClient error-handling test:

```
python -m pytest tests/test_base_client.py -v
```

## Allure Reports

Generate Allure result files:

```
python -m pytest tests/ -v --alluredir=allure-results --clean-alluredir
```

View the report locally with Allure CLI:

```
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
5. Adds Allure environment and executor metadata.
6. Uploads raw Allure results.
7. Generates an Allure HTML report.
8. Uploads the HTML report as a downloadable artifact.
9. Sends the test execution result to an authenticated n8n webhook for supported events.

### CI Artifacts

- **allure-results** — Raw Allure test execution data
- **allure-html-report** — Generated HTML report

The HTML report is available as a downloadable GitHub Actions artifact; it is not published as a public website.

The workflow also records Allure environment and executor metadata to identify the test environment and GitHub Actions run.

## CI Failure Notifications — n8n & Telegram

The GitHub Actions pipeline is integrated with an **n8n workflow** that monitors API test execution results and sends automated Telegram alerts when tests fail.

The integration provides real-time visibility into CI failures without requiring manual monitoring of GitHub Actions.

### Notification Architecture

```
GitHub Actions
      |
      v
Run Pytest API Tests
      |
      v
Determine Test Outcome
      |
      v
Authenticated HTTP POST
      |
      v
n8n Webhook
      |
      v
IF Node: status == "failure"
      |
      +---- False (success) ---> No failure alert
      |
      +---- True (failure)
                 |
                 v
            Edit Fields
                 |
                 v
          Telegram Bot
                 |
                 v
        CI Failure Notification
```

### How It Works

1. GitHub Actions executes the API test suite using Pytest.
2. The workflow captures the outcome of the test execution step.
3. A notification step sends an HTTP POST request to the n8n production webhook.
4. The request includes the project name, execution status, branch, GitHub Actions run ID, and run URL.
5. The n8n workflow evaluates whether the status is `failure`.
6. Failed test runs trigger an automated Telegram message containing a direct link to the failed GitHub Actions execution.
7. Successful test runs do not trigger a failure notification.

The notification step runs even when Pytest fails, allowing failure alerts to be sent without changing the original test result.

### Example Webhook Payload

```
{
  "project": "python-api-automation",
  "status": "failure",
  "branch": "main",
  "run_id": 123456789,
  "run_url": "https://github.com/BenKeidar/python-api-automation/actions/runs/123456789"
}
```

### Webhook Security

The integration uses **Header Authentication** to protect the n8n webhook.

The GitHub Actions workflow sends a custom authentication header:

```
X-Webhook-Secret: <secret-value>
```

Sensitive configuration is stored in GitHub Actions repository secrets:

| Secret               | Purpose                               |
| -------------------- | ------------------------------------- |
| `N8N_WEBHOOK_URL`    | Production n8n webhook endpoint       |
| `N8N_WEBHOOK_SECRET` | Authentication secret for the webhook |

The workflow reads these values at runtime rather than hardcoding them in the repository.

For additional security, the notification step excludes `pull_request` events, avoiding the use of webhook credentials in pull request executions.

### Notification Reliability

The GitHub Actions notification step uses:

- `if: always()` to execute after the test step, including when tests fail.
- `steps.api_tests.outcome` to identify the Pytest execution result.
- `continue-on-error: true` to prevent notification delivery problems from overriding the CI test result.
- A 10-second HTTP request timeout to avoid waiting indefinitely for the webhook.

The notification is sent only when the test outcome is `success` or `failure` and the required secrets are available.

**Note:** A successful HTTP response confirms that the webhook accepted the request; it does not independently guarantee downstream Telegram delivery.

### Telegram Failure Alert

When a CI test execution fails, the Telegram bot sends a message similar to:

```
🚨 CI FAILURE
Project: python-api-automation
Branch: test-ci-failure-alert
Run ID: 41631815570
Details: https://github.com/BenKeidar/python-api-automation/actions/runs/41631815570
```

The alert provides enough information to identify the affected project and branch and navigate directly to the failed CI run.

### End-to-End Integration Validation

The notification system was validated through multiple scenarios:

| Scenario                                  | Expected Behavior                                                         | Result    |
| ----------------------------------------- | ------------------------------------------------------------------------- | --------- |
| Successful GitHub Actions execution       | Send `success` to n8n without a Telegram failure alert                    | Passed    |
| Simulated failure sent through PowerShell | Route `failure` through n8n and send Telegram alert                       | Passed    |
| Intentionally failing Pytest test in CI   | GitHub Actions fails and automatically triggers Telegram alert            | Passed    |
| Temporary test branch cleanup             | Remove the intentionally failing test and return to a clean `main` branch | Completed |

For the real failure scenario, a temporary branch named `test-ci-failure-alert` contained an intentionally failing Pytest test.

GitHub Actions correctly reported the execution as failed, while the notification step continued running and triggered an n8n workflow that delivered a Telegram alert.

The temporary branch was deleted locally and remotely after validation. The intentionally failing test was not merged into `main`.

This exercise demonstrates **end-to-end CI/CD integration testing, secure webhook communication, workflow orchestration, negative testing, and automated failure monitoring**.

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

The first reviewed pull request, **[Add posts list API test with JSON Schema validation](https://github.com/BenKeidar/python-api-automation/pull/1)**, introduced `PostsClient.get_posts()` and a test validating the `/posts` collection.

Qodo generated a pull request summary, an architecture diagram, and a high-level assessment. Its review reported:

| Review Category  | Findings |
| ---------------- | -------- |
| Bugs             | 0        |
| Rule violations  | 0        |
| Requirement gaps | 0        |

GitHub displayed **2 successful checks** and no merge conflicts. The pull request was successfully merged into `main`.

Qodo's assessment supported reusing the existing client and post schema rather than introducing an additional collection-level abstraction for this test.

**AI review is an additional quality signal, not a guarantee of defect-free code or a substitute for testing and human judgment.**

## Testing Approach

The project combines API integration tests with an isolated unit test for framework error handling.

Real HTTP requests validate API responses, status codes, response bodies, and schemas.

Mocking is used specifically to test how `BaseClient` handles a simulated network timeout without relying on an actual server failure.

The CI monitoring integration extends this testing approach by validating both successful execution and intentionally triggered failure scenarios.

This separation helps keep tests focused, predictable, and easier to diagnose.

## Key Skills Demonstrated

- REST API automation using Python and Requests
- Pytest fixtures, parameterization, and reusable test architecture
- JSON Schema validation and API response assertions
- HTTP error handling and mocking
- Allure reporting and GitHub Actions CI/CD
- Secure webhook integration using HTTP headers and repository secrets
- n8n workflow orchestration and conditional routing
- Telegram Bot API integration for automated failure notifications
- End-to-end validation of CI failure monitoring
- AI-assisted pull request review with Qodo
- Git branching, pull requests, and repository maintenance

## Repository

[GitHub — Python API Automation](https://github.com/BenKeidar/python-api-automation)
