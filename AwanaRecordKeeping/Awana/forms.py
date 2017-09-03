from django import forms  
from Awana.models import Clubber

TT_BOOKS = (
    ('TSZ', 'T&T Start Zone'),
    ('GIA', 'T&T Grace In Action'),
    ('AD1', 'T&T Adventure Book1'),
    ('AD2', 'T&T Adventure Book2'),
    ('CH1', 'T&T Challenge Book1'),
    ('CH2', 'T&T Challenge Book2'),
)

class TTForm(forms.Form):  
    
    def __init__(self,*args,**kwargs):
        my_arg = kwargs.pop('club')
        super(TTForm,self).__init__(*args,**kwargs)
        self.club_enum = '4'
 
        club_roll = Clubber.objects.filter(club=my_arg)
        for c in club_roll:
             self.fields['book_%s' % c]= forms.ChoiceField(choices=TT_BOOKS, label=c, widget=forms.Select(attrs={'onchange': 'this.form.submit()'}), required=True )
