import unicodedata

def strip_accents(value):
   return ''.join(c for c in unicodedata.normalize('NFD', value)
                  if unicodedata.category(c) != 'Mn')
