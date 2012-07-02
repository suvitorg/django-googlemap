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
  init: function() {
    if (!(google || google.maps))
      return;

    $('div.' + GoogleMapManager.options.div_class).each(function(){
      map = this;
      input = $(map).prev();
      latlng = input.val().split(',', 2);
      var point = new google.maps.LatLng(parseFloat(latlng[0]),
                                          parseFloat(latlng[1]));

      GoogleMapManager.load(map, point);
 
      //add clear link
      $(map).after('<a href="#">' + GoogleMapManager.options.restore_title +'</a>')
            .next('a').click(function(){
        GoogleMapManager.resetPosition($(this).prev('div'));
        return false;
      });

    });
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

    input = $(map).prev('input');
    input.val(point.lat().toFixed(6) + "," + point.lng().toFixed(6));
  },
  load: function(map, point) {
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

    /* save coordinates on clicks */
    google.maps.event.addListener(gmap, "click", function (overlay, point) {
      GoogleMapManager.clear_markers(map);
      GoogleMapManager.add_market(map, point);
      GoogleMapManager.savePosition(map, point);
    });
  }
};

$(document).ready(function() {
  GoogleMapManager.init();
});
