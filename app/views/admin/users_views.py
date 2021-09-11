from flask import render_template

from . import main

from app.utils.mixins import AdminMethodView
from app._db.models import User
from app.forms.admin.users import AdminEditForm


class AdminUserList(AdminMethodView):
    def get(self):
        users = User.query.filter_by(is_admin=True).all()
        return render_template('admin/users/admin_users.html', instances=users)


class AdminDetail(AdminMethodView):
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        form = AdminEditForm(obj=user)
        return render_template('admin/users/admin_detail.html', instance=user, form=form)


main.add_url_rule('/admin_list', view_func=AdminUserList.as_view('admin_list'))
main.add_url_rule('/admin_detail/<user_id>', view_func=AdminDetail.as_view('admin_detail'))
