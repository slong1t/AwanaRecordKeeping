#from django.test import TestCase

# Create your tests here.
from Awana.models import Section
from Awana.models import Chapter
from Awana.models import ClubBook

s = Section(number=1)
c = Chapter(number = 1, sections= s)
ttBook = ClubBook(book = 4, chapters=c)
