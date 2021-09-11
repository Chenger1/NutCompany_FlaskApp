from flask import render_template, request, redirect, url_for
from werkzeug.datastructures import CombinedMultiDict

from . import main

from app.utils.mixins import AdminMethodView, AttrUndefined
from app.utils.funcs import handle_files
from app._db.models import User
from app.forms.admin.users import AdminEditForm, AdminCreateForm

from app import db

from datetime import date


class AdminUserList(AdminMethodView):
    def get(self):
        users = User.query.filter_by(is_admin=True).all()
        return render_template('admin/users/admin_users.html', instances=users)


class AdminDetail(AdminMethodView):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        form = AdminEditForm(obj=user)
        return render_template('admin/users/admin_detail.html', instance=user, form=form)

    def post(self, user_id):
        user = User.query.get_or_404(user_id)
        form = AdminEditForm(CombinedMultiDict((request.files, request.form)))
        if form.validate_on_submit():
            if form.photo.data:
                filename = handle_files(form.photo.data)
                user.photo = filename
            user.email = form.email.data
            user.fio = form.fio.data
            user.phone = form.phone.data
            user.password = form.password.data
            user.is_admin = form.is_admin.data
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.admin_list'))
        form.email.data = user.email
        form.fio.data = user.fio
        form.phone.data = user.phone
        form.is_admin.data = user.is_admin
        return render_template('admin/users/admin_detail.html', instance=user, form=form)


class CreateAdminView(AdminMethodView):
    undefined = AttrUndefined(name='instance')

    def get(self):
        form = AdminCreateForm()
        return render_template('admin/users/admin_detail.html', form=form, instance=self.undefined)

    def post(self):
        form = AdminEditForm(CombinedMultiDict((request.files, request.form)))
        if form.validate_on_submit():
            filename = handle_files(form.photo.data)
            user = User(email=form.email.data, fio=form.fio.data,
                        phone=form.phone.data, password=form.password.data,
                        is_admin=form.is_admin.data, photo=filename,
                        joined=date.today())
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.admin_list'))
        return render_template('admin/users/admin_detail.html', form=form, instance=self.undefined)


main.add_url_rule('/admin_list', view_func=AdminUserList.as_view('admin_list'))
main.add_url_rule('/admin_detail/<user_id>', view_func=AdminDetail.as_view('admin_detail'))
main.add_url_rule('/admin_detail/create_admin', view_func=CreateAdminView.as_view('create_admin'))
