import bcrypt

password = 'password123'
hashed = '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWrn3ILAWO.iI.l2Bq.hGBw/G1B3Sy'

if bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8')):
    print("Match!")
else:
    print("No Match")
