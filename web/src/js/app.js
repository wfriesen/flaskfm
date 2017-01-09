var last_scrobble, last_scrobble_poll;

function scrobbled_since_text(object) {
  return object.scrobbles + ' scrobbles since ' + object.first_scrobble;
}

function show_artist_modal(url) {
  $.get(url, function(data) {
    $('#artistModalHeader').html(data.artist.name);
    $('#artistModalInfo').html(scrobbled_since_text(data.artist));

    var albums = '';
    $.each(data.artist.albums, function(i, album) {
      albums +=
        '<div class="ui segment">' +
        '<a href="#" onclick="show_album_modal(\'' + album.url + '\')">' + album.name + '</a> ' + scrobbled_since_text(album) + '</div>';
    });
    $('#artistModalAlbums').html(albums);

    $('#artistModal').modal('show');
  });
};

function show_album_modal(url) {
  $.get(url, function(data) {
    $('#albumModalHeader').html('<a href="#" onclick="show_artist_modal(\'' + data.album.artist.url + '\')">' + data.album.artist.name + '</a> - ' + data.album.name);
    $('#albumModalInfo').html(scrobbled_since_text(data.album));

    var tracks = '';
    $.each(data.album.tracks, function(i, track) {
      tracks += '<div class="ui segment">' +
      '<a href="#" onclick="show_track_modal(\'' + track.url + '\')">' + track.name + '</a> (' + scrobbled_since_text(track) + ')</div>';
    });
    $('#albumModalTracks').html(tracks);

    $('#albumModal').modal('show');
  });
};

function show_track_modal(url) {
  $.get(url, function(data) {
    $('#trackModalHeader').html(
      '<a href="#" onclick="show_artist_modal(\'' + data.track.artist.url + '\')">' + data.track.artist.name + '</a> - ' + data.track.name + ' ' +
      '<a href="#" onclick="show_album_modal(\'' + data.track.album.url + '\')">[' + data.track.album.name + ']</a>'
    );
    $('#trackModalInfo').html(scrobbled_since_text(data.track));

    $('#trackModal').modal('show');
  });
};

function remove_scrobble(url) {
  $.ajax({
    url: url,
    type: 'DELETE',
    success: function(response) {
      $('div[data-scrobble-url="' + url + '"]').transition({
        animation: 'scale',
        onComplete: function() {
          last_scrobble = undefined;
          get_user_stats();
        }
      });
    }
  });
};

function get_user_stats() {
  $.get("/api/v0.1/user_stats", function(data) {
    html = '<p>' + data.stats.scrobble_count + ' scrobbles since ' + data.stats.first_scrobble + '</p>'
    last_scrobble = data.stats.last_scrobble
    restart_polling();
    $("#userstats").html(html);

    html = '';
    $.each(data.stats.last_ten_scrobbles, function(index, item) {
      html +=
        '<div class="ui segment" data-scrobble-url="' + item.url + '">' +
        '<a href="#" onclick="show_artist_modal(\'' + item.artist.url + '\')">' + item.artist.name + '</a>' +
        ' - <a href="#" onclick="show_track_modal(\'' + item.track.url + '\')">' + item.track.name + '</a> - ' +
        '<a href="#" onclick="show_album_modal(\'' + item.album.url + '\')">[' + item.album.name + ']</a>' +
        '<span title="' + item.scrobble_timestamp + '"> (' + item.scrobble_timestamp + ')</span>' +
        '<a href="#" onclick="remove_scrobble(\'' + item.url + '\')"><i class="remove circle icon"></i></a>' +
        '</div>';
    });
    $('#recentscrobbles').html(html);
  });
};

function restart_polling() {
  clearInterval(last_scrobble_poll);
  last_scrobble_poll = setInterval(function() {
    $.get('/api/v0.1/last_scrobble', function(data) {
      if ( last_scrobble !== undefined && last_scrobble !== data.last_scrobble) {
        get_user_stats();
      }
      last_scrobble = data.last_scrobble;
    });
  }, 5000);
}

$(document).ready(function() {
  get_user_stats();
});
