from flask import render_template

from . import main


@main.route('/admin')
def statistic():
    return render_template('admin/admin_base.html')
