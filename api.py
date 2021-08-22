from models import *
from flask import request, Response, jsonify

@app.route('/movies', methods=['GET'])
def get_movies():
    '''Function to get all the movies in the database'''
    return jsonify({'Movies': Movie.get_all_movies()})



@app.route('/user', methods=['POST'])
def addUser():
    request_data = request.get_json()  # getting data from client
    err = User.add(request_data["name"], request_data["password"])
    if err is None:
        return Response("User added", 201, mimetype='application/json')
    else:
        return Response("User already exist", 409, mimetype='application/json')


@app.route('/login', methods=['GET'])
def loginUser():
    userName = request.headers['userName']
    if len(userName) == 0 or isinstance(userName, str) == False:
        return Response("userName wrrong value", status=400, mimetype='application/json')
    user = User.getUser(userName)
    password = request.headers['password']
    if len(password) == 0 or isinstance(password, str) == False:
        return Response("password wrrong value", status=400, mimetype='application/json')
    token = user.checkPassword(password)
    if len(token) > 0:
        return Response(token, status=201, mimetype='application/json')
    else:
        return Response("wrong password or userName", status=403, mimetype='application/json')


@app.route('/menu', methods=['POST'])
def addMenu():
    request_data = request.get_json()  # getting data from client
    name = request_data["name"]
    if len(name) == 0 or isinstance(name, str) == False:
        return Response("name wrrong value", status=400, mimetype='application/json')
    err = Menu.add(name)
    if err is None:
        return Response("Menu added", 201, mimetype='application/json')
    else:
        return Response("Menu already exist", 409, mimetype='application/json')


@app.route('/menu', methods=['DELETE'])
def removeMenu():
    name = request.headers['name']
    if len(name) == 0 or isinstance(name, str) == False:
        return Response("name wrrong value", status=400, mimetype='application/json')
    menu = Menu.get(name)
    print(menu)
    print(type(menu))
    if menu is None:
        return Response("menu not found", status=404, mimetype='application/json')
    menu.delete()
    return Response("menu deleted", status=200, mimetype='application/json')


@app.route('/menu', methods=['GET'])
def getMenu():
    orderBy = request.headers['orderBy']

    if orderBy == '':
        return jsonify({'menu': Menu.getAll()})
    elif orderBy == 'name':
        return jsonify({'menu': Menu.getAllOBName()})
    elif orderBy == 'dish':
        return jsonify({'menu': Menu.getAllOBDish()})
    else:
        return Response("orderBy wrrong value", status=400, mimetype='application/json')



@app.route('/dish', methods=['POST'])
def adddish():
    request_data = request.get_json()  # getting data from client
    name = request_data["name"]
    if len(name) == 0 or isinstance(name, str) == False:
        return Response("name wrrong value", status=400, mimetype='application/json')

    menuName = request_data["menuName"]
    if len(menuName) == 0 or isinstance(menuName, str) == False:
        return Response("menuName wrrong value", status=400, mimetype='application/json')

    description = request_data["description"]
    if len(description) == 0 or isinstance(description, str) == False:
        return Response("description wrrong value", status=400, mimetype='application/json')

    price = request_data["price"]
    if price <=0 or isinstance(price, int) == False:
        return Response("price wrrong value", status=400, mimetype='application/json')

    timePreparation = request_data["timePreparation"]
    if timePreparation <= 0 or isinstance(timePreparation, int) == False:
        return Response("timePreparation wrrong value", status=400, mimetype='application/json')

    vegan = request_data["vegan"]
    if isinstance(vegan, bool) == False:
        return Response("vegan wrrong value", status=400, mimetype='application/json')

    err = Dish.add(name, menuName, description, price, timePreparation, vegan)
    if err is None:
        return Response("Dish added", 201, mimetype='application/json')
    else:
        return Response("db error", 409, mimetype='application/json')

@app.route('/dish', methods=['PUT'])
def updatedish():
    request_data = request.get_json()  # getting data from client
    id = request_data["id"]
    if isinstance(id, int) == False:
        return Response("name wrrong value", status=400, mimetype='application/json')
    name = request_data["name"]
    if len(name) == 0 or isinstance(name, str) == False:
        return Response("name wrrong value", status=400, mimetype='application/json')

    menuName = request_data["menuName"]
    if len(menuName) == 0 or isinstance(menuName, str) == False:
        return Response("menuName wrrong value", status=400, mimetype='application/json')

    description = request_data["description"]
    if len(description) == 0 or isinstance(description, str) == False:
        return Response("description wrrong value", status=400, mimetype='application/json')

    price = request_data["price"]
    if price <=0 or isinstance(price, int) == False:
        return Response("price wrrong value", status=400, mimetype='application/json')

    timePreparation = request_data["timePreparation"]
    if timePreparation <= 0 or isinstance(timePreparation, int) == False:
        return Response("timePreparation wrrong value", status=400, mimetype='application/json')

    vegan = request_data["vegan"]
    if isinstance(vegan, bool) == False:
        return Response("vegan wrrong value", status=400, mimetype='application/json')

    err = Dish.update(id, name, menuName, description, price, timePreparation, vegan)
    if err is None:
        return Response("Dish updated", 201, mimetype='application/json')
    else:
        return Response("db error", 409, mimetype='application/json')

@app.route('/dish', methods=['GET'])
def listDish():
    menuName = request.headers['menu']
    if len(menuName) == 0 or isinstance(menuName, str) == False:
        return Response("menuName wrrong value", status=400, mimetype='application/json')

    dishName = request.headers['dish']
    if isinstance(dishName, str) == False:
        return Response("dishName wrrong value", status=400, mimetype='application/json')

    return jsonify({'menu': Dish.list(menuName, dishName)})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
