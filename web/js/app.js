function get_recent_scrobbles() {
  $.get("http://localhost:5000/flaskfm/api/v0.1/recent", function(data) {
    var html = '';
    $.each(data.scrobbles, function(index, item) {
      console.log(this.timestamp);
      html +=
        '<div class="item">' +
        this.artist + ' - ' + this.track + ' [' + this.album + ']' +
        '<span title="' + this.timestamp + '"> (' + this.human_timestamp + ')</span>' +
        '</div>';
    });
    $("#recentscrobbles").html(html);
  });
};

$(document).ready(function() {
  get_recent_scrobbles();
});
