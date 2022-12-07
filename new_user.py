from app import Session,User,engine

local_session=Session( bind=engine)
new_user=User( id=2,username='Akashk',email='kk@gmail.com',password='123456078')
local_session.add(new_user)
local_session.commit()

