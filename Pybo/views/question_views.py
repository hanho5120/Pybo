from flask import Blueprint , render_template ,request, url_for
from werkzeug.utils import redirect
from Pybo import db
from Pybo.models import Question,Answer
from datetime import datetime
from ..forms import QuestionForm,AnswerForm

bp = Blueprint('question', __name__, url_prefix='/question') #앞이 / 로 시작하면 블루프린트가 감시

@bp.route('/list/')
def qlist():
    page = request.args.get('page',type=int,default=1)
    question_lst = Question.query.order_by(Question.create_date.desc())  # desc asc -->정렬
    question_lst = question_lst.paginate(page,per_page=10)
    return render_template('question/question_list.html', question_list=question_lst)



@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)

    return render_template('question/question_detail.html',question = question,form=form)

@bp.route('/create/', methods=('GET','POST'))
def create():
    form = QuestionForm()

    if request.method == "POST" and form.validate_on_submit():
        q = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now())
        db.session.add(q)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html',form=form)