from flask import Blueprint , render_template, request, url_for, g, flash
from werkzeug.utils import redirect
from Pybo import  db
from Pybo.models import Question,Answer
from datetime import datetime
from ..forms import QuestionForm,AnswerForm
from Pybo.views.auth_views import login_required

bp = Blueprint('question',__name__,url_prefix='/question')

@bp.route('/list/')
def qlist():
    page = request.args.get('page',type=int,default=1)
    question_lst = Question.query.order_by(Question.create_date.desc())
    question_lst = question_lst.paginate( page , per_page=10)

    print(question_lst.total)
    print(question_lst.per_page)
    print(question_lst.iter_pages)
    print(question_lst.prev_num)


    return render_template('question/question_list.html', question_list=question_lst)

@bp.route('/detail/<int:question_id>/')    #<자료형:변수명>
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html',question = question , form=form)

@bp.route('/create/' , methods=('GET','POST'))
@login_required
def create():
    form = QuestionForm()

    if request.method == "POST" and form.validate_on_submit():
        q = Question(subject=form.subject.data , content=form.content.data, create_date=datetime.now(),user=g.user)
        db.session.add(q)
        db.session.commit()
        return redirect(url_for('main.index'))


    return render_template('question/question_form.html',form=form)

@bp.route('/modify/<int:question_id>',methods=('GET','POST'))
@login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('수정 권한이 없습니다.')
        return redirect(url_for('question.detail',question_id=question_id))

    if request.method == 'POST':
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)
            question.modify_date = datetime.now()
            db.session.commit()
            return redirect(url_for('question.detail',question_id=question_id))
    else :
        form = QuestionForm(obj=question)

    return render_template('question/question_form.html',form=form)

@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('삭제권한이 없습니다.')
        return redirect(url_for('question.detail',question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question.qlist'))
