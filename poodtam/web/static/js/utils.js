// initial dropdown function
$('.ui.dropdown').dropdown();

// initial sidebar
$(document).ready(function () {
  $('.left.sidebar.menu').sidebar('attach events', '.launch.right.attached.fixed.button', 'show');
});

$("input:text").click(function () {
  $(this).parent().find("input:file").click();
});

$('input:file', '.ui.action.input')
  .on('change', function (e) {
    var name = e.target.files[0].name;
    $('input:text', $(e.target).parent()).val(name);
  });