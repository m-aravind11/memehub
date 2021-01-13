from flask import Flask, render_template, request, flash
from base64 import b64encode
from models import db,MemeTemplate,MemeTags

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SECRET_KEY'] = 'secret'

app.app_context().push()
db.init_app(app)

@app.route('/')
def index():
    return 'Hello'

@app.route('/new-template')
def addNewTemplate():
    return render_template('new_template_entry.html')

@app.route('/new-template/processTemplateForm',methods=['POST'])
def processTemplateForm():
    if request.method == 'POST':
        templateImg = request.files.get('templateImg')
        templateImg_string=b64encode(templateImg.read())
        dialogue_template_name = request.form['dialogue_template_name']
        movieName = request.form['movieName']
        tags = request.form['tags'].split(',')

        meme_record = MemeTemplate(templateImg_string, dialogue_template_name, movieName)
        db.session.add(meme_record)

        for tag in tags:
            db.session.add(MemeTags(tag.lower().strip()))
    
        db.session.commit()
        flash ('Record insertion successful!')
        return 'Submitted!'

if __name__=='__main__':
    app.run('127.0.0.1',port=5000,debug=True)