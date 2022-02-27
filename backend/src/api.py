from flask import Flask, request, jsonify, abort
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this function will add one
'''
db_drop_and_create_all()

# ROUTES

'''
GET /healtz
    This route is for kubernetes readiness and liveness probes
'''
@app.route("/healthz")
def get_health():
    return jsonify({
        "success": True
    }), 200




'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks")
def get_drinks():

    try:

        drinks_query = Drink.query.all()
        drinks = [drink.short() for drink in drinks_query]
    
    except Exception as e:
        print(e)
        abort(422)


    return jsonify({
        "success": True,
        "drinks": drinks
    }), 200


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks-detail")
@requires_auth(permission='get:drinks-detail')
def get_drinks_detail(payload):

    try:

        drinks_query = Drink.query.order_by(Drink.id).all()
        drinks = [drink.long() for drink in drinks_query]
    
    except Exception as e:
        print(e)
        abort(422)


    return jsonify({
        "success": True,
        "drinks": drinks
    }), 200

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks", methods=["POST"])
@requires_auth(permission='post:drinks')
def post_drinks(payload):
    
    body = request.get_json()
    new_title = body.get("title", None)
    new_recipe = body.get("recipe", None)

    try:
        
        drink = Drink(title=new_title, recipe=json.dumps(new_recipe))
        drink.insert()
    
    except Exception as e:
        print(e)
        abort(422)


    return jsonify({
        "success": True,
        "drinks": drink.long()
    }), 200

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks/<id>", methods=["PATCH"])
@requires_auth(permission='patch:drinks')
def patch_drinks(payload, id):
    
    body = request.get_json()
    new_title = body.get("title", None)
    new_recipe = body.get("recipe", None)
    drink = Drink.query.filter(Drink.id == id).first_or_404()

    try:
        
        
        if new_title:
            drink.title = new_title
        if new_recipe:
            drink.recipe = json.dumps(new_recipe)
        drink.update()
    
    except Exception as e:
        print(e)
        abort(422)


    return jsonify({
        "success": True,
        "drinks": [drink.long()]
    }), 200

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks/<id>", methods=["DELETE"])
@requires_auth(permission='delete:drinks')
def delete_drinks(payload, id):

    drink = Drink.query.filter(Drink.id == id).first_or_404()
    try:    
        drink.delete()        
    
    except Exception as e:
        print(e)
        abort(422)


    return jsonify({
        "success": True,
        "drinks": drink.id
    }), 200

# Error Handling

@app.errorhandler(401)
def notfound(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Unauthorized"
    }), 401

@app.errorhandler(403)
def notfound(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "Forbidden"
    }), 403

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable"
    }), 422

@app.errorhandler(404)
def notfound(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Not Found"
    }), 404

@app.errorhandler(405)
def notfound(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "Method Not Allowed"
    }), 405

@app.errorhandler(AuthError)
def autherror(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error
    }), error.status_code


if __name__ == "__main__":
    app.debug = True
    app.run()
