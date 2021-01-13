from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class MemeTemplate(db.Model):
    __tablename__ = 'meme_template'
    memeID = db.Column(db.Integer, primary_key=True)
    memeTemplateImageString = db.Column(db.LargeBinary)
    dialogue_template_name = db.Column(db.String(200))
    movieName = db.Column(db.String(50))
    tags = db.relationship('MemeTags',backref='memetemplate',lazy=True)

    def __repr__ (self):
        return '<Meme %r>' % self.memeID

    def __init__(self,memeTemplateImageString,dialogue_template_name,movieName):
        self.memeTemplateImageString = memeTemplateImageString
        self.dialogue_template_name = dialogue_template_name
        self.movieName = movieName

class MemeTags(db.Model):
    __tablename__ = 'meme_tags'
    meme_tag_id = db.Column(db.Integer, primary_key=True)
    memeID = db.Column(db.Integer, db.ForeignKey('meme_template.memeID'))
    meme_tag = db.Column(db.String(50))

    def __repr__ (self):
        return '<Tag %r>' % self.meme_tag_id

    def __init__ (self,memetag):
        self.meme_tag=memetag