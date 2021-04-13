from Pybo import db

class Userinput(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    user_id = db.Column(db.String(10) , nullable=False) # 아이디를 10자로 제한
    content = db.Column(db.Text(),nullable=False)
    create_date = db.Column(db.DateTime(),nullable=False)

class Useroutput(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer , db.ForeignKey('user.id' , ondelete='CASCADE'))
    user = db.relationship('Userinput' , backref=db.backref('answer_set'))
    content = db.Column(db.Text(),nullable=False)
    create_date = db.Column(db.DateTime(),nullable=False)
