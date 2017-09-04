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
    roll = Clubber.objects.all().order_by('name')
    template = loader.get_template('AwanaRecordKeeping/index.html')
    context = {
        'night' : night,
        'roll' : roll,
        'wed' : next_wednesday()
    }

    return HttpResponse(template.render(context,request))


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
        
    club_roll = Clubber.objects.filter(club=club_enum).order_by('name')
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
        dues = request.POST.getlist("dues[]")
        print (dues[0])
        i = 0
        for c in club_roll:
            dues_pts[c.name] = dues[i]
            i += 1
        print (dues_pts)
        for child in attendance:
            c = Clubber.objects.get(name=child)
            c.dues = dues_pts[c.name]
            c.save()
            print (c.name + " dues " + str(c.dues))
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
            
    club_roll = Clubber.objects.filter(club=club_enum).order_by('name')
    
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

def PointsSparks(request):
    template = loader.get_template('AwanaRecordKeeping/PointsSparks.html')
    club_roll = Clubber.objects.filter(club='2').order_by('name')
    roll = {}
    for c in club_roll:
        roll[c.name] = True
    context = {        
            'roll' : roll,
        }
    return HttpResponse(template.render(context,request))

def PointsTTGirls(request):
    template = loader.get_template('AwanaRecordKeeping/PointsTTGirls.html')
    club_roll = Clubber.objects.filter(club='3').order_by('name')
    roll = {}
    for c in club_roll:
        roll[c.name] = True
    context = {        
            'roll' : roll,
        }
    return HttpResponse(template.render(context,request))

def PointsTTBoys(request):
    template = loader.get_template('AwanaRecordKeeping/PointsTTBoys.html')
    club_roll = Clubber.objects.filter(club='4').order_by('name')
    roll = {}
    for c in club_roll:
        roll[c.name] = True
    context = {        
            'roll' : roll,
        }
    return HttpResponse(template.render(context,request))

def AwardsSparks(request):
    template = loader.get_template('AwanaRecordKeeping/AwardsSparks.html')
    club_roll = Clubber.objects.filter(club='2').order_by('name')
    spark_chapter = {
            1 : 'Rank',
            2 : 'RJ1',
            3 : 'GJ1',
            4 : 'RJ2',
            5 : 'GJ2',
            6 : 'RJ3',
            7 : 'GJ3',
            8 : 'RJ4',
            9 : 'GJ4',
        }
    section = {}
    for c in club_roll:
        completed_sections = HandBookPoint.objects.filter(clubber=c,date=datetime.date.today())
        i = 0
        for cs in completed_sections:
            if cs.book == 0 and cs.section == 6:
                section[c.name + " (" + str(i) + ")"] = BOOK_TYPE_CHOICES[int(cs.book)][1] + ' : ' + spark_chapter[cs.chapter]
            elif cs.chapter == 1 and cs.section == 8:
                section[c.name + " (" + str(i) + ")"] = BOOK_TYPE_CHOICES[int(cs.book)][1] + ' : ' + spark_chapter[cs.chapter]
            elif cs.chapter > 1 and cs.section == 4:
                section[c.name + " (" + str(i) + ")"] = BOOK_TYPE_CHOICES[int(cs.book)][1] + ' : ' + spark_chapter[cs.chapter]
            i +=1
    context = {        
            'section' : section,
        }
    return HttpResponse(template.render(context,request))

def AwardsTT(request):
    template = loader.get_template('AwanaRecordKeeping/AwardsTT.html')
    tt_chapter = {
        '4' : 'SZ',
        '5' : 'Unit',
        '6' : 'Discovery',
        '7' : 'Discovery',
        '8' : 'Discovery',
        '9' : 'Discovery'
    }
    club_roll = Clubber.objects.filter(club='3').order_by('name')
    gsection = {}
    for c in club_roll:
        completed_sections = HandBookPoint.objects.filter(clubber=c,date=datetime.date.today())
        i = 0
        for cs in completed_sections:
            if cs.book == 4 and cs.section == 2: 
                gsection[c.name + " (" + str(i) + ")"] = BOOK_TYPE_CHOICES[int(cs.book)][1] + ' : ' + tt_chapter[str(cs.book)] + str(cs.chapter)
            elif cs.section == 8: 
                gsection[c.name + " (" + str(i) + ")"] = BOOK_TYPE_CHOICES[int(cs.book)][1] + ' : ' + tt_chapter[str(cs.book)] + str(cs.chapter)
            i += 1
            
    club_roll = Clubber.objects.filter(club='4').order_by('name')
    bsection = {}
    for c in club_roll:
        completed_sections = HandBookPoint.objects.filter(clubber=c,date=datetime.date.today())
        i = 0
        for cs in completed_sections:
            bsection[c.name + " :" + str(i)] = BOOK_TYPE_CHOICES[int(cs.book)][1] + ' : ' + tt_chapter[str(cs.book)] + str(cs.chapter) + " : " + str(cs.section) 
            i +=1

    context = {
            'gsection' : gsection,
            'bsection' : bsection,
        }
    return HttpResponse(template.render(context,request))

def HandBook(request, club_enum):
    club_roll = Clubber.objects.filter(club=club_enum).order_by('name')
    roll = {}
    hbook = {}
    hchap = {}
    hsec1 = {}
    hsec2 = {}
    hsec3 = {}
    hsec4 = {}
    hsec5 = {}
    hsec6 = {}
    hsec7 = {}
    hsec8 = {}
    for c in club_roll:
        roll[c.name] = True
        hbook[c.name] = BOOK_TYPE_CHOICES[int(c.current_book)][1]
        hchap[c.name] = c.current_chapter
        bookpts =  HandBookPoint.objects.filter(clubber=c, book=c.current_book, chapter=c.current_chapter)
        for pt in bookpts:
            if pt.section == 1:
                hsec1[c.name] = 1
            elif pt.section == 2:
                hsec2[c.name] = 1
            elif pt.section == 3:
                hsec3[c.name] = 1                
            elif pt.section == 4:
                hsec4[c.name] = 1                
            elif pt.section == 5:
                hsec5[c.name] = 1                
            elif pt.section == 6:
                hsec6[c.name] = 1                
            elif pt.section == 7:
                hsec7[c.name] = 1                
            elif pt.section == 8:
                hsec8[c.name] = 1                
        
    context = {
        'roll' : roll,
        'book' : hbook,
        'chapter' : hchap,
        'section1' : hsec1,
        'section2' : hsec2,
        'section3' : hsec3,
        'section4' : hsec4,
        'section5' : hsec5,
        'section6' : hsec6,
        'section7' : hsec7,
        'section8' : hsec8,
    }
    return context

def updateSection(_sectionList,_sectionNumber):
        sec = {}
        for clubber in _sectionList:
            if clubber in sec:
                sec[clubber] += 1
            else:
                sec[clubber] = 1
        #print(sec)
        for clubber in sec:
            db_sec = {}
            c = Clubber.objects.get(name=clubber)
            bookpts = HandBookPoint.objects.filter(clubber=c, book=c.current_book, chapter=c.current_chapter)
            for pt in bookpts:
                db_sec[pt.section] = 1
            #print (clubber + str(db_sec))
            if sec[clubber] == 1 and _sectionNumber in db_sec:
                #print(clubber + ":" + str(_sectionNumber) + " needs to be removed from db_sec")
                HandBookPoint.objects.filter(clubber=c, book=c.current_book, chapter=c.current_chapter, section=_sectionNumber).delete()
            elif sec[clubber] == 2 and not _sectionNumber in db_sec:
                #print(clubber + ":" + str(_sectionNumber) +  " needs to be added to db_sec")
                #hbp = HandBookPoint(clubber=c,book=c.current_book,chapter=c.current_chapter,section=_sectionNumber,date=next_wednesday())
                hbp = HandBookPoint(clubber=c,book=c.current_book,chapter=c.current_chapter,section=_sectionNumber,date=datetime.date.today())
                hbp.save()

def updateBook(_bookList):
    rtnVal = ''    
    for b in _bookList:
        child = b.split(',')
        c = Clubber.objects.get(name=child[0])
        if c.current_book != child[1]:
            c.current_book = child[1]
            c.current_chapter = 1
            c.save()
            rtnVal = child[0]
    return rtnVal

def updateChapter(_chapterList):
    rtnVal = ''
    for ch in _chapterList:
        child = ch.split(',')
        c = Clubber.objects.get(name=child[0])
        #print ("uc " + str(child[1]) + " " + c.name + " " + str(c.current_chapter))
        if c.current_chapter != int(child[1]):
            c.current_chapter = int(child[1])
            c.save()
            rtnVal = child[0]
    return rtnVal
        
def BookTTBoys(request):
    template = loader.get_template('AwanaRecordKeeping/BookTTBoys.html')
    #print(request.method)
    if request.method == 'POST':
        bookChanged = ''
        chapterChanged = ''        
        #print (request.POST)
        books = request.POST.getlist("ttbook")
        bookChanged = updateBook(books)      
        if bookChanged == '':
            chapters = request.POST.getlist("ttchap")
            chapterChanged = updateChapter(chapters)
            #print ('chapter changed ' + chapterChanged)            
            if chapterChanged == '':
                sec1 = request.POST.getlist('section1')
                updateSection(sec1,1)        
                sec2 = request.POST.getlist('section2')
                updateSection(sec2,2)        
                sec3 = request.POST.getlist('section3')
                updateSection(sec3,3)        
                sec4 = request.POST.getlist('section4')
                updateSection(sec4,4)        
                sec5 = request.POST.getlist('section5')
                updateSection(sec5,5)        
                sec6 = request.POST.getlist('section6')
                updateSection(sec6,6)        
                sec7 = request.POST.getlist('section7')
                updateSection(sec7,7)        
                sec8 = request.POST.getlist('section8')
                updateSection(sec8,8)                      

    context = HandBook(request,'4')
    return HttpResponse(template.render(context,request))
 
def BookTTGirls(request):
    template = loader.get_template('AwanaRecordKeeping/BookTTGirls.html')
    if request.method == 'POST':
        bookChanged = ''
        chapterChanged = ''        
        #print (request.POST)
        books = request.POST.getlist("ttbook")
        bookChanged = updateBook(books)      
        if bookChanged == '':
            chapters = request.POST.getlist("ttchap")
            chapterChanged = updateChapter(chapters)
            #print ('chapter changed ' + chapterChanged)            
            if chapterChanged == '':
                sec1 = request.POST.getlist('section1')
                updateSection(sec1,1)        
                sec2 = request.POST.getlist('section2')
                updateSection(sec2,2)        
                sec3 = request.POST.getlist('section3')
                updateSection(sec3,3)        
                sec4 = request.POST.getlist('section4')
                updateSection(sec4,4)        
                sec5 = request.POST.getlist('section5')
                updateSection(sec5,5)        
                sec6 = request.POST.getlist('section6')
                updateSection(sec6,6)        
                sec7 = request.POST.getlist('section7')
                updateSection(sec7,7)        
                sec8 = request.POST.getlist('section8')
                updateSection(sec8,8)                      
    
    context = HandBook(request,'3')
    return HttpResponse(template.render(context,request))

def BookSparks(request):
    template = loader.get_template('AwanaRecordKeeping/BookSparks.html')
    if request.method == 'POST':
        bookChanged = ''
        chapterChanged = ''        
        #print (request.POST)
        books = request.POST.getlist("sbook")
        bookChanged = updateBook(books)      
        if bookChanged == '':
            chapters = request.POST.getlist("schap")
            chapterChanged = updateChapter(chapters)
            #print ('chapter changed ' + chapterChanged)            
            if chapterChanged == '':
                sec1 = request.POST.getlist('section1')
                updateSection(sec1,1)        
                sec2 = request.POST.getlist('section2')
                updateSection(sec2,2)        
                sec3 = request.POST.getlist('section3')
                updateSection(sec3,3)        
                sec4 = request.POST.getlist('section4')
                updateSection(sec4,4)        
                sec5 = request.POST.getlist('section5')
                updateSection(sec5,5)        
                sec6 = request.POST.getlist('section6')
                updateSection(sec6,6)        
                sec7 = request.POST.getlist('section7')
                updateSection(sec7,7)        
                sec8 = request.POST.getlist('section8')
                updateSection(sec8,8)                      
    context = HandBook(request,'2')
    return HttpResponse(template.render(context,request))
