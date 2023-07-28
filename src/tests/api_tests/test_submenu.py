
from http import HTTPStatus

menu_id = None


class TestSubMenu:

    def test_read_submenus(self, client, fixture_menu):
        global menu_id
        response = client.post('/api/v1/menus', json=fixture_menu[0])
        assert response.status_code == HTTPStatus.CREATED
        global menu_id
        menu_id = str(response.json()['id'])
        response = client.get(f'/api/v1/menus/{menu_id}/submenus')
        assert response.status_code == 200
        assert response.json() == []

    def test_read_menu(self, client, fixture_menu):
        pass
        # global menu_id
        # response = client.get(f'/api/v1/menus/{menu_id}')
        # assert response.json()['title'] == fixture_menu[0]['title']
        # assert response.json()['description'] == fixture_menu[0]['description']

    def test_update_menu(self, client, fixture_menu):
        pass
        # global menu_id
        # response = client.patch(f'/api/v1/menus/{menu_id}', json=fixture_menu[1])
        # assert response.json()['title'] == fixture_menu[1]['title']
        # assert response.json()['description'] == fixture_menu[1]['description']

    def test_delete_menu(self, client):
        pass
        # global menu_id
        # response = client.delete(f'/api/v1/menus/{menu_id}')
        # assert response.status_code == HTTPStatus.OK
