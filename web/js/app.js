var last_scrobble, last_scrobble_poll;

function show_artist_modal(id) {
  $.get('http://localhost:5000/flaskfm/api/v0.1/scrobble_artist_info/' + id, function(data) {
    var artist_info = data['scrobble_artist_info']['info'];
    var album_info = data['scrobble_artist_info']['albums'];
    $('#artistModalHeader').html(artist_info['artist']);
    $('#artistModalInfo').html('Scrobbled ' + artist_info['total_scrobbles'] + ' times since ' + artist_info['first_scrobble']);

    var albums = '';
    $.each(album_info, function() {
      albums += '<div class="ui segment">' + this['album'] + ' (' + this['play_count'] + ' scrobbles since ' + this['first_scrobble'] + ')</div>'
    });
    $('#artistModalAlbums').html(albums);

    $('#artistModal').modal('show');
  });
};

function remove_scrobble(id) {
  $.ajax({
    url: 'http://localhost:5000/flaskfm/api/v0.1/delete_scrobble/' + id,
    type: 'DELETE',
    success: function(response) {
      $('#recent-scrobble-' + id).transition({
        animation: 'scale',
        onComplete: function() {
          last_scrobble = undefined;
          get_recent_scrobbles();
          get_user_stats();
        }
      });
    }
  });
};

function get_recent_scrobbles() {
  $.get("http://localhost:5000/flaskfm/api/v0.1/recent", function(data) {
    var html = '';
    $.each(data.scrobbles, function(index, item) {
      html +=
        '<div class="ui segment" id="recent-scrobble-' + this.id + '">' +
        '<a href="#" onclick="show_artist_modal(' + this.id + ')">' + this.artist + '</a>' +
        ' - ' + this.track + ' [' + this.album + ']' +
        '<span title="' + this.timestamp + '"> (' + this.human_timestamp + ')</span>' +
        '<a href="#" onclick="remove_scrobble(' + this.id + ')"><i class="remove circle icon"></i></a>' +
        '</div>';
    });
    $("#recentscrobbles").html(html);
  });
};

function get_user_stats() {
  $.get("http://localhost:5000/flaskfm/api/v0.1/user_stats", function(data) {
    html = '<p>' + data.stats.scrobble_count + ' scrobbles since ' + data.stats.first_scrobble + '</p>'
    last_scrobble = data.stats.last_scrobble
    restart_polling();
    $("#userstats").html(html);
  });
};

function restart_polling() {
  clearInterval(last_scrobble_poll);
  last_scrobble_poll = setInterval(poll_for_last_scrobble, 5000);
}

function poll_for_last_scrobble() {
  $.get('http://localhost:5000/flaskfm/api/v0.1/last_scrobble', function(data) {
    if ( last_scrobble !== undefined && last_scrobble !== data.last_scrobble) {
      get_recent_scrobbles();
      get_user_stats();
    }
    last_scrobble = data.last_scrobble;
  });
};

$(document).ready(function() {
  get_recent_scrobbles();
  get_user_stats();
});
