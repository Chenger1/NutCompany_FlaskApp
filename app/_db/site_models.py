from app import db


class MainPageGallery(db.Model):
    __tablename__ = 'main_page_gallery'

    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.String())
    url = db.Column(db.String())


class NewsItem(db.Model):
    __tablename__ = 'news_item'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    text = db.Column(db.Text())
    photo = db.Column(db.String())
    date = db.Column(db.DateTime())


class CorporateClients(db.Model):
    __tablename__ = 'corporate_clients'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text())
    photo = db.Column(db.String())


class Contacts(db.Model):
    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key=True)
    office_address = db.Column(db.String(100))
    manufacture = db.Column(db.String(100))
    main_phone = db.Column(db.String(30))
    add_phone = db.Column(db.String(30))
    telegram = db.Column(db.String(30))
    viber = db.Column(db.String(30))
    whats_up = db.Column(db.String(30))
    email = db.Column(db.String(100))
    map = db.Column(db.Text())


class AboutCompany(db.Model):
    __tablename__ = 'about_company'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text())
    images = db.relationship('AboutCompanyGallery', backref='entity')


class AboutCompanyGallery(db.Model):
    __tablename__ = 'about_company_gallery'

    id = db.Column(db.Integer, primary_key=True)
    entity = db.Column(db.Integer(), db.ForeignKey('about_company.id'))
    photo = db.Column(db.String())
