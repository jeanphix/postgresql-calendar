import os
from datetime import date, timedelta

from flask import (
    abort,
    Flask,
    render_template,
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    func,
    Interval,
)


app = Flask(__name__)
app.config.update(dict(
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
))


db = SQLAlchemy(app)
session = db.session


def get_calendar(month: date):
    return session.query(func.generate_series(
        func.date_trunc('week', month),
        func.cast(func.date_trunc(
            'week',
            month +
            func.cast('1 month', Interval()) -
            func.cast('2 day', Interval()) +
            func.cast('1 week', Interval())
        ) - func.cast('1 day', Interval()), db.Date),
        func.cast('1 day', Interval())
    ).label('day')).all()


@app.route('/')
@app.route('/<int:year>/<int:month>')
def calendar(year=None, month=None):
    today = date.today()

    if year is None:
        year = today.year
        month = today.month

    try:
        month = date(year, month, 1)

    except ValueError:
        return abort(404)

    days = get_calendar(month)

    return render_template(
        'calendar.html',
        month=month,
        days=days,
        today=today,
        previous=month - timedelta(days=1),
        next=month + timedelta(days=31),
    )
