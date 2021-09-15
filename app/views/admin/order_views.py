from . import main

from app.utils.generic import ListViewMixin, UpdateViewMixin, DeleteInstanceMixin
from app.utils.mixins import AdminMethodView
from app._db.models import Order
from app.forms.admin.common import EditOrderForm


class OrdersListView(AdminMethodView, ListViewMixin):
    model = Order
    template_name = 'admin/orders/orders_list.html'


class EditOrderView(AdminMethodView, UpdateViewMixin):
    model = Order
    template_name = 'admin/orders/edit_order.html'
    form_class = EditOrderForm


class DeleteOrderView(AdminMethodView, DeleteInstanceMixin):
    model = Order
    redirect_url = 'main.orders_list'


main.add_url_rule('/admin/order/list', view_func=OrdersListView.as_view('orders_list'))
main.add_url_rule('/admin/order/detail/<obj_id>', view_func=EditOrderView.as_view('edit_order'))
main.add_url_rule('/admin/order/detail/<obj_id>/delete', view_func=DeleteOrderView.as_view('delete_order'))
