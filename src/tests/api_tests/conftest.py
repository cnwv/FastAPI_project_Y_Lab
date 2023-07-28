import pytest


@pytest.fixture(autouse=True)
def fixture_menu():
    menus = [{'title': 'New menu', 'description': 'New description'},
             {'title': 'Updated menu', 'description': 'Updated description'}]
    return menus
