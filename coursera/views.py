import urllib2
from django.shortcuts import render_to_response
import ast


rest_url = 'https://api.coursera.org/api/catalog.v1/'
def get_courses(request):
    courses_data = {}
    courses_list = []
    if request.method == 'GET':
        #import pdb; pdb.set_trace()
        ''' all courses data'''
        c_url = rest_url + 'courses?fields=name,language&includes=universities,sessions'
        c_data = urllib2.urlopen(c_url)
        reply_data = c_data.read()
        c_data.close()
        final_data = ast.literal_eval(reply_data)    
        final_data = final_data['elements']

        ''' fetching the all university data'''
        u_url = rest_url + 'universities?fields=name,id'
        u_data = urllib2.urlopen(u_url)
        u_all_data = u_data.read()
        u_data.close()
        u_all_data = ast.literal_eval(u_all_data)    
        u_all_data = u_all_data['elements']

        ''' fetching session related data '''
        s_url = rest_url + 'sessions?fields=durationString,startDay,startMonth,startYear'
        s_data = urllib2.urlopen(s_url)
        s_all_data = s_data.read()
        s_data.close()
        s_all_data = ast.literal_eval(s_all_data)    
        s_all_data = s_all_data['elements']

        for data in final_data:
            if data:
                courses_data['name'] = data.get('name')
                courses_data['language'] = data.get('language')  
                courses_data['url'] = data.get('shortName')
                links = data.get('links') 
                uni = links.get('universities')
                ''' here we can call the restful Api by using the id to get the Exact information but it was show slow '''
                u_name = [item.get('name') for item in u_all_data if item.get('id') == uni[0]]
                if u_name:
                    courses_data['universtity'] = u_name[0]

                ses = links.get('sessions') 
                s_duration = [{'duration':item.get('durationString'),'startDay':item.get('startDay'),\
                               'startMonth':item.get('startYear'),'startYear':item.get('startYear')\
                              } for item in s_all_data if item.get('id') == ses[0]]
                if s_duration:
                    courses_data['duration'] = s_duration[0]['duration']
                    courses_data['startDay'] = s_duration[0]['startDay']
                    courses_data['startMonth'] = s_duration[0]['startMonth']
                    courses_data['startYear'] = s_duration[0]['startYear']
                courses_list.append(courses_data.copy())
        return render_to_response('coursera/cources.html', {'data' : courses_list})

def course_detail(request, detail):
    c_url = rest_url + 'courses?fields=name,aboutTheCourse,photo,courseSyllabus,video'
    c_data = urllib2.urlopen(c_url)
    reply_data = c_data.read()
    c_data.close()
    final_data = ast.literal_eval(reply_data)    
    final_data = final_data['elements']
    final_data = [item for item in final_data if item['shortName'] == detail]
    return render_to_response('coursera/detail.html', {'details' : final_data})

