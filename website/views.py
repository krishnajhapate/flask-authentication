from flask import Blueprint ,render_template ,request , flash ,jsonify
from flask_login import login_required,current_user
from .model import User , Note
from . import db
import json


views = Blueprint('views',__name__)

@views.route("/",methods=["GET","POST"])
@login_required
def home():
    if request.method == "POST":
        note = request.form['note']

        if len(note) < 8 :
            flash("Note should be greater then two words" ,category="error")

        else:
            note = Note(data=note,user_id=current_user.id)
            db.session.add(note)
            db.session.commit()

            flash("Note added ",category="success" )


    return render_template("home.html",user=current_user)

@views.route("/delete-note",methods=["POST"])
@login_required
def delete_note():
    note = json.loads(request.data)

    noteId= note['noteId']
    note = Note.query.get(noteId)

    if note: 
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            return jsonify({})
