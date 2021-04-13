from flask import Blueprint , render_template , request,url_for
from Pybo import db
from Pybo.models import Question,Answer
from datetime import datetime
from werkzeug.utils import redirect
from ..forms import AnswerForm


bp = Blueprint('answer',__name__,url_prefix='/answer')

@bp.route('/create/<int:question_id>' , methods=('POST',))
def create(question_id):
    form =AnswerForm()
    question = Question.query.get_or_404(question_id)
    if form.validate_on_submit():
        content = request.form['content']
        answer = Answer(question=question, content=content,create_date=datetime.now())
        db.session.add(answer)
        db.session.commit()
        return  redirect(url_for('question.detail',question_id=question.id))

    return render_template('question.question_detail.html',question=question,form=form)