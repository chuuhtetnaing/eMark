import io
from flask import Blueprint, Flask, render_template, flash, request, jsonify, redirect, url_for, Response, send_file
from flask_login import login_required, current_user
from .models import Note, Imge
from . import db
import json
from PIL import Image
import os
from werkzeug.utils import secure_filename

src="https://code.jquery.com/jquery-3.6.0.min.js"


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
        # new_cert = Project(projName=filename, data=data, canvas_image=canvas_image, user_id=current_user.id)
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



# @views.route('/watermark2', methods=['GET','POST'])
# @login_required
# def watermark():
#     if request.method =='POST':
#         #Get the uploaded file from the form data
#         file = request.files['image']
#         file2 = request.form.get('image')

#         #Save the file to a location on the server
#         file.save(r'website/static/watermarked.jpg')

#         new_image = Image(image=file2, id=current_user.id)
#         db.session.add(new_image)
#         db.session.commit()
#         flash('Image added!', category='success')    

    # #Return a  response to the client
    # return render_template("watermark.html", user=current_user)

@views.route('/watermark', methods=['GET','POST'])
@login_required
def watermark():
    if request.method =='POST':
        pic = request.files['image']

        if not pic:
                return "no pic uploaded", 404
        
        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        img = Imge(image=pic.read(), mimetype=mimetype, name=filename)
        check = Imge.query.filter_by(name=filename).first()
        if check:
            flash('Image already exist.', category='error')
        else: 
            db.session.add(img)
            db.session.commit()
            flash('Image has been uploaded!', category='success')

    return render_template("watermark.html", user=current_user)

@views.route('/get_image/<int:id>')
def get_img(id):
    img = Imge.query.filter_by(id=id).first()
    if not img:
        return flash('There are no image in the database.', category='error')
    
    return Response(img.image, mimetype=img.mimetype)