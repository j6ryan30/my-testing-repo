from app import app, db, User

def seed_users():
    with app.app_context():
        users_to_create = [
            ('ROwens03', 'ROwens03', 'admin'),
            ('J0spina02', 'J0spina02', 'admin'),
            ('EBarreno01', 'EBarreno01', 'admin'),
            ('KPeekSM', 'KPeekSM', 'admin'),
            ('CPowersQA', 'CPowersQA', 'admin'),
            ('FAlmasri01', 'FAlmasri01', 'user')
        ]

        for u, p, r in users_to_create:
            if not User.query.filter_by(username=u).first():
                new_user = User(username=u, role=r)
                new_user.set_password(p)
                db.session.add(new_user)

        db.session.commit()

        print("Users added successfully!")

        users = User.query.all()
        print("Current users:")
        for user in users:
            print(user.username)

if __name__ == "__main__":
    seed_users()