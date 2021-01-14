from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class MemeTemplate(db.Model):
    __tablename__ = "memetemplate"
    memeID = db.Column(db.Integer, primary_key=True)
    memeTemplateSavePathURI = db.Column(db.String(500))
    dialogue_template_name = db.Column(db.String(200))
    movieName = db.Column(db.String(100))
    tags = db.relationship('MemeTag', backref='memetemplateID')
    def __repr__ (self):
        return '<Meme %r>' % self.memeID

    def __init__(self,memeTemplateSavePathURI,dialogue_template_name,movieName):
        self.memeTemplateSavePathURI = memeTemplateSavePathURI
        self.dialogue_template_name = dialogue_template_name
        self.movieName = movieName

class MemeTag(db.Model):
    __tablename__ = "memetag"
    meme_tag_id = db.Column(db.Integer, primary_key=True)
    meme_tag = db.Column(db.String(50))

    memeID = db.Column(db.Integer, db.ForeignKey('memetemplate.memeID'))
 
    def __repr__ (self):
        return '<Tag %r>' % self.meme_tag_id

    def __init__ (self,memetag,memeID):
        self.meme_tag=memetag
        self.memeID=memeID