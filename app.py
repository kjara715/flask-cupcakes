"""Flask app for Cupcakes"""
from flask import Flask, request, redirect, render_template, jsonify
from models import db, connect_db, Cupcake
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False #change to false for now
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

db.create_all()

@app.route("/")
def cupcake_page():
    cupcakes=Cupcake.query.all()
    return render_template("list_cupcakes.html", cupcakes=cupcakes)


@app.route("/api/cupcakes")
def get_cupcakes():
    """Responds with json of all cupcakes"""
    cupcakes = Cupcake.query.all()
    serialized = [c.serialize_cupcake() for c in cupcakes]

    return jsonify(cupcakes=serialized)

@app.route("/api/cupcakes/<int:cup_id>")
def get_cupcake(cup_id):
    """Responds with json of a particular cupcake with id of cup_id"""
    cupcake=Cupcake.query.get_or_404(cup_id)
    serialized = cupcake.serialize_cupcake()

    return jsonify(cupcake=serialized)
 
@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """Creates a new cupcake, inserts into the db and responseds with the json details"""
    all_params=request.json["params"]
    new_cupcake=Cupcake(flavor=all_params["flavor"], size=all_params["size"], rating=all_params["rating"], image=all_params["image"])
    db.session.add(new_cupcake)
    db.session.commit()

    response_json= jsonify(cupcake=new_cupcake.serialize_cupcake())

    return(response_json, 201)

@app.route("/api/cupcakes/<int:cup_id>", methods=["PATCH"])
def edit_cupcake(cup_id):
    """Edits a cupcake with id of cup_id"""
    cupcake=Cupcake.query.get_or_404(cup_id)

    cupcake.flavor=request.json.get("flavor", cupcake.flavor)
    cupcake.size=request.json.get("size", cupcake.size)
    cupcake.rating=request.json.get("rating", cupcake.rating)
    cupcake.image=request.json.get("image", cupcake.image)

    db.session.commit()

    return jsonify(cupcake=cupcake.serialize_cupcake())

@app.route("/api/cupcakes/<int:cup_id>", methods=["DELETE"])
def delete_cupcake(cup_id):
    """Deletes a selected cupcake"""
    cupcake=Cupcake.query.get_or_404(cup_id)
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")