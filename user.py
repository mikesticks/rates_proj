from werkzeug.security import safe_str_cmp


class User(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password


users = [
    User("testuser", "z1c3b5m7"),
]

users_table = {x.username: x for x in users}


def validate_credentials(username, password):
    """
    This function is used to verify the passed username and password are valid

    :param username: username string
    :param password: password string
    :return: a user object if it is found otherwise it doesn't return anything
    """
    user = users_table.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user
