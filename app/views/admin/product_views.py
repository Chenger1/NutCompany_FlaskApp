from . import main

from app.utils.mixins import AdminMethodView
from app.utils.generic import InlineFormsetMixin, ListViewMixin, DeleteInstanceMixin
from app._db.models import Product, ProductGallery

from app.forms.admin.common import CreateProductForm, EditProductForm, ProductGalleryForm
from app.forms.admin.formset import InlineFormset


class ListProductsView(AdminMethodView, ListViewMixin):
    template_name = 'admin/product/product_list.html'
    model = Product


class ProductView(AdminMethodView, InlineFormsetMixin):
    template_name = 'admin/product/edit_product.html'
    model = ProductGallery
    entity_model = Product
    redirect_url = 'main.products_list'
    formset_class = InlineFormset(form_class=ProductGalleryForm, model=ProductGallery)


class CreateProductView(ProductView):
    form_class = CreateProductForm

    def get_queryset(self):
        return ()


class EditProductView(ProductView):
    form_class = EditProductForm

    def get_queryset(self):
        return self.model.query.filter_by(entity=self.instance.id).all()


class DeleteProductView(AdminMethodView, DeleteInstanceMixin):
    model = Product
    redirect_url = 'main.products_list'


main.add_url_rule('/admin/products/list', view_func=ListProductsView.as_view('products_list'))
main.add_url_rule('/admin/products/create', view_func=CreateProductView.as_view('create_product'))
main.add_url_rule('/admin/products/edit/<obj_id>', view_func=EditProductView.as_view('edit_product'))
main.add_url_rule('/admin/products/delete/<obj_id>', view_func=DeleteProductView.as_view('delete_product'))
