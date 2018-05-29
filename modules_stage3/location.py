import requests
import sqlite3
def get_category(location):
    def choices(location):
        url = 'https://maps.googleapis.com/maps/api/geocode/json'
        params = {
        'key': 'AIzaSyBkaSzW2TGlN6ZXwH_65N7Z5r5p3iS7UIE',
        'address': location,
        }
        r = requests.get(url, params=params)
        location = r.json()
        if location['results']:
            return (location['results'][0]['types'])
        return ['Other']

    conn = sqlite3.connect('categories.db')
    c = conn.cursor()
    category = None
    for element in choices(location):
        c.execute('SELECT * FROM categories WHERE name=?', (element,))
        a = c.fetchone()
        if a:
            category = a[1]
            break
    return category
