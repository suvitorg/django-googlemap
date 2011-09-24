# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings
from django.template.loader import render_to_string

DEFAULT_WIDTH = 500
DEFAULT_HEIGHT = 300

DEFAULT_LATITUDE = getattr(settings, 'GMAP_DEFAULT_LATITUDE', 56.8436)
DEFAULT_LONGTITUDE = getattr(settings, 'GMAP_DEFAULT_LONGTITUDE', 60.6073)

def get_latlng(value):
    if isinstance(value, unicode):
        a, b = value.split(',')
    else:
        a, b = value

    return float(a), float(b)


class LocationWidget(forms.widgets.Widget):
    
    class Media:
        js = ["http://maps.googleapis.com/maps/api/js?sensor=false",
              settings.MEDIA_URL + 'js/jquery-1.4.2.min.js',
              settings.MEDIA_URL + 'js/googlemap/manager.js',
             ]
    
    def __init__(self, *args, **kw):
        self.map_width = kw.get("map_width", DEFAULT_WIDTH)
        self.map_height = kw.get("map_height", DEFAULT_HEIGHT)
        
        super(LocationWidget, self).__init__(*args, **kw)
        self.inner_widget = forms.widgets.HiddenInput()

    def render(self, name, value, *args, **kwargs):
        
        if not value:
            lat = DEFAULT_LATITUDE
            lng = DEFAULT_LONGTITUDE
        else:
            lat, lng = get_latlng(value)
        
        inner_widget = self.inner_widget.render("%s" % name,
                                                "%f,%f" % (lat,lng),
                                                dict(id='id_%s' % name))

        return render_to_string('googlemap/widget.html',
                  {'name':name,
                   'def_lat':DEFAULT_LATITUDE, 'def_lng':DEFAULT_LONGTITUDE,
                   'inner_widget':inner_widget,
                   'map_width':self.map_width,
                   'map_height':self.map_height
                  })


class LocationField(forms.Field):
    widget = LocationWidget

    def clean(self, value):
        return "%f,%f" % get_latlng(value)
