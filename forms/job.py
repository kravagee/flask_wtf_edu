from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, DateField
from wtforms.validators import DataRequired


class AddJobForm(FlaskForm):
    teamleader = StringField('Имя тимлида', validators=[DataRequired()])
    job = StringField('Название работы', validators=[DataRequired()])
    work_size = IntegerField('Объем работы', validators=[DataRequired()])
    collaborators = StringField('Сотрудники выполняющие работу', validators=[DataRequired()])
    start_date = DateField('Дата начала', validators=[DataRequired()])
    end_date = DateField('Дата окончания', validators=[DataRequired()])