from django import forms
from django.forms.formsets import BaseFormSet

class PerformanceForm(forms.Form):
    OPTIONS = (
                ("male", "Male"),
                ("female", "Female"),
                )
    gender = forms.ChoiceField(choices=OPTIONS)
    OPTIONS_DIST = (
                ("None","NONE"),
                ("0", "100 metres"),
                ("1", "200 metres"),
                ("2", "400 metres"),
                ("3", "800 metres"),
                ("4", "1500 metres"),
                ("5", "Mile"),
                ("6", "5 km"),
                ("7", "10 km"),
                ("8", "Half-Marathon"),
                ("9", "Marathon"),
                )
    distance1 = forms.ChoiceField(choices=OPTIONS_DIST,label='Distance A')
    time1 = forms.CharField(initial='0:00:00.00',label='Time A')
    distance2 = forms.ChoiceField(choices=OPTIONS_DIST,label='Distance B')
    time2 = forms.CharField(initial='0:00:00.00',label='Time B')
    distance3 = forms.ChoiceField(choices=OPTIONS_DIST,label='Distance C')
    time3 = forms.CharField(initial='0:00:00.00',label='Time C')
    distanceToPredict = forms.ChoiceField(choices=OPTIONS_DIST,label='Distance to predict')


class LinkForm(forms.Form):
    """
    Form for individual user links
    """
    OPTIONS_DIST = (
                ("0", "100 metres"),
                ("1", "200 metres"),
                ("2", "400 metres"),
                ("3", "800 metres"),
                ("4", "1500 metres"),
                ("5", "Mile"),
                ("6", "5 km"),
                ("7", "10 km"),
                ("8", "Half-Marathon"),
                ("9", "Marathon"),
                )
    anchor = forms.ChoiceField(choices=OPTIONS_DIST,label='Bla')
    url = forms.CharField(
                    widget=forms.TextInput(),
                    required=False)

class ProfileForm(forms.Form):
    """
    Form for user to update their own profile details
    (excluding links which are handled by a separate formset)
    """
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        OPTIONS = (
                    ("male", "Male"),
                    ("female", "Female"),
                    )

        self.fields['first_name'] = forms.ChoiceField(choices=OPTIONS,label='Test')
        OPTIONS_DIST = (
                    ("0", "100 metres"),
                    ("1", "200 metres"),
                    ("2", "400 metres"),
                    ("3", "800 metres"),
                    ("4", "1500 metres"),
                    ("5", "Mile"),
                    ("6", "5 km"),
                    ("7", "10 km"),
                    ("8", "Half-Marathon"),
                    ("9", "Marathon"),
                    )
        self.fields['to_predict'] = forms.ChoiceField(choices=OPTIONS_DIST,label='To Predict')
#        self.fields['last_name'] = forms.CharField(
#                                        max_length=30,
#                                        initial = 'Blythe',
#                                        widget=forms.TextInput(attrs={
#                                            'placeholder': 'Last Name',
#                                        }))

class BaseLinkFormSet(BaseFormSet):
    def clean(self):
        """
        Adds validation to check that no two links have the same anchor or URL
        and that all links have both an anchor and URL.
        """
        if any(self.errors):
            return

        anchors = []
        urls = []
        duplicates = False

        for form in self.forms:
            if form.cleaned_data:
                anchor = form.cleaned_data['anchor']
                url = form.cleaned_data['url']

                # Check that no two links have the same anchor or URL
                if anchor and url:
                    if anchor in anchors:
                        duplicates = True
                    anchors.append(anchor)

                    if url in urls:
                        duplicates = True
                    urls.append(url)

                if duplicates:
                    raise forms.ValidationError(
                        'Links must have unique anchors and URLs.',
                        code='duplicate_links'
                    )

                # Check that all links have both an anchor and URL
                if url and not anchor:
                    raise forms.ValidationError(
                        'All links must have an anchor.',
                        code='missing_anchor'
                    )
                elif anchor and not url:
                    raise forms.ValidationError(
                        'All links must have a URL.',
                        code='missing_URL'
                    )
