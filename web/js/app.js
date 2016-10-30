function remove_scrobble(id) {
  $.ajax({
    url: 'http://localhost:5000/flaskfm/api/v0.1/delete_scrobble/' + id,
    type: 'DELETE',
    success: function(response) {
      $('#recent-scrobble-' + id).transition({
        animation: 'scale',
        onComplete: function() {
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
        this.artist + ' - ' + this.track + ' [' + this.album + ']' +
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
    $("#userstats").html(html);
  });
};

$(document).ready(function() {
  get_recent_scrobbles();
  get_user_stats();
});
