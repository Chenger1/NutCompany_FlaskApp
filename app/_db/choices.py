from enum import Enum


class SelectFieldEnum(Enum):
    """
    SelectField from WTForms requires additional preparing
    """
    @classmethod
    def choices(cls):
        """
        SelectField requires choices either dict or tuple with (value, key) format
        """
        return [(choice, choice.value) for choice in cls]

    @classmethod
    def coerce(cls, item):
        """
        SelectField requires function to represent chosen value as valid type
        """
        return cls(item) if not isinstance(item, cls) else item

    def __str__(self):
        return str(self.value)


class UserTypeChoice(SelectFieldEnum):
    legal_person = 'Юридическое лицо'
    physical_person = 'Физические лицо'


class DeliveryTypeChoice(SelectFieldEnum):
    new_mail = 'Новая почта (по Украине, оплата за счет Клиента)'
    courier = 'Куръер по Одесса'
    self_pickup = 'Самовывоз со склада'


class PaymentChoice(SelectFieldEnum):
    privat = 'LiqPay/Приват24'
    cashless = 'Безналичный расчет'
    cash = 'Наличными при получении (Наложенным платежом)'


class OrderStatusChoice(SelectFieldEnum):
    unpaid = 'Неоплачен'
    in_progress = 'В обработке'
    sent = 'Отправлен'
    done = 'Выполнен'


class RequestStatusChoice(SelectFieldEnum):
    in_progress = 'В обработке'
    closed = 'Отказано'
    done = 'Выполнен'


class CountryChoice(SelectFieldEnum):
    ua = 'Украина'
    pl = 'Польша'
    by = 'Беларусь'
