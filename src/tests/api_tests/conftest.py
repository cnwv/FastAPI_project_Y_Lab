import pytest


@pytest.fixture(autouse=True)
def fixture_menu():
    menus = [{'title': 'New menu', 'description': 'New description'},
             {'title': 'Updated menu', 'description': 'Updated description'}]
    return menus


@pytest.fixture(autouse=True)
def fixture_submenu():
    submenus = [{'title': 'New submenu', 'description': 'New description'},
                {'title': 'Updated submenu', 'description': 'Updated description'}]
    return submenus


@pytest.fixture(autouse=True)
def fixture_dish():
    dishes = [{'title': 'New dish', 'description': 'New description', 'price': 1111.01},
              {'title': 'Updated dish', 'description': 'Updated description', 'price': 2222.01}]
    return dishes
