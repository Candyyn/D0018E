# How to start
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
