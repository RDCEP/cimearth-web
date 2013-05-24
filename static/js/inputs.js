function CimEarthInputs() {
  var data_selects = document.getElementsByClassName('data_select'),
    run_graph = document.getElementById('run_graph')
  ;
  d3.selectAll(data_selects)
    .on('change', function() {
      var _v = this.value;
      $(this).siblings().children('option').prop('disabled', false);
      $(this).siblings().children('option[value='+_v+']').prop('disabled', true);
      _dt = document.getElementById('data_type').value;
      _r1 = document.getElementById('region1').value;
      _r2 = document.getElementById('region2').value;
      _c1 = document.getElementById('commodity1').value;
      line_graph.redraw(_dt, _r1, _r2, _c1);
    });
  d3.select(run_graph)
    .on('click', function() {
      _dt = document.getElementById('data_type').value;
      _r1 = document.getElementById('region1').value;
      _r2 = document.getElementById('region2').value;
      _c1 = document.getElementById('commodity1').value;
      line_graph.redraw(_dt, _r1, _r2, _c1);
    });
}
inputs = CimEarthInputs();
