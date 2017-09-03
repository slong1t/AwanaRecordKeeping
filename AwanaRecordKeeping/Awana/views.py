#from django.shortcuts import render
#push to GitHub
# Create your views here.
from django.http import HttpResponse
from django.template import loader

from Awana.models import Clubber,MeetingNight,ClubPoints,HandBookPoint,BOOK_TYPE_CHOICES

import datetime
def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead < 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

def next_wednesday():
    d = datetime.date.today()
    return next_weekday(d, 2) # 0 = Monday, 1=Tuesday, 2=Wednesday...
    

def index(request):
    night = MeetingNight.objects.all()
    roll = Clubber.objects.all()
    points = ClubPoints.objects.all()
    #s = ''
    #for n in night:
    #    s += str(n)
    #    s += "\n"
    template = loader.get_template('AwanaRecordKeeping/index.html')
    context = {
        'night' : night,
        'roll' : roll,
        'points' : points,
        'wed' : next_wednesday()
    }

    return HttpResponse(template.render(context,request))
    #return HttpResponse('Hello')


from django.template.defaulttags import register
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def CheckIn(request, club_enum):
    try:
        n = MeetingNight.objects.get(date=next_wednesday())
    except MeetingNight.DoesNotExist:
        n = MeetingNight(date=next_wednesday())
        n.save()
        
    club_roll = Clubber.objects.filter(club=club_enum)
    present = {}
    uniform_pts = {}
    bible_pts = {}
    book_pts = {}
    visitor_pts = {}
    dues_pts = {}

    if request.method == "POST":
        attendance = request.POST.getlist("attend[]")
        uniform = request.POST.getlist("uniform[]")
        bible = request.POST.getlist("bible[]")
        book = request.POST.getlist("handbook[]")
        visitor = request.POST.getlist("visitor[]")
        print (visitor)
        dues = request.POST.getlist("dues[]")
        i = 0
        for c in club_roll:
            dues_pts[c.name] = dues[i]
            i += 1

        for child in attendance:
            c = Clubber.objects.get(name=child)
            c.dues = dues_pts[c.name]
            c.save()
            present[c.name] = True
            b = False
            u = False
            bk = False
            v = False
            if child in bible:
                b = True
            if child in uniform:
                u = True
            if child in book:
                bk = True
            if child in visitor:
                v = True
            try:
                p = ClubPoints.objects.get(kid=c,night=n)
                p.bible = b
                p.uniform = u
                p.book = bk
                p.visitor = v
                p.save()
            except ClubPoints.DoesNotExist:
                p1 = ClubPoints(bible=b,uniform=u,book=bk,visitor=v,kid=c,night=n)
                p1.save()
            n.attendees.add(c)
            n.save()
            
    club_roll = Clubber.objects.filter(club=club_enum)
    roll = {}
    for c in club_roll:
        roll[c.name] = True
        dues_pts[c.name] = c.dues                        
        try:
            p = ClubPoints.objects.get(kid=c,night=n)
            if request.method == "POST" and c.name not in present:
                p.delete()
                n.attendees.remove(c)
                n.save()
            else:
                present[c.name] = True
                if p.uniform:
                    uniform_pts[c.name] = True
                if p.book:
                    book_pts[c.name] = True
                if p.bible:
                    bible_pts[c.name] = True
                if p.visitor:
                    visitor_pts[c.name] = True

                
        except ClubPoints.DoesNotExist:
            #print ('could not find ' + c.name)
            pass
 
    context = {
        'night' : n,
        'roll' : roll,
        'present' : present,
        'bible' : bible_pts,
        'uniform' : uniform_pts,
        'handbook' : book_pts,
        'visitor' : visitor_pts,
        'dues' : dues_pts,
        'wed' : next_wednesday()
    }
    return context
    
def CheckInPuggles(request):
    template = loader.get_template('AwanaRecordKeeping/CheckInPuggles.html')
    context = CheckIn(request,'0')
    return HttpResponse(template.render(context,request))

def CheckInCubbies(request):
    template = loader.get_template('AwanaRecordKeeping/CheckInCubbies.html')
    context = CheckIn(request,'1')
    return HttpResponse(template.render(context,request))

def CheckInSparks(request):
    template = loader.get_template('AwanaRecordKeeping/CheckInSparks.html')
    context = CheckIn(request,'2')
    return HttpResponse(template.render(context,request))

def CheckInTTGirls(request):
    template = loader.get_template('AwanaRecordKeeping/CheckInTTGirls.html')
    context = CheckIn(request,'3')
    return HttpResponse(template.render(context,request))

def CheckInTTBoys(request):
    template = loader.get_template('AwanaRecordKeeping/CheckInTTBoys.html')
    context = CheckIn(request,'4')
    return HttpResponse(template.render(context,request))

def HandBook(request, club_enum):
    club_roll = Clubber.objects.filter(club=club_enum)
    roll = {}
    hbook = {}
    hchap = {}
    hsec = {}
    for c in club_roll:
        roll[c.name] = True
        hbook[c.name] = BOOK_TYPE_CHOICES[int(c.current_book)][1]
        hchap[c.name] = c.current_chapter
        hsec[c.name] = c.current_section
        
    context = {
        'roll' : roll,
        'book' : hbook,
        'chapter' : hchap,
        'section' : hsec,
    }
    return context

def BookTTBoys(request):
    template = loader.get_template('AwanaRecordKeeping/BookTTBoys.html')
    if request.method == 'POST':
        print (request.POST)
        books = {}
        books = request.POST.getlist("ttbook")
        for b in books:
            child = b.split(',')
            c = Clubber.objects.get(name=child[0])
            c.current_book = child[1]
            c.save()
        chaps = {}
        chaps = request.POST.getlist("ttchap")
        for ch in chaps:
            child = ch.split(',')
            c = Clubber.objects.get(name=child[0])
            c.current_chapter = child[1]
            c.save()
        sec1 = request.POST.get('section1')
        if sec1:
            print (sec1)
        sec2 = request.POST.get('section2')
        if sec2:
            print (sec2)
        sec3 = request.POST.get('section3')
        if sec3:
            print (sec3)
        sec4 = request.POST.get('section4')
        if sec4:
            print (sec4)
        sec5 = request.POST.get('section5')
        if sec5:
            print (sec5)
        sec6 = request.POST.get('section6')
        if sec6:
            print (sec6)
        sec7 = request.POST.get('section7')
        if sec7:
            print (sec7)
        sec8 = request.POST.get('section8')
        if sec8:
            print (sec8)
        
    context = HandBook(request,'4')
    return HttpResponse(template.render(context,request))
 
def BookTTGirls(request):
    template = loader.get_template('AwanaRecordKeeping/BookTTGirls.html')
    context = HandBook(request,'3')
    return HttpResponse(template.render(context,request))

def BookSparks(request):
    template = loader.get_template('AwanaRecordKeeping/BookSparks.html')
    context = HandBook(request,'2')
    return HttpResponse(template.render(context,request))
