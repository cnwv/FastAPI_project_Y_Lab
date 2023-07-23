from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, UniqueConstraint, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

metadata = MetaData()
Base = declarative_base(metadata=metadata)


class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True, default='None')


class Submenu(Base):
    __tablename__ = "submenus"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True, default='None')
    menu_id = Column(Integer, ForeignKey('menus.id', ondelete='CASCADE'))
    menu = relationship("Menu", back_populates="submenus")
    __table_args__ = (UniqueConstraint('menu_id', name='uq_submenu_title_menu_id'),)


class Dish(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True, default='None')
    price = Column(DECIMAL(precision=10, scale=2), nullable=False)
    submenu_id = Column(Integer, ForeignKey('submenus.id', ondelete='CASCADE'))
    submenu = relationship("Submenu", back_populates="dishes")
    __table_args__ = (UniqueConstraint('title', 'submenu_id', name='uq_dish_title_submenu_id'),)


Menu.submenus = relationship("Submenu", order_by=Submenu.id, back_populates="menu")
Submenu.dishes = relationship("Dish", order_by=Dish.id, back_populates="submenu")
