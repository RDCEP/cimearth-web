function CimEarthInputs() {
  var data_selects = document.getElementsByClassName('data_select'),
    run_graph = document.getElementById('run_graph')
  ;
  function compile_data() {
    var _c1 = document.getElementById('commodity'),
      _r1 = document.getElementById('region'),
      _cs = [],
      _rs = [];
    $('input[type=checkbox]:checked').each(function() {
      if (_c1) {_rs.push($(this).val());}
      else {_cs.push($(this).val())}
    });
    if (_c1) {_cs = _c1.value;}
    else {_rs = _r1.value;}
    line_graph.redraw(Options.dtype, _rs, _cs);
    $('h2 span').html($('#'+$(this).attr('class')+' option:selected').html());
    var opts = '',
      inputs = $('input[name='+Options.cmap+']:checked');
    for (i=0;i<inputs.length;++i) {
      opts += $(inputs[i]).next('label').html() + ', '
    }
    $('h3').html(opts.slice(0,-2));
  }
  d3.selectAll(data_selects)
    .on('change', function() {
      var _v = this.value;
      $(this).siblings().children('option').prop('disabled', false);
      $(this).siblings().children('option[value='+_v+']').prop('disabled', true);

      compile_data();
    });
  $('input[type=checkbox]').change(function() {
    compile_data();
  })
}
inputs = CimEarthInputs();
