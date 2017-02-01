from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone
from .forms import PerformanceForm, LinkForm, BaseLinkFormSet, ProfileForm
from django.forms.formsets import formset_factory
from numpy import load, zeros, nan, isnan
from prediction_formula import *
from getpass import getuser
import pdb

USER = getuser()

def enter_perform(request):
    form = PerformanceForm()
    return render(request, 'calculator/enter_times.html', {'form': form, 'results': 'Prediction:', 'color': 'white'})

def enter_perform_variable(request):
    form = PerformanceForm()
    return render(request, 'calculator/enter_times_variable.html', {'form': form, 'results': 'Prediction:', 'color': 'white'})

def calculateresult(request,distance_pred,gender,distance1,time1,distance2,time2,distance3,time3):
    try:
        if USER=='duncanblythe':
            if gender=='male':
                x = load('male.npy')
            else:
                x = load('female.npy')
        else:
            if gender=='male':
                x = load('/home/blythed/running_calculator/male.npy')
            else:
                x = load('/home/blythed/running_calculator/female.npy')
        distance1 = int(distance1)
        time1 = convert_to_seconds(time1)

        if distance2.isdigit():
            distance2 = int(distance2)
            time2 = convert_to_seconds(time2)
        else:
            distance2 = np.nan

        if distance3.isdigit():
            distance3 = int(distance3)
            time3 = convert_to_seconds(time3)
        else:
            distance3 = np.nan

        data = nan*zeros(10)
        data[distance1] = time1
        if not(isnan(distance2)):
            data[distance2] = time2
        if not(isnan(distance3)):
            data[distance3] = time3

        tbc = zeros(10)
        tbc[distance_pred] = 1
        prediction, error = portal_to_prediction(x,data,tbc)
        prediction = convert_to_time(prediction)
        error = convert_to_time(error)
        response = prediction+",&plusmn"+error
    except ValueError:
        response = ",input should be hrs:mins:secs;<br> select distances and please try again"
    except IndexError:
        response = ",select distances and please try again"
    return HttpResponse(response)

def test_profile_settings(request):
    LinkFormSet = formset_factory(LinkForm, formset=BaseLinkFormSet)

#    if request.method == 'POST':
#        profile_form = ProfileForm(request.POST)
#        link_formset = LinkFormSet(request.POST)
#
#        if profile_form.is_valid() and link_formset.is_valid():
#            first_name = profile_form.cleaned_data.get('first_name')
#            last_name = profile_form.cleaned_data.get('last_name')
#            print first_name
#
#            for link_form in link_formset:
#                anchor = link_form.cleaned_data.get('anchor')
#                url = link_form.cleaned_data.get('url')
#                print anchor
#                print url

    profile_form = ProfileForm()
    link_formset = LinkFormSet(initial=[])

    context = {
        'profile_form': profile_form,
        'link_formset': link_formset,
    }

    return render(request, 'calculator/edit_profile.html', context)

def threenumbersummary(request,t0,t1,t2,t3,t4,t5,t6,t7,t8,t9):
    times = np.zeros(10)
    if USER=='duncanblythe':
        x = load('male.npy')
        d = load('distances.npy')
    else:
        x = load('/home/blythed/running_calculator/male.npy')
        d = load('/home/blythed/running_calculator/distances.npy')
    for i in range(10):
        exec('times[i] = convert_to_seconds(t%d)' % i)
    #try:
    times[np.where(times==0)] = np.nan
    tbc = np.zeros(10)
    tbc[np.where(np.isnan(times))] = 1
    print "predicting"
    prediction, error = portal_to_prediction_tns(x,times,tbc)
    prediction_disp = [convert_to_time(t) for t in prediction]
    speed = d/prediction
    prediction_disp =  ','.join(map(str, prediction_disp)) 
    x = np.zeros((len(d),2))
    x[:,0] = speed
    x[:,1] = d
    x = [list(x[i,:]) for i in range(x.shape[0])]
    return HttpResponse(convert_array_to_string(x)+'<br>'+prediction_disp)

def convert_array_to_string(arr):
    y = "["
    for i in range(len(arr)):
        if i<len(arr)-1:
            y+="["+','.join(map(str, arr[i]))+"]," 
        else:
            y+="["+','.join(map(str, arr[i]))+"]" 
    y+="]"
    return y

def get_weights(request):
    if USER=='duncanblythe':    
        f = open('/Users/duncanblythe/work/repo/running_calculator/weights.csv')
        csvz = f.read()
    else:
        f = open('/home/blythed/running_calculator/weights.csv')
        csvz = f.read()
    return HttpResponse(csvz)
