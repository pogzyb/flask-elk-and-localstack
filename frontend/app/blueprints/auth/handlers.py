from app.blueprints.auth import auth


@auth.route('/register', methods=['GET', 'POST'])
def register():
    pass


@auth.route('/login', methods=['GET', 'POST'])
def login():
    pass


@auth.route('/logout', methods=['GET'])
def logout():
    pass