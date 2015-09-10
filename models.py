
# __author__ = 'Eugene'

class User(object):
    def __init__(self, user_id, username, password, user_type, icon='/file/default_user.png', name='default', email='null',
                 identity_number='null', card_id='null'):
        super().__init__()
        self.user_id = user_id
        self.username = username
        self.password = password
        self.user_type = user_type
        self.icon = icon
        self.name = name
        self.email = email
        self.identity_number = identity_number
        self.card_id = card_id
