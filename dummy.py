from todo.models import db, User, Todo, List
import string
import random

def init():
    db.drop_all()
    db.create_all()
    emails = ['shalvinpshaji@gmail.com',
    'bednar.elfrieda@hotmail.com',
    'duncan.auer@hackett.biz',
    'dandre.cremin@hauck.com',
    'bailey.lenore@osinski.info',
    'ronny49@dach.com',
    'vfritsch@yahoo.com',
    'whitney.rosenbaum@gmail.com',
    'brooklyn38@yahoo.com',
    'nkrajcik@hotmail.com',
    'grant.carlee@legros.com']


    passwords = ['PEqMdZCX',
    'jk3swu8A',
    'BxqTQkff',
    'gmQwjpcU',
    'uEYyFVBF',
    'hfPTyjAk',
    '674C5p4D',
    'VLJPdLxM',
    'pgEvaXF5',
    'wSU5zbxU',
    'PkU6rF79']
    lists = [
        'Personal',
        'Work',
        'Internship',
        'Placement',
        'Projects',
        'Subject',
        'Projects',
        'Interviews',
        'Clubs',
        'ECA'
    ]
    for email, password in zip(emails, passwords):
        u = User(email=email, password=password)
        db.session.add(u)
    db.session.commit()
    for i in range(1, len(emails)+1):
        sample = random.sample(lists, 3)
        for s in sample:
            l = List(name=s, user_id=i)
            db.session.add(l)
    db.session.commit()

    for i in range(500):
        user_id = random.choice(range(1, 12))
        list_id = random.choice(range(1, len(lists)+1))
        todo = ''.join([random.choice(string.ascii_letters) for _ in range(15)])
        t = Todo(item=todo, user_id=user_id, list_id=list_id)
        db.session.add(t)
    db.session.commit()


if __name__ == "__main__":
    init()