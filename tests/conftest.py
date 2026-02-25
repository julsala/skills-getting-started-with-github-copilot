import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities as original_activities


@pytest.fixture
def client():
    # deep copy the activities so each test starts fresh
    activities_backup = copy.deepcopy(original_activities)
    client = TestClient(app)
    yield client
    # restore the original data after test
    original_activities.clear()
    original_activities.update(activities_backup)
