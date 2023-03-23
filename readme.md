# D0018E - Database Technology
This project is part of the course ’D0018E - Database Technology’ at Luleå University of Technology. The objective for this project was to approach an SQL database by building a small e-commerce site, which is accessed by standard web browser clients. The task was to set up and manage the database on a server and build a basic web frontend. An SQL database schema was to be established in the server to store the data handled by the web site.

## The Group

The student group consists of the following three members:

@SwirlyTrain - Henrik Eklund - henekl-0@student.ltu.se \
@peggykhialie - Peggy Khialie - pegkhi-0@student.ltu.se \
@Candyyn - Emil Magnusson - emimag-0@student.ltu.se

## How to start
- Clone the repo
- Run `pipip install -r requirements.txt`
- Run `python main`
- ...
- Profit


## Roles
- User
- Moderator
- Admin


## Permissions
- Create Product - 0x01000000
- edit Product - 0x01010000
- View Orders - 0x01110000
- edit Orders - 0x01000100
- View Users - 0x01100000
- edit Users - 0x01001000



AdminPerm = 0x01000000 | 0x01100000 | 0x01010000 | 0x01110000 = 0b1000100010000000000000000
