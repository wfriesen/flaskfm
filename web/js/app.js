function get_recent_tracks_html(data) {
  var html = '';
  $.each(data.scrobbles, function(index, item) {
    html += '<div clas="item">' + this.artist + ' - ' + this.album + ' - ' + this.track + ' (' + $.timeago(Date.parse(this.timestamp)) + ')' + '</div>';
  });
  return html;
};

$(document).ready(function() {
  $.get("http://localhost:5000/flaskfm/api/v0.1/recent", function(data) {
    $("#recentscrobbles").html(get_recent_tracks_html(data));
  });
});
