from flask import Blueprint , render_template,url_for
from Pybo import db
from Pybo.models import Question,Answer
from datetime import datetime
from werkzeug.utils import redirect


bp = Blueprint('main', __name__, url_prefix='/') #앞이 / 로 시작하면 블루프린트가 감시



@bp.route('/')
def index():

    return redirect(url_for('question.qlist')) # question 이라는 블루프린트에 qlist함수로 주소를 넘겨라



@bp.route('/test')
def test():
    for i in range(300):
        q = Question(subject='테스트 데이터입니다. {0}'.format(i) , content='내용무' , create_date=datetime.now())
        db.session.add(q)
    db.session.commit()
    return 'sucess'
