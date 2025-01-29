# 2024 TV program items management system test automation
## Pytest + Python

## Overview
The purpose of this project is to create a comprehensive suite of automated tests, specifically targeting a microservice responsible for managing TV program items. This microservice provides core CRUD operations for TV program entries, forming a critical part of the overall system. The automated tests focus on classical API testing.

---
### Prerequisites (Before Running Locally)

1. Install the required Python packages:

```bash
  pip3 install -r requirements.txt
```
2. Using `.env_example` file create `.env` file to load environment variables

---
## Running Tests

To execute the tests, use the following commands:

=== Basic Test Run ===

Run all tests with verbose output:
```bash
  pytest -v ./tests 
```

or simply:

```bash
  pytest -v
```
---

## Allure

run with Allure reports:

```bash
  pytest -v --alluredir=allure-results
```

start Allure:

```bash
  allure serve allure-results
```