from PIL import Image
from pytesseract import image_to_string
from location import get_category

class Receipt:
    def __init__(self, filename):
        self.data = image_to_string(Image.open(filename)).split('\n')
        #self.location = ''
        #self.total = ''

    def location(self):
        self.location = None
        for element in self.data:
            if 'магазин' in element or 'Магазин' in element or'МАГАЗИН'  in element:
                self.location = element
        return self.location

    def total(self):
        for element in self.data:
            if 'СУМА' in element or 'Сума' in element:
                temp = element.split()[1:]
                temp = float(''.join(temp).replace(',', '.'))
        return temp

    def category(self):
        return get_category(self.location)
