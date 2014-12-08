import urllib2
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.conf import settings
from django.views.generic import ListView
from .forms import PhotoForm, UserDataForm
from .models import UserData
import xmltodict


api_key = settings.FLICKR_API_KEY
api_password = settings.FLICKR_API_SECRET
url = settings.FLICKR_REST_URL

def get_all_photo(request):

    if request.method == 'GET':
        form = PhotoForm()
    else:
        import json
        form = PhotoForm(request.POST)
        if form.is_valid():
            ''' concept behind searching the images for a location is, first find the location \
                then serch the images for that location 
            '''
            ''' Finding the place woe_id to search the images '''

            location = form.cleaned_data['location']
            post_data = 'method=flickr.places.find&api_key=' +api_key+ '&query=' +location+ '&format=rest'
            flickr_places = urllib2.urlopen(url, post_data)
            reply_data = flickr_places.read()
            flickr_places.close()
            all_places = xmltodict.parse(reply_data)

            ''' checking the status of the response from, flickr rest api'''
            #import pdb; pdb.set_trace()
            if all_places['rsp']['places']['@total'] == '0':
                return render(request, 'flickr/photos.html', {'no_data' : 'No record founds!!  try again, for new search',})

            ''' Searching for the images according to the return woe_id '''
            try:
                woe_id = all_places['rsp']['places']['place'][0]['@woeid']
            except KeyError:
                woe_id = all_places['rsp']['places']['place']['@woeid']
            post_data = 'method=flickr.photos.search&api_key=' +api_key+ '&woe_id=' +woe_id
            flickr_phptos = urllib2.urlopen(url, post_data)
            reply_photo_data = flickr_phptos.read()
            flickr_phptos.close()
            all_photos = xmltodict.parse(reply_photo_data)
            try:
                data = [dict(x) for x in all_photos['rsp']['photos']['photo']]
                ''' updating the database for user with ip address and search key '''

                db = UserDataForm()
                instance = db.save(commit=False)
                instance.search_key = location
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    instance.user_ip = x_forwarded_for.split(',')[-1].strip()
                else:
                    instance.user_ip = request.META.get('REMOTE_ADDR')

                instance.save()
            except KeyError:
                return render(request, 'flickr/photos.html', {'no_data' : 'No record founds!!  try again, for new search',})
            photo_list = []
            for item in data:
                image = "<img src='https://farm%s.staticflickr.com/%s/%s_%s_m.jpg'/>" %(item['@farm'], item['@server'], item['@id'], item['@secret'])
                photo_list.append(image)
            return render_to_response('flickr/photos.html', {'data' : photo_list, 'woe_id': woe_id, 'page' :'1', 'all_pages':all_photos['rsp']['photos']['@pages']})

    return render(request, 'flickr/search.html', {
        'form': form,
    })

def ajax_search_view(request):
    import json
    if request.is_ajax():
        woe_id = request.GET['location_woeid']
        page_number = request.GET['page_number']
        post_data = 'method=flickr.photos.search&api_key=' +api_key+ '&woe_id=' +woe_id+ '&page=' +page_number+ '&format=rest'
        flicksocket_phptos = urllib2.urlopen(url, post_data)
        reply_photo_data = flicksocket_phptos.read()
        flicksocket_phptos.close()
        all_photos = xmltodict.parse(reply_photo_data)
        all_photos['rsp']['photos']['woe_id'] = woe_id
        all_photos['rsp']['photos']['page'] = page_number
        all_photos['rsp']['photos']['all_pages'] = all_photos['rsp']['photos']['@pages']
        json = json.dumps(all_photos['rsp']['photos'])
        return HttpResponse(json, content_type='application/json')

def show_search_data(request):
    data = UserData.objects.all()
    return render_to_response("flickr/data.html", {'data' : data})


