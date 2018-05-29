import time
from database import *
from photo import *

photo = 'lviv.jpg'
rc = Receipt(photo)
location = rc.location()
total = rc.total()
print(type(total))
category = rc.category()
db = Database('example.db')
db.new_fill(category, total)
db = Database('total.db')
db.new_entry([str(category), time.strftime("%d/%m/%Y"), location, total])
