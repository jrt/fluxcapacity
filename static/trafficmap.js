//var baseurl = "http://localhost:5000";
var baseurl = ''
var circles = {}
var next = '201505010500'
var timer_event = null;
var map = null;
var infowindow = null;

function initialize() {
	var mapProp = {
		center: new google.maps.LatLng(-31.946,115.854),
		zoom: 15,
		mapTypeId: google.maps.MapTypeId.ROADMAP
	};
	map = new google.maps.Map(document.getElementById("googleMap"),mapProp);

	infowindow = new google.maps.InfoWindow({});

	$.getJSON(baseurl + '/locations').done(function(locs) {
		$.each(locs, function(i, row) {
			var tcsno = row[0]
			var point = new google.maps.LatLng(row[1],row[2]);
			var opts = {
				strokeColor: '#0000FF',
				strokeOpacity: 0.8,
				strokeWeight: 2,
				fillColor: '#0000FF',
				fillOpacity: 0.35,
				map: map,
				center: point,
				radius: 25.0
			}
			var circle = new google.maps.Circle(opts);
			google.maps.event.addListener(circle, 'click', function(ev) {
				get_tcs_info(tcsno, ev);
			});
			circles[tcsno] = circle;
		});
	});
}

function get_tcs_info(tcsno, ev) {
	$.getJSON(baseurl + '/tcs/' + tcsno).done(function(info) {
		var cont = '<h1>' + tcsno + '</h1>';
		if ('img' in info) {
			cont += '<img src="' + baseurl + '/' + info['img'] + '"></img>';
		}
		infowindow.setContent(cont);
		infowindow.setPosition(ev.latLng);
		infowindow.open(map);
	});
}


function get_next() {
	$.getJSON(baseurl + '/data/' + next).done(function(res) {
		var data = res['data']
		next = res['next'];
		$("div#time").text(res['time']);
		if (next == '') {
			pause_traffic();
			next = '201505010500'
		}
		$.each(data, function(i, row) {
			var tcsno = row[0];
			var count = row[1];
			var red = Math.min(255,Math.floor(count));
			var green = 255-red;
			var color = "rgb(" + red + "," + green + ",0)";
			var radius = Math.max(25,count/4);

			circles[tcsno].setOptions({
				fillColor: color,
				strokeColor: color,
				radius: radius
			});
		});
	});
}

function play_traffic() {
	timer_event = setInterval(function() { get_next()}, 500);
}

function pause_traffic() {
	clearInterval(timer_event);
	timer_event = null;
}

google.maps.event.addDomListener(window, 'load', initialize);
