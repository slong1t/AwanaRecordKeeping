from django.db import models

# Create your models here.
BOOK_TYPE_CHOICES = (
    ('0', 'Flight 3:16'),
    ('1', 'Sparks HangGlider'),
    ('2', 'Sparks WingRunner'),
    ('3', 'Sparks SkyStormer'),
    ('4', 'T&T Start Zone'),
    ('5', 'T&T Grace In Action'),
    ('6', 'T&T Adventure Book1'),
    ('7', 'T&T Adventure Book2'),
    ('8', 'T&T Challenge Book1'),
    ('9', 'T&T Challenge Book2'),
    ('10', 'Cubbie Appleseed'),
    ('11', 'Cubbie HoneyComb'),
    ('12', 'Puggle'),
    ('13', 'Sparks HangGlider Review'),
    ('14', 'Sparks WingRunner Review'),
    ('15', 'Sparks SkyStormer Review')
    
)

CLUBBER_TYPE_CHOICES = (
    ('0', 'Puggle'),
    ('1', 'Cubbie'),
    ('2', 'Spark'),
    ('3', 'TnT Girls'),
    ('4', 'TnT Boys'),
)

clubber_type = models.CharField(max_length=1, choices=CLUBBER_TYPE_CHOICES)
book_type = models.CharField(max_length=2, choices=BOOK_TYPE_CHOICES)
club_book_type = models.CharField(max_length=2, choices=BOOK_TYPE_CHOICES)

    
class Clubber (models.Model):
    name = models.CharField(max_length=30)
    club = clubber_type
    dues = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    current_book = book_type
    current_chapter = models.IntegerField(default = 0, null=True)
    current_section = models.IntegerField(default = 0, null=True)
    info_link = models.URLField(default = "/DefaultInfo.html")
    
    def __str__(self):
        return self.name + ":" + CLUBBER_TYPE_CHOICES[int(self.club)][1] 

class HandBookPoint (models.Model):
    clubber = models.ForeignKey(Clubber)
    book = models.CharField(max_length=2, choices=BOOK_TYPE_CHOICES, blank=True, null=True)
    chapter = models.IntegerField(null=True)
    section =  models.IntegerField(null=True)
    date = models.DateField(null=True)
    
    def __str__(self):
        return  str(self.clubber) + ' ' + BOOK_TYPE_CHOICES[int(self.book)][1] + ' ch-' + str(self.chapter) + ' sec-' + str(self.section) + ' ' + str(self.date)
    
class MeetingNight (models.Model):
    from datetime import date
    date = models.DateField(default=date.today)
    attendees = models.ManyToManyField (Clubber)
   
    def __str__(self):
        return str(self.date)
    
class ClubPoints (models.Model):
    bible = models.BooleanField(default=False)
    uniform = models.BooleanField(default=False)
    book = models.BooleanField(default=False)
    visitor = models.BooleanField(default=False)
    kid = models.ForeignKey(Clubber, null=True)
    night = models.ForeignKey(MeetingNight, null=True)
    version = models.IntegerField( default=0 )
    present = models.BooleanField(default=False)
    
        
    def __str__(self):
        return '%s %s %s %s %s %s %s %s' % (self.kid, self.night, 'book = ', self.book, 'uniform = ', self.uniform, 'bible = ', self.bible)

    

    