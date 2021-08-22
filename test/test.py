from datetime import datetime, timedelta
import pytest
from models import User, Menu, Dish

def test_user_add_and_get():
    User.add('test1', 'pass1')
    user = User.getUser('test1')
    assert user is not None

def test_menu_add():
    Menu.add('test1')
    menu = Menu.get('test1')
    assert menu is not None

def test_menu_delete():
    menu = Menu.get('test1')
    menu.delete()
    menu = Menu.get('test1')
    assert menu is None

def test_menu_get():
    Menu.add('test1')
    menuList1 = Menu.getAll()
    Dish.add("test1",'test1','test1',1,1,True)
    menuList2 = Menu.getAll()
    assert len(menuList1) == 0 and len(menuList2) != 0

def test_dish_update():
    date1 = datetime.now() + timedelta(days=7)
    date2 = datetime.now() + timedelta(days=7)
    dish = Dish.list("test1", '', date1, date2)
    assert len(dish) == 0

