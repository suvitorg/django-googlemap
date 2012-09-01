// Author: PROGWAY LLC
// (c) 2011

var GoogleMapManager = GoogleMapManager || {
  options: {
    div_class: 'gmap',
    zoom: 15,
    def_point: null, //setted later
    marker_title: 'Координаты адреса',
    restore_title: 'Сбросить'
  },
  inited: false,
  init: function() {
    if (!(window['google'] && google.maps))
      return;

    if (GoogleMapManager.inited)
      return;

    $('div.' + GoogleMapManager.options.div_class).each(function(){
      var map = $(this),
          center,
          simple = false;

      if (map.attr('center')) {
        center = map.attr('center');
        simple = true;
      }
      else
        center = map.prev().find('input').val();
      var latlng = center.split(',', 2);

      var point = new google.maps.LatLng(parseFloat(latlng[0]),
                                         parseFloat(latlng[1]));

      GoogleMapManager.load(this, point, simple);

      if (!simple) {
        //add clear link
        map.after('<a href="#">' + GoogleMapManager.options.restore_title +'</a>')
              .next('a').click(function(){
          GoogleMapManager.resetPosition($(this).prev('div'));
          return false;
        });
      }

    });

    GoogleMapManager.inited = true;
  },

  add_marker: function(map, point){
    gmap = $(map).data('gmap');
    markers = $(map).data('gmapmarkers');

    var m = new google.maps.Marker({
      position: point,
      map: gmap,
      draggable: true,
      title : GoogleMapManager.options.marker_title
    });

    markers.push(m);

    google.maps.event.addListener(m, "dragend", function() {
      point = m.getPosition();
      GoogleMapManager.savePosition(map, point);
    });
  },
  clear_markers: function(map){
    markers = $(map).data('gmapmarkers');
    $.each(markers, function(i, item){
      item.setMap(null);
    });
    markers.length = 0;
  },
  resetPosition: function(map){
    var point = GoogleMapManager.options.def_point;

    gmap = $(map).data('gmap');
    GoogleMapManager.clear_markers(map);
    gmap.setCenter(point);

    GoogleMapManager.add_marker(map, point);
    GoogleMapManager.savePosition(map, point);
    return false;
  },
  savePosition: function(map, point) {
    gmap = $(map).data('gmap');
    gmap.panTo(point);

    input = $(map).prev().find('input');
    input.val(point.lat().toFixed(6) + "," + point.lng().toFixed(6));
  },
  load: function(map, point, simple) {
    var center = point;

    var myOptions = {
        zoom: 15,
        center: center,
        mapTypeId: google.maps.MapTypeId.ROADMAP
      };

    gmap = new google.maps.Map(map, myOptions);
    $(map).data('gmap', gmap);
    $(map).data('gmapmarkers', []);

    GoogleMapManager.add_marker(map, point);

    if (!simple) {
      /* save coordinates on clicks */
      google.maps.event.addListener(gmap, "click", function (event) {
        GoogleMapManager.clear_markers(map);
        GoogleMapManager.add_marker(map, event.latLng);
        GoogleMapManager.savePosition(map, event.latLng);
      });
    }
  },
};

$(document).ready(function() {
  $.getScript("http://maps.google.com/maps/api/js?sensor=true&callback=GoogleMapManager.init");
});
