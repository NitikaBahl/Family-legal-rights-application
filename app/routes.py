from flask import render_template, request, redirect, url_for, flash
from app.forms import ConsultationForm
from app.models import Consultation, Article
from app import db
from app import app

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/learn-more')
def learn_more():
    return render_template('learn_more.html')

@app.route('/articles')
def articles():
    articles = Article.query.all()
    return render_template('articles.html', articles=articles)

@app.route('/consultation', methods=['GET', 'POST'])
def consultation():
    form = ConsultationForm()
    if form.validate_on_submit():
        new_consultation = Consultation(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            details=form.details.data
        )
        db.session.add(new_consultation)
        db.session.commit()
        flash('Your consultation request has been submitted!', 'success')
        return redirect(url_for('index'))
    return render_template('consultation.html', form=form)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    if query:
        results = Article.query.filter(Article.title.contains(query) | Article.content.contains(query)).all()
        return render_template('search_results.html', results=results, query=query)
    return render_template('search_results.html', results=[], query=query)