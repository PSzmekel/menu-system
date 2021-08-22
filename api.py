from models import *
from flask import request, Response, jsonify




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


if __name__ == "__main__":
    app.run(port=5000, debug=True)
