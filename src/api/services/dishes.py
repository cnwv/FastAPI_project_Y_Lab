from sqlalchemy import delete, exists, insert, select, update
from sqlalchemy.exc import IntegrityError

from src.api.models import Dish, Submenu


class DishService:
    @staticmethod
    def check_menu(menu_id, submenu_id, session):
        exists_query = select(
            exists().where(Submenu.id == submenu_id).where(Submenu.menu_id == menu_id)
        )
        if session.execute(exists_query).scalar():
            return True
        return False

    @staticmethod
    def prepare_response(dish):
        response = dict()
        response['id'] = str(dish.id)
        response['title'] = str(dish.title)
        response['description'] = str(dish.description)
        response['price'] = str(dish.price)
        return response

    @staticmethod
    def get_dishes(menu_id, submenu_id, session):
        is_exist = DishService.check_menu(menu_id, submenu_id, session)
        if not is_exist:
            return []
        result = {'Dishes': []}
        dishes = session.query(Dish).where(Dish.submenu_id == submenu_id).all()
        if dishes:
            for dish in dishes:
                result['Dishes'].append(DishService.prepare_response(dish))
            return result
        return []

    @staticmethod
    def create_dish(menu_id, submenu__id, dish, session):
        is_exist = DishService.check_menu(menu_id, submenu__id, session)
        if not is_exist:
            return False
        stmt = (
            insert(Dish)
            .values(
                submenu_id=submenu__id,
                title=dish.title,
                description=dish.description,
                price=dish.price,
            )
            .returning(Dish)
        )
        try:
            dish = session.execute(stmt).scalar()
            session.commit()
            result = DishService.prepare_response(dish)
            return result
        except IntegrityError as e:
            print(f'Error: {e.orig}')
            return []

    @staticmethod
    def update_dish(menu_id, submenu_id, dish_id, dish, session):
        is_exist = DishService.check_menu(menu_id, submenu_id, session)
        if not is_exist:
            return False
        stmt = session.execute(
            update(Dish)
            .where(Dish.id == dish_id, Dish.submenu_id == submenu_id)
            .values(**dish.dict())
            .returning(Dish)
        )
        updated_dish = stmt.scalar()
        if updated_dish:
            session.commit()
            result = DishService.prepare_response(updated_dish)
            return result
        return False

    @staticmethod
    def delete_dish(menu_id, submenu_id, dish_id, session):
        is_exist = DishService.check_menu(menu_id, submenu_id, session)
        if not is_exist:
            return False
        stmt = session.execute(delete(Dish).where(Dish.id == dish_id))
        if stmt.rowcount > 0:
            session.commit()
            return True
        return False

    @staticmethod
    def get_dish(menu_id, submenu_id, dish_id, session):
        is_exist = DishService.check_menu(menu_id, submenu_id, session)
        if not is_exist:
            return False
        query = select(Dish).where(Dish.id == dish_id)
        dish = session.execute(query).scalar()
        if dish:
            result = DishService.prepare_response(dish)
            return result
        else:
            return []
