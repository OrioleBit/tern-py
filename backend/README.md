# Order Management App

![coverage](docs/coverage_badge.svg)

## Overview

This is a simple order management Python project following **Clean Architecture** and **DDD** principles.

For run you could follow any oth below path:

    - running in local
    - running with docker

## Feature Status

### User Management

    - register user

### Order Management

    - create order
    - list order (return all for manager user and owned for customer)
    - edit an item in order
    - remove order

User management has not been implemented yet. but as an start follow below steps to create user:

    - for login to admin panel: use admin user with similar words for username and pass.
    - two groups created: **manager** and **customer**
    - two user created (manager, customer) and moved to respectively group.
    - you can add another user and assign them in any of manager or customer group.
    - to work with rest API endpoint use user's Tokens.

## Project Structure

    root/
    ├── src/
    │    └── order_app/
    │        ├── domain/
    │        │   ├─── entities/ --> entities and their related value objects
    │        │   └─── value_objects/ --> common value objects
    │        ├── application/
    │        │   └─── use_cases/
    │        ├── interface/
    │        │   ├─── controllers/
    │        │   ├─── presenters/
    │        │   └─── view_models/
    │        └── infrastructure/
    │            ├─── persistence/
    │            ├─── security/
    │            ├─── web/
    │            │    └─── fastapi/
    │            └─── composition_root
    └── tests/
        └── order_app/
            ├── unit/
            └── contract/

## Request/Response Flow

    HTTP Request (FastAPI)
            ↓
    Interface Layer
    └── Controller
            ↓
    Application Layer
    └── Use Case
            ↓
    Domain Layer
    └── Entities / Value Objects
            ↓
    Application Layer
    └── Use Case Result
            ↓
    Interface Layer
    └── Presenter
            ↓
    ViewModel
            ↓
    HTTP Response (FastAPI)

## Setup / Installation (Local)

### clone the repository

    git clone https://github.com/hassan-mohagheghian/oder_management_ddd_ca
    cd oder_management_ddd_ca

### Create a virtual environment in the root folder

    python -m venv .venv
    source .venv/bin/activate  # Linux/macOS

### Use PYTHONPATH

    export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"  # Linux/macOS

### Install dependencies

    pip install -r requirements.txt

### Running the Application

    fastapi dev ./src/order_app/web_main.py

### Running Tests

    pytest

## Run with Docker (Development)

    docker compose --profile dev up

## Run with Docker (Production)

    docker compose --profile prod up

## Usage

### access to REST api OpenAPI panel

    http://127.0.0.1:8000/docs
