from sqlalchemy import select, insert, update, delete, func, exists
from .schemas import Dish, Submenu
from sqlalchemy.exc import IntegrityError

from dataclasses import dataclass


@dataclass
class CRUDDish:

    @staticmethod
    def check_menu(menu_id, submenu_id, session):
        exists_query = select(exists().where(Submenu.id == submenu_id).where(Submenu.menu_id == menu_id))
        if session.execute(exists_query).scalar():
            return True
        return False

    @staticmethod
    def get_dish_count(submenu_id, session):
        dish_count = session.query(func.count(Dish.id)).join(Submenu).filter(Submenu.id == submenu_id).scalar()
        return dish_count

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
        is_exist = CRUDDish.check_menu(menu_id, submenu_id, session)
        if not is_exist:
            return []
        result = {'Dishes': []}
        dishes = session.query(Dish).where(Dish.submenu_id == submenu_id).all()
        if dishes:
            for dish in dishes:
                dish_count = CRUDDish.get_dish_count(submenu_id, session)
                result['Dishes'].append(
                    {'Dish ID': dish.id, 'Title': dish.title, 'Price': dish.price, 'Dish Count': dish_count}
                )
            return result
        return []

    @staticmethod
    def create_dish(menu_id, submenu__id, dish, session):
        is_exist = CRUDDish.check_menu(menu_id, submenu__id, session)
        if not is_exist:
            return False
        stmt = insert(Dish).values(submenu_id=submenu__id,
                                   title=dish.title,
                                   description=dish.description,
                                   price=dish.price).returning(Dish)
        try:
            result = session.execute(stmt).scalar()
            session.commit()
            result = CRUDDish.prepare_response(result)
            return result
        except IntegrityError as e:
            print(f'Error: {e.orig}')
            return []

    @staticmethod
    def update_dish(menu_id, submenu_id, dish_id, dish, session):
        is_exist = CRUDDish.check_menu(menu_id, submenu_id, session)
        if not is_exist:
            return False
        stmt = session.execute(update(Dish).where(Dish.id == dish_id,
                                                  Dish.submenu_id == submenu_id).values(**dish.dict()).returning(
            Dish))
        updated_row = stmt.scalar()
        if updated_row:
            session.commit()
            result = CRUDDish.prepare_response(updated_row)
            return result
        return False

    @staticmethod
    def delete_dish(menu_id, submenu_id, dish_id, session):
        is_exist = CRUDDish.check_menu(menu_id, submenu_id, session)
        if not is_exist:
            return False
        stmt = session.execute(delete(Dish).where(Dish.id == dish_id))
        if stmt.rowcount > 0:
            session.commit()
            return True
        return False

    @staticmethod
    def get_dish(menu_id, submenu_id, dish_id, session):
        is_exist = CRUDDish.check_menu(menu_id, submenu_id, session)
        if not is_exist:
            return False
        query = select(Dish).where(Dish.id == dish_id)
        result = session.execute(query).scalar()
        if result:
            result = CRUDDish.prepare_response(result)
            return result
        else:
            return []
