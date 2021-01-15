from flask import Flask, render_template, request, flash, jsonify, send_from_directory, redirect, url_for
from base64 import b64encode
from models import db,MemeTemplate,MemeTag
from flask_sqlalchemy import Model
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://iobztsjapjlhkq:10af9d6965ef13dbca3b4aa2195f50788f0db49a1add8fb772a4d84181dc6104@ec2-54-163-47-62.compute-1.amazonaws.com:5432/d3fgd14rl7d0tk'
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

UPLOAD_FOLDER = '/memeTemplateUploads/'
ALLOWED_EXTENSIONS = {'jpg','jpeg','png'}
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER 
app.app_context().push()
db.init_app(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/search')
def search():
    if (request.args.get('search_query')):
        data = request.args.get('search_query').lower().strip()
        results = MemeTemplate.query.join(MemeTag,MemeTemplate.memeID == MemeTag.memeID) \
                    .filter( (MemeTemplate.dialogue_template_name.ilike('%'+data+'%')) | (MemeTemplate.movieName.ilike('%'+data+'%'))  | (MemeTag.meme_tag.ilike('%'+data+'%'))) \
                    .all()
    else:
        results=MemeTemplate.query.join(MemeTag,MemeTemplate.memeID == MemeTag.memeID).all()

    response=[]
    for result in results:
        filename=result.memeTemplateSavePathURI.split('/')[-1]
        
        response.append({"onClickURL": '/uploads/'+filename, \
                        "dialogue":result.dialogue_template_name, \
                        "movie_name":result.movieName, \
                        "tags":[tagName.meme_tag for tagName in result.tags]
                        })

    #print (response)
    return jsonify({"result":response})

@app.route('/search-suggestions')
def searchsuggestions():
    results = MemeTemplate.query.join(MemeTag,MemeTemplate.memeID == MemeTag.memeID).all()
    response=set()
    for result in results:
        response.add(result.dialogue_template_name)    
        response.add(result.movieName)  
        for tag in result.tags:
            response.add(tag.meme_tag)

        responseList=[x[0].upper()+x[1:] for x in response if x]
    return jsonify({"result":responseList})

@app.route('/uploads/<path:filename>')
def uploads(filename):
    return send_from_directory(UPLOAD_FOLDER,filename)

@app.route('/new-template')
def addNewTemplate():
    return render_template('new_template_entry.html')

@app.route('/new-template/processTemplateForm',methods=['POST'])
def processTemplateForm():
    if request.method == 'POST':
        templateImg = request.files.get('templateImg')
        fileExtension = templateImg.filename.split('.')[-1]
        dialogue_template_name = request.form['dialogue_template_name']
        template_image_name = dialogue_template_name.replace(' ','_').lower().strip() + '.' + fileExtension

        movieName = request.form['movieName'].strip()
        tagsList = request.form['tags'].split(',')

        memeTemplateSavePathURI=os.path.join(app.config['UPLOAD_FOLDER'],template_image_name)
        templateImg.save(memeTemplateSavePathURI)

        meme_record = MemeTemplate(memeTemplateSavePathURI, dialogue_template_name, movieName)
        db.session.add(meme_record)
        db.session.flush()
        
        for tag in tagsList:
            db.session.add(MemeTag(tag.lower().strip(),meme_record.memeID))
    
        db.session.commit()
        return redirect(url_for('index'))

if __name__=='__main__':
    db.create_all()
    app.run()