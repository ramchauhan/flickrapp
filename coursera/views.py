import urllib2
from django.shortcuts import render_to_response
import ast



rest_url = 'https://api.coursera.org/api/catalog.v1/'


def get_data(rest_query):
    post_url = rest_url + rest_query 
    all_data = urllib2.urlopen(post_url)
    reply_data = all_data.read()
    all_data.close()
    final_data = ast.literal_eval(reply_data)    
    return final_data['elements']

def get_courses(request):
    courses_data = {}
    courses_list = []
    if request.method == 'GET':
        import pdb; pdb.set_trace()
        ''' all courses data'''
        final_data = get_data('courses?fields=name,language&includes=universities,sessions')
        
        ''' fetching the all university data'''
        u_all_data = get_data('universities?fields=name,id')

        ''' fetching session related data '''
        s_all_data = get_data('sessions?fields=durationString,startDay,startMonth,startYear')
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
    final_data = get_data('courses?fields=name,aboutTheCourse,photo,courseSyllabus,video')
    final_data = [item for item in final_data if item['shortName'] == detail]
    return render_to_response('coursera/detail.html', {'details' : final_data})

