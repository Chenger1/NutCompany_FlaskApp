from . import main

from flask import request, jsonify

from app.utils.mixins import AdminMethodView
from app.utils.generic import ListViewMixin, UpdateViewMixin, CreateViewMixin, DeleteInstanceMixin
from app._db.models import User, OrderItem, Order
from app.forms.admin.users import AdminEditForm, AdminCreateForm, ClientAdminPageForm


class AdminUserList(AdminMethodView, ListViewMixin):
    model = User
    template_name = 'admin/users/admin_users.html'

    def get_queryset(self):
        query = self.model.query.filter_by(is_admin=True)
        return self.paginate(query)


class AdminDetail(AdminMethodView, UpdateViewMixin):
    model = User
    form_class = AdminEditForm
    template_name = 'admin/users/admin_detail.html'
    redirect_url = 'main.admin_list'


class CreateAdminView(AdminMethodView, CreateViewMixin):
    model = User
    form_class = AdminCreateForm
    template_name = 'admin/users/admin_detail.html'
    redirect_url = 'main.admin_list'


class DeleteAdminView(AdminMethodView, DeleteInstanceMixin):
    model = User
    redirect_url = 'main.admin_list'


class ClientUserList(AdminMethodView, ListViewMixin):
    model = User
    template_name = 'admin/users/client_users.html'

    def get_queryset(self):
        query = self.model.query.filter_by(is_admin=False)
        return self.paginate(query)


class ClientDetail(AdminMethodView, UpdateViewMixin):
    model = User
    form_class = ClientAdminPageForm
    template_name = 'admin/users/client_detail.html'
    redirect_url = 'main.client_list'

    def get_context(self, form, instance):
        context = super().get_context(form, instance)
        context['order_item_class'] = OrderItem
        return context


class DeleteClientView(AdminMethodView, DeleteInstanceMixin):
    model = User
    redirect_url = 'main.client_list'


class ListClientOrders(AdminMethodView):
    model = Order

    def get(self, obj_id):
        page = request.args.get('page', 1, type=int)
        instances = self.model.query.filter_by(user=obj_id)
        pagination = instances.paginate(
            page, per_page=10, error_out=False
        )
        return jsonify({
            'orders': self.serialize(pagination.items),
            'current_page': page,
            'total_pages': pagination.pages
        })

    def serialize(self, queryset):
        result = []
        for item in queryset:
            result.append({
                'id': item.id,
                'date': f'{item.date.strftime("%Y-%m-%d")} ?? {item.date.strftime("%H:%M")}',
                'amount': OrderItem.amount_for_order(item.id),
                'status': item.status.value,
                'sum': item.sum
            })
        return result


main.add_url_rule('/admin_list', view_func=AdminUserList.as_view('admin_list'))
main.add_url_rule('/admin_detail/<obj_id>', view_func=AdminDetail.as_view('admin_detail'))
main.add_url_rule('/admin_detail/create_admin', view_func=CreateAdminView.as_view('create_admin'))
main.add_url_rule('/admin_detail/<obj_id>/delete', view_func=DeleteAdminView.as_view('delete_admin'))


main.add_url_rule('/client/list', view_func=ClientUserList.as_view('client_list'))
main.add_url_rule('/client/detail/<obj_id>', view_func=ClientDetail.as_view('client_detail'))
main.add_url_rule('/client/detail/<obj_id>/delete', view_func=DeleteClientView.as_view('delete_client'))

main.add_url_rule('/client/detail/<obj_id>/orders_list', view_func=ListClientOrders.as_view('client_orders_list'),
                  methods=['GET'])
