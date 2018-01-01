#from django.shortcuts import render
#push to GitHub
# Create your views here.
from django.http import HttpResponse
from django.template import loader
from Awana.models import Clubber,MeetingNight,ClubPoints,HandBookPoint,BOOK_TYPE_CHOICES
import datetime
import pytz
summer_start_night = datetime.date(2017, 9, 6)
christmas_store_night = datetime.date(2017, 12, 13)
winter_start_night = datetime.date(2018, 1, 10)

def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead < 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days=days_ahead)

def next_wednesday():
    d = datetime.datetime.now(pytz.timezone('US/Central'))
    return next_weekday(d.date(), 2) # 0 = Monday, 1=Tuesday, 2=Wednesday...
    

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
    version = {}
    info = {}

    if request.method == "POST":
        #print (request.POST)
        attendance = request.POST.getlist("attend[]")
        uniform = request.POST.getlist("uniform[]")
        bible = request.POST.getlist("bible[]")
        book = request.POST.getlist("handbook[]")
        visitor = request.POST.getlist("visitor[]")
        dues = request.POST.getlist("dues[]")
        ver = request.POST.getlist('version[]')
        i = 0
        for c in club_roll:
            dues_pts[c.name] = dues[i]
            version[c.name] = int(ver[i])
            i += 1
        #print (dues_pts)
        for child in attendance:
            c = Clubber.objects.get(name=child)
            c.dues = dues_pts[c.name]
            c.save()
            #print (c.name + " dues " + str(c.dues))
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
                #print (c.name + " " + str(version[c.name]) + " " + str(p.version))
                if version[c.name] == p.version and (p.bible != b or p.uniform != u or p.book != bk or p.visitor != v):
                    p.bible = b
                    p.uniform = u
                    p.book = bk
                    p.visitor = v
                    #print ("adding to version")
                    p.version += 1
                    p.save()
            except ClubPoints.DoesNotExist:
                p1 = ClubPoints(bible=b,uniform=u,book=bk,visitor=v,kid=c,night=n,version=1,present=True)
                p1.save()
            n.attendees.add(c)
            n.save()
            
    club_roll = Clubber.objects.filter(club=club_enum).order_by('name')
    
    roll = {}
    for c in club_roll:
        roll[c.name] = True
        dues_pts[c.name] = c.dues                        
        version[c.name] = 0
        info[c.name] = c.info_link
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
                version[c.name] = p.version

                
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
        'wed' : next_wednesday(),
        'info' : info,
        'version' : version
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
    attendance = {}
    bible = {}
    uniform = {}
    book = {}
    visitor = {}
    sections = {}
    total = {}
    for c in club_roll:
        start_date = summer_start_night
        club_points = ClubPoints.objects.filter(kid=c)
        book_points = HandBookPoint.objects.filter(clubber=c)
        try:
            MeetingNight.objects.get(attendees=c,date=christmas_store_night)
            start_date = winter_start_night
        except MeetingNight.DoesNotExist:
            pass

        club_points = ClubPoints.objects.filter(kid=c)
        book_points = HandBookPoint.objects.filter(clubber=c)
        attendance[c.name] = 0
        uniform[c.name] = 0
        book[c.name] = 0
        visitor[c.name] = 0
        sections[c.name] = 0
        bible[c.name] = 0
        for pt in club_points:
            if pt.night.date >= start_date:
                attendance[c.name] += 1
                if pt.bible:
                    bible[c.name] += 1
                if pt.uniform:
                    uniform[c.name] += 1
                if pt.book:
                    book[c.name] += 1
                if pt.visitor:
                    visitor[c.name] += 1 
        for pt in book_points:
            if pt.date >= start_date:
                sections[c.name] += 1
        if attendance[c.name] > 0:
            roll[c.name] = True
        total[c.name] = attendance[c.name] + uniform[c.name] + book[c.name] + visitor[c.name]*5 + sections[c.name]*2 + bible[c.name]
         
    context = {        
            'roll' : roll,
            'attendance' : attendance,
            'uniform' : uniform,
            'book' : book,
            'bible' : bible,
            'visitor' : visitor,
            'sections' : sections,
            'total' : total,
        }
    return HttpResponse(template.render(context,request))

def PointsTTGirls(request):
    template = loader.get_template('AwanaRecordKeeping/PointsTTGirls.html')
    club_roll = Clubber.objects.filter(club='3').order_by('name')
    roll = {}
    attendance = {}
    bible = {}
    uniform = {}
    book = {}
    visitor = {}
    sections = {}
    total = {}
    for c in club_roll:
        start_date = summer_start_night
        club_points = ClubPoints.objects.filter(kid=c)
        book_points = HandBookPoint.objects.filter(clubber=c)
        try:
            MeetingNight.objects.get(attendees=c,date=christmas_store_night)
            start_date = winter_start_night
        except MeetingNight.DoesNotExist:
            pass

        club_points = ClubPoints.objects.filter(kid=c)
        book_points = HandBookPoint.objects.filter(clubber=c)
        attendance[c.name] = 0
        uniform[c.name] = 0
        book[c.name] = 0
        visitor[c.name] = 0
        sections[c.name] = 0
        bible[c.name] = 0
        for pt in club_points:
            if pt.night.date >= start_date:
                attendance[c.name] += 1
                if pt.bible:
                    bible[c.name] += 1
                if pt.uniform:
                    uniform[c.name] += 1
                if pt.book:
                    book[c.name] += 1
                if pt.visitor:
                    visitor[c.name] += 1 
        for pt in book_points:
            if pt.date >= start_date:
                sections[c.name] += 1
   
        if attendance[c.name] > 0:
            roll[c.name] = True
        if c.current_book == '5':
            total[c.name] = attendance[c.name] + uniform[c.name] + book[c.name] + visitor[c.name]*5 + sections[c.name]*4 + bible[c.name]
        else:
            total[c.name] = attendance[c.name] + uniform[c.name] + book[c.name] + visitor[c.name]*5 + sections[c.name]*2 + bible[c.name]
         
    context = {        
            'roll' : roll,
            'attendance' : attendance,
            'uniform' : uniform,
            'book' : book,
            'bible' : bible,
            'visitor' : visitor,
            'sections' : sections,
            'total' : total,
        }
    return HttpResponse(template.render(context,request))

def PointsTTBoys(request):
    template = loader.get_template('AwanaRecordKeeping/PointsTTBoys.html')
    club_roll = Clubber.objects.filter(club='4').order_by('name')
    roll = {}
    attendance = {}
    bible = {}
    uniform = {}
    book = {}
    visitor = {}
    sections = {}
    total = {}
    for c in club_roll:
        start_date = summer_start_night
        club_points = ClubPoints.objects.filter(kid=c)
        book_points = HandBookPoint.objects.filter(clubber=c)
        try:
            MeetingNight.objects.get(attendees=c,date=christmas_store_night)
            start_date = winter_start_night
        except MeetingNight.DoesNotExist:
            pass
            
        attendance[c.name] = 0
        uniform[c.name] = 0
        book[c.name] = 0
        visitor[c.name] = 0
        sections[c.name] = 0
        bible[c.name] = 0
        for pt in club_points:
            if pt.night.date >= start_date:
                attendance[c.name] += 1
                if pt.bible:
                    bible[c.name] += 1
                if pt.uniform:
                    uniform[c.name] += 1
                if pt.book:
                    book[c.name] += 1
                if pt.visitor:
                    visitor[c.name] += 1 
        for pt in book_points:
            if pt.date >= start_date:
                sections[c.name] += 1
        if attendance[c.name] > 0:
            roll[c.name] = True
        if c.current_book == '5':
            total[c.name] = attendance[c.name] + uniform[c.name] + book[c.name] + visitor[c.name]*5 + sections[c.name]*4 + bible[c.name]
        else:
            total[c.name] = attendance[c.name] + uniform[c.name] + book[c.name] + visitor[c.name]*5 + sections[c.name]*2 + bible[c.name]
                
    context = {        
            'roll' : roll,
            'attendance' : attendance,
            'uniform' : uniform,
            'book' : book,
            'bible' : bible,
            'visitor' : visitor,
            'sections' : sections,
            'total' : total,
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
        now = datetime.datetime.now(pytz.timezone('US/Central'))
        completed_sections = HandBookPoint.objects.filter(clubber=c,date=now.date())
        i = 0
        prev_chap = ''
        for cs in completed_sections:
            if cs.book == '0' and cs.section == 6:
                section[c.name + " (" + str(i) + ")"] = BOOK_TYPE_CHOICES[int(cs.book)][1] + ' : ' + spark_chapter[cs.chapter]
            elif cs.chapter == 1 and prev_chap != cs.chapter:
                prev_chap = cs.chapter
                chapter_sections = HandBookPoint.objects.filter(clubber=c,book=cs.book,chapter=cs.chapter)
                #print (len(chapter_sections),chapter_sections)
                if len(chapter_sections) == 8:
                    section[c.name + " (" + str(i) + ")"] = BOOK_TYPE_CHOICES[int(cs.book)][1] + ' : ' + spark_chapter[cs.chapter]
            elif prev_chap != cs.chapter:
                chapter_sections = HandBookPoint.objects.filter(clubber=c,book=cs.book,chapter=cs.chapter)
                if len(chapter_sections) == 4:
                    section[c.name + " (" + str(i) + ")"] = BOOK_TYPE_CHOICES[int(cs.book)][1] + ' : ' + spark_chapter[cs.chapter]
                prev_chap = cs.chapter
            i += 1
    context = {        
            'section' : section,
        }
    return HttpResponse(template.render(context,request))

def AwardsTT(request):
    
    # 1) need to only give award if all sections have been completed
    # 2) when all sections have been completed automatically move to the next chapter 
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
        now = datetime.datetime.now(pytz.timezone('US/Central'))
        completed_sections = HandBookPoint.objects.filter(clubber=c,date=now.date())
        #print (c.name, ' completed sections: ', completed_sections)
        i = 0
        prev_chap = ''
        for cs in completed_sections:
            if cs.book == '4' and cs.section == 2: 
                gsection[c.name + " (" + str(i) + ")"] = BOOK_TYPE_CHOICES[int(cs.book)][1] + ' : ' + tt_chapter[str(cs.book)] + str(cs.chapter)
            elif cs.book == '5' and cs.chapter == 5 and prev_chap != cs.chapter:
                chapter_sections = HandBookPoint.objects.filter(clubber=c,book=cs.book,chapter=cs.chapter)
                if len(chapter_sections) == 10:
                    gsection[c.name + " (" + str(i) + ")"] = BOOK_TYPE_CHOICES[int(cs.book)][1] + ' : ' + tt_chapter[str(cs.book)] + str(cs.chapter)
                    prev_chap = cs.chapter
            elif cs.book == '5' and int(cs.chapter) > 5 and prev_chap != cs.chapter:
                chapter_sections = HandBookPoint.objects.filter(clubber=c,book=cs.book,chapter=cs.chapter)              
                if len(chapter_sections) == 12:
                    gsection[c.name + " (" + str(i) + ")"] = BOOK_TYPE_CHOICES[int(cs.book)][1] + ' : ' + tt_chapter[str(cs.book)] + str(cs.chapter)
                    prev_chap = cs.chapter
            elif prev_chap != cs.chapter: 
                chapter_sections = HandBookPoint.objects.filter(clubber=c,book=cs.book,chapter=cs.chapter)
                if len(chapter_sections) == 7:
                    gsection[c.name + " (" + str(i) + ")"] = BOOK_TYPE_CHOICES[int(cs.book)][1] + ' : ' + tt_chapter[str(cs.book)] + str(cs.chapter)
                prev_chap = cs.chapter
            i += 1
            
    club_roll = Clubber.objects.filter(club='4').order_by('name')
    bsection = {}
    for c in club_roll:
        now = datetime.datetime.now(pytz.timezone('US/Central'))
        completed_sections = HandBookPoint.objects.filter(clubber=c,date=now.date())
        i = 0
        prev_chap = ''
        for cs in completed_sections:                
            if cs.book == '4' and cs.section == 2: 
                gsection[c.name + " (" + str(i) + ")"] = BOOK_TYPE_CHOICES[int(cs.book)][1] + ' : ' + tt_chapter[str(cs.book)] + str(cs.chapter)
            elif cs.book == '5' and cs.chapter == 5 and prev_chap != cs.chapter:
                chapter_sections = HandBookPoint.objects.filter(clubber=c,book=cs.book,chapter=cs.chapter)
                if len(chapter_sections) == 10:
                    gsection[c.name + " (" + str(i) + ")"] = BOOK_TYPE_CHOICES[int(cs.book)][1] + ' : ' + tt_chapter[str(cs.book)] + str(cs.chapter)
                    prev_chap = cs.chapter
            elif cs.book == '5' and int(cs.chapter) > 5 and prev_chap != cs.chapter:
                chapter_sections = HandBookPoint.objects.filter(clubber=c,book=cs.book,chapter=cs.chapter)              
                if len(chapter_sections) == 12:
                    gsection[c.name + " (" + str(i) + ")"] = BOOK_TYPE_CHOICES[int(cs.book)][1] + ' : ' + tt_chapter[str(cs.book)] + str(cs.chapter)
                    prev_chap = cs.chapter
            elif prev_chap != cs.chapter: 
                chapter_sections = HandBookPoint.objects.filter(clubber=c,book=cs.book,chapter=cs.chapter)
                if len(chapter_sections) == 7:
                    gsection[c.name + " (" + str(i) + ")"] = BOOK_TYPE_CHOICES[int(cs.book)][1] + ' : ' + tt_chapter[str(cs.book)] + str(cs.chapter)
                prev_chap = cs.chapter
            i += 1

    #print (bsection)
    context = {
            'gsection' : gsection,
            'bsection' : bsection,
        }
    return HttpResponse(template.render(context,request))

def HandBook(request, club_enum, leader, group, msg):
    #print ("leader ", leader, " group ", group)
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
    hsec9 = {}
    hsec10 = {}
    hsec11 = {}
    hsec12 = {}
    leadername = leader
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
            elif pt.section == 9:
                hsec9[c.name] = 1                
            elif pt.section == 10:
                hsec10[c.name] = 1                
            elif pt.section == 11:
                hsec11[c.name] = 1                
            elif pt.section == 12:
                hsec12[c.name] = 1                
        
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
        'section9' : hsec9,
        'section10' : hsec10,
        'section11' : hsec11,
        'section12' : hsec12,
        'wed' : next_wednesday(),
        'lname' : leadername,
        'group' : group,
        'msg' : msg,
    }
    return context

def updateSection(_sectionList,_sectionNumber, _group):
        rtn_val = ''
        sec = {}
        for clubber in _sectionList:
            if clubber in sec:
                sec[clubber] += 1
            else:
                sec[clubber] = 1
        #print ('here ' + str(_sectionNumber))
        #print(sec)
        for clubber in sec:
            db_sec = {}
            c = Clubber.objects.get(name=clubber)
            bookpts = HandBookPoint.objects.filter(clubber=c, book=c.current_book, chapter=c.current_chapter)
            for pt in bookpts:
                db_sec[pt.section] = 1
            #print (clubber + str(db_sec))
            if sec[clubber] == 1 and _sectionNumber in db_sec and clubber in _group:
                #print(clubber + ":" + str(_sectionNumber) + " needs to be removed from db_sec")
                HandBookPoint.objects.filter(clubber=c, book=c.current_book, chapter=c.current_chapter, section=_sectionNumber).delete()
            elif sec[clubber] == 2 and not _sectionNumber in db_sec and clubber in _group:
                #print(clubber + ":" + str(_sectionNumber) +  " needs to be added to db_sec")
                #hbp = HandBookPoint(clubber=c,book=c.current_book,chapter=c.current_chapter,section=_sectionNumber,date=next_wednesday())
                ptDate = datetime.datetime.now(pytz.timezone('US/Central'))
                hbp = HandBookPoint(clubber=c,book=c.current_book,chapter=c.current_chapter,section=_sectionNumber,date=ptDate.date())
                hbp.save()
            elif (sec[clubber] == 1 and _sectionNumber in db_sec) or (sec[clubber] == 2 and not _sectionNumber in db_sec):
                rtn_val = clubber
        return rtn_val

def updateBook(_bookList, _group):
    rtnVal = ''    
    for b in _bookList:
        child = b.split(',')
        c = Clubber.objects.get(name=child[0])
        if c.current_book != child[1] and child[0] in _group:
            c.current_book = child[1]
            c.current_chapter = 1
            c.save()
            rtnVal = child[0]
        elif c.current_book != child[1]:
            rtnVal = child[0]
    return rtnVal

def updateChapter(_chapterList, _group):
    rtnVal = ''
    for ch in _chapterList:
        child = ch.split(',')
        c = Clubber.objects.get(name=child[0])
        #print ("uc " + str(child[1]) + " " + c.name + " " + str(c.current_chapter))
        if c.current_chapter != int(child[1]) and child[0] in _group:
            c.current_chapter = int(child[1])
            c.save()
            rtnVal = child[0]
        elif c.current_chapter != int(child[1]):
            rtnVal = child[0]
    return rtnVal

def AdvanceSectionIfNeededTT(_bookList):        
    for b in _bookList:
        child = b.split(',')
        c = Clubber.objects.get(name=child[0])
        chapter_sections = HandBookPoint.objects.filter(clubber=c,book=c.current_book,chapter=c.current_chapter)
        #print ('a',chapter_sections)
        #print (c.name,' club:',c.club,' book:',c.current_book,' chap:',c.current_chapter,' secs:',len(chapter_sections))
        if c.club == '3' or c.club == '4':
            #print ('club ', c.club)
            # start zone
            if c.current_book == '4':
                if len(chapter_sections) == 2:
                    # 'T&T Grace In Action'
                    c.current_book = 5
                    c.current_chapter = 1
                    c.current_section = 1
                    c.save()
            # T&T Grace In Action
            elif c.current_book == '5':
                #print (c.name, ' current_chapter: ', c.current_chapter, ' sections: ', len(chapter_sections))
                if int(c.current_chapter) < 5:  
                    if len(chapter_sections) == 7:
                        c.current_chapter = c.current_chapter + 1
                        c.current_section = 1
                        c.save()
                elif int(c.current_chapter) == 5:
                    if len(chapter_sections) == 10:
                        c.current_chapter = c.current_chapter + 1
                        c.current_section = 1
                        c.save()
                else:
                    if len(chapter_sections) == 12:
                        c.current_chapter = c.current_chapter + 1
                        c.current_section = 1
                        c.save()
            # Legacy Books
            else:
                #print ('leg current_chapter: ', c.current_chapter, ' sections: ', len(chapter_sections))
                if c.current_chapter < 8:  
                    if len(chapter_sections) == 7:
                        c.current_chapter = c.current_chapter + 1
                        c.current_section = 1
                        c.save()
                
def AdvanceSectionIfNeededSpark(_bookList):        
    for b in _bookList:
        child = b.split(',')
        c = Clubber.objects.get(name=child[0])
        chapter_sections = HandBookPoint.objects.filter(clubber=c,book=c.current_book,chapter=c.current_chapter)
        #print ('a',chapter_sections)
        #print (c.name,' club:',c.club,' book:',c.current_book,' chap:',c.current_chapter,' secs:',len(chapter_sections))
        # Flight 3:16
        if c.current_book == '0':
            if len(chapter_sections) == 6:
                c.current_book = 1
                c.current_chapter = 1
                c.current_section = 1
                c.save()
        else:
            #print ('leg current_chapter: ', c.current_chapter, ' sections: ', len(chapter_sections))
            if c.current_chapter == 1:  
                if len(chapter_sections) == 8:
                    c.current_chapter = c.current_chapter + 1
                    c.current_section = 1
                    c.save()
            else:  
                if len(chapter_sections) == 4:
                    c.current_chapter = c.current_chapter + 1
                    c.current_section = 1
                    c.save()

def BookTTBoys(request):
    template = loader.get_template('AwanaRecordKeeping/BookTTBoys.html')
    #print(request.method)
    leader_name = ''
    leaders_group = {}
    error_msg = ''
    if request.method == 'POST':
        #print (request.POST)
        leader = request.POST.getlist("leadername")
        leaders_group = request.POST.getlist("leader")
        leader_name = leader[0]
        if len(leaders_group) > 0:
            bookChanged = ''
            chapterChanged = '' 
            books = request.POST.getlist("ttbook")
            bookChanged = updateBook(books,leaders_group)      
            if bookChanged == '':
                chapters = request.POST.getlist("ttchap")
                chapterChanged = updateChapter(chapters,leaders_group)
                #print ('chapter changed ' + chapterChanged)            
                if chapterChanged == '':
                    sec1 = request.POST.getlist('section1')
                    section1 = updateSection(sec1,1,leaders_group)        
                    sec2 = request.POST.getlist('section2')
                    section2 = updateSection(sec2,2,leaders_group)        
                    sec3 = request.POST.getlist('section3')
                    section3 = updateSection(sec3,3,leaders_group)        
                    sec4 = request.POST.getlist('section4')
                    section4 = updateSection(sec4,4,leaders_group)        
                    sec5 = request.POST.getlist('section5')
                    section5 = updateSection(sec5,5,leaders_group)        
                    sec6 = request.POST.getlist('section6')
                    section6 = updateSection(sec6,6,leaders_group)        
                    sec7 = request.POST.getlist('section7')
                    section7 = updateSection(sec7,7,leaders_group)
                    sec8 = request.POST.getlist('section8')
                    section8 = updateSection(sec8,8,leaders_group)
                    sec9 = request.POST.getlist('section9')
                    section9 = updateSection(sec9,9,leaders_group)
                    sec10 = request.POST.getlist('section10')
                    section10 = updateSection(sec10,10,leaders_group)
                    sec11 = request.POST.getlist('section11')
                    section11 = updateSection(sec11,11,leaders_group)
                    sec12 = request.POST.getlist('section12')
                    section12 = updateSection(sec12,12,leaders_group)
                    if section1 != '' or section2 != '' or section3 != '' or section4 != '' or section5 != '' or section6 != '' or section7 != '' or section8 != '' or section9 != '' or section10 != '' or section11 != '' or section12 != '':
                        error_msg = 'Select clubber(s) to \'E\'dit in first column to make changes.'
                    else:
                        AdvanceSectionIfNeededTT(books)                                 
                elif chapterChanged not in leaders_group:   
                    error_msg = 'Select clubber(s) to \'E\'dit in first column to make changes.'                                 
            elif bookChanged not in leaders_group:   
                error_msg = 'Select clubber(s) to \'E\'dit in first column to make changes.'                                 
        else:
            error_msg = 'Select clubber(s) to \'E\'dit in first column to make changes.'
    context = HandBook(request,'4', leader_name, leaders_group, error_msg)
    return HttpResponse(template.render(context,request))
 
def BookTTGirls(request):
    template = loader.get_template('AwanaRecordKeeping/BookTTGirls.html')
    leader_name = ''
    leaders_group = {}
    error_msg = ''
    if request.method == 'POST':
        #print (request.POST)
        leader = request.POST.getlist("leadername")
        leaders_group = request.POST.getlist("leader")
        leader_name = leader[0]
        if len(leaders_group) > 0:
            bookChanged = ''
            chapterChanged = '' 
            books = request.POST.getlist("ttbook")
            bookChanged = updateBook(books,leaders_group)      
            if bookChanged == '':
                chapters = request.POST.getlist("ttchap")
                chapterChanged = updateChapter(chapters,leaders_group)
                #print ('chapter changed ' + chapterChanged)            
                if chapterChanged == '':
                    sec1 = request.POST.getlist('section1')
                    section1 = updateSection(sec1,1,leaders_group)        
                    sec2 = request.POST.getlist('section2')
                    section2 = updateSection(sec2,2,leaders_group)        
                    sec3 = request.POST.getlist('section3')
                    section3 = updateSection(sec3,3,leaders_group)        
                    sec4 = request.POST.getlist('section4')
                    section4 = updateSection(sec4,4,leaders_group)        
                    sec5 = request.POST.getlist('section5')
                    section5 = updateSection(sec5,5,leaders_group)        
                    sec6 = request.POST.getlist('section6')
                    section6 = updateSection(sec6,6,leaders_group)        
                    sec7 = request.POST.getlist('section7')
                    section7 = updateSection(sec7,7,leaders_group)
                    sec8 = request.POST.getlist('section8')
                    section8 = updateSection(sec8,8,leaders_group)
                    sec9 = request.POST.getlist('section9')
                    section9 = updateSection(sec9,9,leaders_group)
                    sec10 = request.POST.getlist('section10')
                    section10 = updateSection(sec10,10,leaders_group)
                    sec11 = request.POST.getlist('section11')
                    section11 = updateSection(sec11,11,leaders_group)
                    sec12 = request.POST.getlist('section12')
                    section12 = updateSection(sec12,12,leaders_group)
                    if section1 != '' or section2 != '' or section3 != '' or section4 != '' or section5 != '' or section6 != '' or section7 != '' or section8 != '' or section9 != '' or section10 != '' or section11 != '' or section12 != '':
                        error_msg = 'Select clubber(s) to \'E\'dit in first column to make changes.'
                    else:
                        AdvanceSectionIfNeededTT(books)                                 
                elif chapterChanged not in leaders_group:   
                    error_msg = 'Select clubber(s) to \'E\'dit in first column to make changes.'                                 
            elif bookChanged not in leaders_group:   
                error_msg = 'Select clubber(s) to \'E\'dit in first column to make changes.'                                 
        else:
            error_msg = 'Select clubber(s) to \'E\'dit in first column to make changes.'
    
    context = HandBook(request,'3', leader_name, leaders_group, error_msg)
    return HttpResponse(template.render(context,request))

def BookSparks(request):
    template = loader.get_template('AwanaRecordKeeping/BookSparks.html')
    leader_name = ''
    leaders_group = {}
    error_msg = ''
    if request.method == 'POST':
        leader = request.POST.getlist("leadername")
        leaders_group = request.POST.getlist("leader")
        leader_name = leader[0]
        if len(leaders_group) > 0:
            bookChanged = ''
            chapterChanged = ''        
            #print (request.POST)
            books = request.POST.getlist("sbook")
            bookChanged = updateBook(books, leaders_group)      
            if bookChanged == '':
                chapters = request.POST.getlist("schap")
                chapterChanged = updateChapter(chapters,leaders_group)
                #print ('chapter changed ' + chapterChanged)            
                if chapterChanged == '':
                    sec1 = request.POST.getlist('section1')
                    section1 = updateSection(sec1,1,leaders_group)        
                    sec2 = request.POST.getlist('section2')
                    section2 = updateSection(sec2,2,leaders_group)        
                    sec3 = request.POST.getlist('section3')
                    section3 = updateSection(sec3,3,leaders_group)        
                    sec4 = request.POST.getlist('section4')
                    section4 = updateSection(sec4,4,leaders_group)        
                    sec5 = request.POST.getlist('section5')
                    section5 = updateSection(sec5,5,leaders_group)        
                    sec6 = request.POST.getlist('section6')
                    section6 = updateSection(sec6,6,leaders_group)        
                    sec7 = request.POST.getlist('section7')
                    section7 = updateSection(sec7,7,leaders_group)        
                    sec8 = request.POST.getlist('section8')
                    section8 = updateSection(sec8,8,leaders_group)
                    if section1 != '' or section2 != '' or section3 != '' or section4 != '' or section5 != '' or section6 != '' or section7 != '' or section8 != '':
                        error_msg = 'Select clubber(s) to \'E\'dit in first column to make changes.'                                 
                    else:
                        AdvanceSectionIfNeededSpark(books)                                 
                elif chapterChanged not in leaders_group:   
                    error_msg = 'Select clubber(s) to \'E\'dit in first column to make changes.'                                 
            elif bookChanged not in leaders_group:   
                error_msg = 'Select clubber(s) to \'E\'dit in first column to make changes.'                                 
        else:
            error_msg = 'Select clubber(s) to \'E\'dit in first column to make changes.'
    context = HandBook(request,'2', leader_name, leaders_group, error_msg)
    return HttpResponse(template.render(context,request))
