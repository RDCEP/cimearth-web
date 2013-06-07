$(document).ajaxStart(function() {
  var _aj = $('<img id="ajax-loader" src="/static/images/ajax-loader.gif">');
  $('h2').append(_aj);
});
$(document).ajaxComplete(function() {
  $('#ajax-loader').remove();
});
