from app import db
from sqlalchemy.orm import backref


class MainPageGallery(db.Model):
    __tablename__ = 'main_page_gallery'

    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.String())
    url = db.Column(db.String(), nullable=True)
    text = db.Column(db.String(), nullable=True)


class NewsItem(db.Model):
    __tablename__ = 'news_item'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    text = db.Column(db.Text())
    photo = db.Column(db.String())
    publication_date = db.Column(db.DateTime())


class CorporateClients(db.Model):
    names = ('Крупные супермаркеты', 'Розничные магазины', 'Компании HoReCa',
             'Фитнес и спорт клубы', 'Кондитерские и пекарни')

    __tablename__ = 'corporate_clients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    text = db.Column(db.Text(), nullable=True)
    photo = db.Column(db.String(), nullable=True)


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


class AboutCompanyGallery(db.Model):
    __tablename__ = 'about_company_gallery'

    id = db.Column(db.Integer, primary_key=True)
    entity_id = db.Column(db.Integer(), db.ForeignKey('about_company.id'))
    entity = db.relationship(AboutCompany, backref=backref('gallery', cascade='all, delete-orphan'))
    photo = db.Column(db.String())
