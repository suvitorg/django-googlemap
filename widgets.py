# -*- coding: utf-8 -*-

from django import forms
from django.utils.safestring import mark_safe
from django.conf import settings

DEFAULT_WIDTH = 500
DEFAULT_HEIGHT = 300


DEFAULT_LATITUDE = getattr(settings, 'GMAP_DEFAULT_LATITUDE', 56.8436)
DEFAULT_LONGTITUDE = getattr(settings, 'GMAP_DEFAULT_LONGTITUDE', 60.6073)



class LocationWidget(forms.widgets.Widget):
    
    class Media:
        js = ["http://maps.google.com/maps?file=api&amp;v=2&amp;sensor=false&amp;key=x",]
    
    def __init__(self, *args, **kw):
        self.map_width = kw.get("map_width", DEFAULT_WIDTH)
        self.map_height = kw.get("map_height", DEFAULT_HEIGHT)
        
        super(LocationWidget, self).__init__(*args, **kw)
        self.inner_widget = forms.widgets.HiddenInput()

    def render(self, name, value, *args, **kwargs):
        
        if not value:
            a = DEFAULT_LATITUDE
            b = DEFAULT_LONGTITUDE
        else:    
            if isinstance(value, unicode):
                a, b = value.split(',')
            else:
                a, b = value
        
        lat, lng = float(a), float(b)
        
        js = '''
        <script type="text/javascript">
        //<![CDATA[

        var map_%(name)s;
    
    function resetPosition_%(name)s()
    {
        var point = new GLatLng(%(def_lat)f, %(def_lng)f)
        
        map_%(name)s.clearOverlays();
        m = new GMarker(point, {draggable: true});
        map_%(name)s.setCenter(point, 15);
        GEvent.addListener(m, "dragend", function() {
               point = m.getPoint();
               savePosition_%(name)s(point);
                });
        map_%(name)s.addOverlay(m);
        savePosition_%(name)s(point);

    }
    function savePosition_%(name)s(point)
    {
        var latitude = document.getElementById("id_%(name)s");
        //var longitude = document.getElementById("id_%(name)s_longitude");
        latitude.value = point.lat().toFixed(6) + "," + point.lng().toFixed(6);
        //longitude.value = point.lng().toFixed(6);
        map_%(name)s.panTo(point);
    }

    function load_%(name)s() {
        if (GBrowserIsCompatible()) {
            map_%(name)s = new GMap2(document.getElementById("map_%(name)s"));
            map_%(name)s.addControl(new GSmallMapControl());
            map_%(name)s.addControl(new GMapTypeControl());

            var point = new GLatLng(%(lat)f, %(lng)f);
            map_%(name)s.setCenter(point, 15);
            m = new GMarker(point, {draggable: true});

            GEvent.addListener(m, "dragend", function() {
                    point = m.getPoint();
                    savePosition_%(name)s(point);
            });

            map_%(name)s.addOverlay(m);

            /* save coordinates on clicks */
            GEvent.addListener(map_%(name)s, "click", function (overlay, point) {
                savePosition_%(name)s(point);
            
                map_%(name)s.clearOverlays();
                m = new GMarker(point, {draggable: true});

                GEvent.addListener(m, "dragend", function() {
                    point = m.getPoint();
                    savePosition_%(name)s(point);
                });

                map_%(name)s.addOverlay(m);
            });
        }
    }
//]]>
</script> 
    <script type="text/javascript"> $(document).ready(function() {    
        load_%(name)s();
            }); </script>
            
        ''' % dict(name=name, lat=lat, lng=lng, def_lat=DEFAULT_LATITUDE, def_lng=DEFAULT_LONGTITUDE)
        
        html = self.inner_widget.render("%s" % name, "%f,%f" % (lat,lng), dict(id='id_%s' % name))
        html += "<div id=\"map_%s\" class=\"gmap\" style=\"width: %dpx; height: %dpx\"></div>" % (name, self.map_width, self.map_height)
        
        html += '<a href="#" onclick="resetPosition_%(name)s()">Сбросить</a>' % dict(name=name)
        return mark_safe((js+html))


class LocationField(forms.Field):
    widget = LocationWidget

    def clean(self, value):
         
        if isinstance(value, unicode):
            a, b = value.split(',')
        else:
            a, b = value
        lat, lng = float(a), float(b)
        return "%f,%f" % (lat, lng)
