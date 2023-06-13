"""Flask app for Cupcakes"""

from flask import Flask, jsonify, request, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake
# from forms import UpdateCupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'mr_pickles'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
app.app_context().push()


@app.route('/')
def home():
    """List all cupcakes and form"""
    return render_template('home.html')


@app.route('/api/cupcakes', methods=["GET", "POST"])
def all_cupcakes():
    """List all cupcakes or add a new one"""

    if request.method == "POST":
        flavor = request.json.get('flavor')
        size = request.json.get('size')
        rating = request.json.get('rating')
        image = request.json.get('image')

        if flavor and size and rating:
            new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
            db.session.add(new_cupcake)
            db.session.commit()

            response_json = jsonify(cupcake=new_cupcake.serialize())
            return (response_json, 201)
        else:
            return jsonify({"error": "Missing data"}), 400
    else:
        all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
        return jsonify(cupcakes=all_cupcakes)


@app.route('/api/cupcakes/<int:id>', methods=["GET", "PATCH", "DELETE"])
def cupcake(id):
    """Cupcake detail"""
    cupcake = Cupcake.query.get_or_404(id)

    if request.method == "PATCH":
        cupcake.flavor = request.json.get("flavor", cupcake.flavor)
        cupcake.size = request.json.get("size", cupcake.size)
        cupcake.rating = request.json("raitng", cupcake.rating)
        cupcake.image = request.json.get("image", cupcake.image)

        db.session.commit()
        return jsonify(cupcake=cupcake.serialize())
    elif request.method == "DELETE":
        db.session.delete(cupcake)
        db.session.commit()
        return jsonify(message=f"{cupcake.flavor} has been deleted")
    else:
        return jsonify(cupcake=cupcake.serialize())
