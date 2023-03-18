import os
from flask import Blueprint, Flask, current_app, render_template, flash, request, jsonify, redirect, send_from_directory, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
from PIL import Image, ImageDraw, ImageFont
import os
from werkzeug.utils import secure_filename

views = Blueprint('views', __name__)
app = Flask(__name__)
    
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@views.route('/', methods=['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')    

    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    
    return jsonify({})

@views.route('/canvas', methods=['GET','POST'])
@login_required
def canvas():
    if request.method == "GET":
        return render_template("canvas.html", user=current_user)
    if request.method == "POST":
        filename = request.form['save_fname']
        data = request.form['save_cdata']
        canvas_image = request.form['save_image']
        # new_cert = Certificate(projName=filename, data=data, canvas_image=canvas_image, user_id=current_user.id)
        # db.session.add(new_cert)
        # db.session.commit()
        flash('Project added!', category='success')
    
    return redirect(url_for('views.canvas'))

# @views.route('/watermark', methods=['GET','POST'])
# @login_required
# def watermark():
#     if request.method == 'POST':
#         file = request.files['image']
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             app.config['UPLOAD_FOLDER'] = 'website\Image'
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             img = Image.open(file).convert("RGBA")

#         txt = Image.new('RGBA', img.size, (255,255,255,0))

#         #Creating text and font object
#         text = 'Digital Watermarked'
#         font = ImageFont.truetype('arial.ttf', 82)

#         #Creating draw object
#         draw = ImageDraw.Draw(txt)

#         #Positioning Text
#         textwidth, textheight = draw.textsize(text,font)
#         width, height = img.size
#         x=width/2-textwidth/2
#         y=height-textheight-300

#         #Applying Text
#         draw.text((x,y), text, fill=(255,255,255,125), font=font)

#         #Saving the new image
#         watermarked = Image.alpha_composite(img,txt)
#         watermarked.save(r'website/Image/watermarked.png')
#         flash('Digital Watermark embedded!', category='success')   
    
#     return render_template("watermark.html", user=current_user)



@views.route('/watermark', methods=['GET','POST'])
@login_required
def watermark():
    if request.method =='POST':
        #Get the uploaded file from the form data
        file = request.files['image']

        #Save the file to a location on the server
        file.save(r'website/Image/watermarked.png')

    #Return a  response to the client
    return render_template("watermark.html", user=current_user)