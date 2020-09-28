from flask import Blueprint, flash, redirect, url_for, render_template, abort, request
from flask_login import login_required, current_user

from mypyblog import db
from mypyblog.models import Post
from mypyblog.postovi.forms import PostForma

postovi = Blueprint('postovi', __name__)

@postovi.route("/post/novi", methods=['GET', 'POST'])
@login_required
def novi_post():
    form = PostForma()
    if form.validate_on_submit():
        post = Post(naslov=form.naslov.data, sadrzaj=form.sadrzaj.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post je napravljen', 'success')
        return redirect(url_for('main.home'))
    return render_template("novi_post.html", title='Novi Post', legend='Azuriraj Post', form=form)


@postovi.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.naslov, post=post)

@postovi.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def azuriraj_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForma()
    if form.validate_on_submit():
        post.naslov = form.naslov.data
        post.sadrzaj = form.sadrzaj.data
        db.session.commit()
        flash('Vas post je uspesno azuriran!', 'success')
        return redirect(url_for('postovi.post', post_id=post.id))
    elif request.method == 'GET':
        form.naslov.data = post.naslov
        form.sadrzaj.data = post.sadrzaj
    return render_template('novi_post.html', title="Azuriraj Post", form=form, legend='Azuriraj Post')


@postovi.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def obrisi_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Uspesno obrisan post!', 'success')
    return redirect(url_for('main.home'))