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


if __name__ == "__main__":
    app.run(port=5000, debug=True)
