function CimEarthInputs() {
  var data_selects = document.getElementsByClassName('data_select'),
    run_graph = document.getElementById('run_graph')
  ;
  function compile_data(redraw) {
    var opts = '',
      inputs = $('input[type=checkbox]:checked'),
      checks = [],
      axis = {item: false, minor: false, major: false};
    inputs.each(function() {
      checks.push($(this).val());
      axis[$(this).attr('name')] = checks;
    });
    $('select').each(function() {
      var obj = $(this);
      axis[obj.attr('id')] = obj.val();
      $('h2 span').eq(obj.index()+2).html(obj.children('option:selected').html());
    });
    if (redraw) {
      line_graph.redraw(Options.data_set, Options.data_table, axis);
    }
    for (i=0;i<inputs.length;++i) {
      opts += $(inputs[i]).next('label').html() + ', '
    }
    $('h3').html(opts.slice(0,-2));
  }
  d3.selectAll(data_selects)
    .on('change', function() {
      compile_data(true);
    });
  $('input[type=checkbox]').change(function() {
    compile_data(true);
  })
  this.draw_initial = function() {
    compile_data(false);
  }
}
var inputs = new CimEarthInputs();
inputs.draw_initial();