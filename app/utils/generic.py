from flask import render_template, request


class ListViewMixin:
    model = None
    template_name = None
    paginate_by = 20

    def __init__(self):
        self.pagination = None

    def get_page(self):
        return request.args.get('page', 1, type=int)

    def get_queryset(self):
        query = self.model.query
        return self.paginate(query)

    def paginate(self, query):
        self.pagination = query.paginate(
            self.get_page(), per_page=self.paginate_by,
            error_out=False
        )
        return self.pagination.items

    def get_context(self):
        return {'instances': self.get_queryset(),
                'pagination': self.pagination}

    def render_template(self):
        context = self.get_context()
        return render_template(self.template_name, **context)

    def get(self):
        return self.render_template()
