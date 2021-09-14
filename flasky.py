from app import create_app, db
from app._db.site_models import CorporateClients


app = create_app('development')


@app.before_first_request
def init_db():
    instances = CorporateClients.query.all()
    if instances:
        return
    for name in CorporateClients.names:
        db.session.add(CorporateClients(name=name))
    db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)
