function CimEarthLineGraph() {
  /*
   Set up initial variables
   ------------------------
   General layout
   */
  var margin = {top: 0, right: 0, bottom: 0, left: 0},
    padding = {top: 10, right: 20, bottom: 20, left: 30},
    outer_width = 500,
    outer_height = 300,
    inner_width = outer_width - margin.left - margin.right,
    inner_height = outer_height - margin.top - margin.bottom,
    width = inner_width - padding.left - padding.right,
    height = inner_height - padding.top - padding.bottom,
    offset = 0
  ;
  /*
   Data domain
   */
  var start_year = 2004, end_year = 2024,
    min_d, max_d, min_domain, max_domain,
    x = d3.scale.linear().domain([start_year, end_year]).range([0, width]),
    y = d3.scale.linear().domain([1, 0]).range([0, height])
  ;
  /*
   Graph entities
   */
  var svg = d3.select("#graph").append("svg")
      .attr("width", width + padding.left + padding.right)
      .attr("height", height + padding.top + padding.bottom)
      .append('g')
      .attr("transform", "translate(" + padding.left + "," + padding.top + ")"),
    line = d3.svg.line()
      .x(function(d, i) { return x(i+start_year); })
      .y(function(d) { return y(d-offset); }),
    x_axis_ticks = d3.svg.axis()
      .scale(x)
      .orient('bottom')
      .tickSize(1)
      .tickPadding(5)
      .tickFormat(d3.format('C')),
    y_axis_ticks = d3.svg.axis()
      .scale(y)
      .tickSize(1)
      .tickPadding(5)
      .orient('left'),
    tooltip = d3.select('body').append('div').attr('id', 'tooltip'),
    regions,
    color,
    dots_layers,
    paths,
    dots,
    points
  ;
  /*
   End variables
   */
  function flat_data(d, r, _i) {
    /*
     Combine datum, region, and index into one object for rollover circles
     */
    _d = [];
    for (i=0; i<d.length; ++i) {
      _d.push({data: d[i], region: r, color: _i});
    }
    return _d;
  }
  function get_domain(data) {
    /*
     Update y domain based on updated data min and max
     */
    min_d = d3.min(data, function(d) { return d3.min(d.data); });
    max_d = d3.max(data, function(d) { return d3.max(d.data); });
    max_domain = max_d + ((max_d - min_d) / 10);
    min_domain = min_d - ((max_d - min_d) / 10);
    return [max_domain, min_domain];
  }
  this.redraw = function(dt, r1, r2, c1) {
    /*
     Update graphs on <select> changes.
     */
    $.ajax({
      dataType: 'json',
      url: 'http://cimearth.obstructures.org/json/'+dt+'/'+r1+'/'+r2+'/'+c1,
      success: function(data) {
        points = d3.max(data, function(d, i) {
          return d.data.length;
        })
        color = d3.scale.category10()
          .domain(d3.keys(data).filter(function(key) { return key === "region"; }));
        y.domain(get_domain(data));
        draw_axes();
        regions.data(data);
        paths.data(data)
          .transition()
          .duration(200)
          .attr("d", function(d) {return line(d.data)})
          .style("stroke", function(d, i) { return color(i); })
        ;
        dots_layers.data(data);
        dots.data(function(d, i) { return flat_data(d.data, d.region, i); })
          .attr('cx', function(d, i) { return x(i+start_year); })
          .attr('cy', function(d) { return y(d.data); })
          .attr('class', function(d, i) {
            return 'dot-' + i;
          })
          .classed('dot', true)
        ;
      }
    });
  };
  this.draw = function() {
    /*
     Draws initial graph on page load. Builds hover effects.
     */
    d3.json('http://cimearth.obstructures.org/json/price/USA/MEX/OIL/', function(error, data) {
      points = d3.max(data, function(d, i) {
          return d.data.length;
      })
      color = d3.scale.category10()
        .domain(d3.keys(data).filter(function(key) { return key === "region"; }));
      y.domain(get_domain(data));
      draw_axes();
      regions = svg.selectAll('regions')
        .data(data)
        .enter()
        .append('g');
      paths = regions
        .append('path')
        .attr("d", function(d) {return line(d.data)})
        .style('stroke-width', 2)
        .classed('output-path', true)
        .style("stroke", function(d, i) { return color(i); })
      ;
      dots_layers = regions
        .append('g')
        .attr('class', function(d) { return d.region; });
      dots = dots_layers.selectAll('.dot')
        .data(function(d, i) { return flat_data(d.data, d.region, i); })
        .enter()
        .append('circle')
        .attr('r', 5)
        .attr('cx', function(d, i) { return x(i+start_year);})
        .attr('cy', function(d) { return y(d.data);})
        .attr('class', function(d, i) {
          return 'dot-' + i;
        })
        .classed('dot', true)
      ;
      svg.selectAll('.data-region')
        .data(data[0].data)
        .enter()
        .append('rect')
        .style('fill', 'none')
        .style('pointer-events', 'all')
        .attr('width', width / (points - 1))
        .attr('height', height)
        .attr('x', function(d, i) {
          return (i * width / (points - 1)) - (width / (points - 1) / 2);
        })
        .attr('y', 0)
        .on('mouseover', function(d, i) {
          d3.selectAll('.dot-'+i)
            .style('fill', function(dd, ii) { return color(dd.color); })
            .classed('visible', true)
            .sort(function(a, b) {
              return d3.descending(a.data, b.data);
            })
            .each(function(dd) {
              var _h = '<b style="color:' + color(dd.color) + '">';
              _h += dd.region + '</b>: '+ dd.data + '<br>';
              tooltip
                .html(tooltip.html() + _h);
            });
            tooltip
              .style('left', (d3.event.pageX + 10) + 'px')
              .style('top', (d3.event.pageY - 48) + 'px')
              .style('opacity', .8);
        })
      .on('mouseout', function(d, i) {
          d3.selectAll('.dot-'+i)
            .style('fill', 'none')
            .classed('visible', false);
            tooltip.html('')
            .style('opacity', 0);
        });
    });
  };
  function draw_axes() {
    /*
     Draw graph axes. Called from draw() and redraw().
     */
    svg.selectAll('.axis').remove();
    svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(x_axis_ticks);
    svg.append("g")
      .attr("class", "y axis")
      .call(y_axis_ticks);
  }
}
/*
 Instantiate graph and draw on page load.
 */
var line_graph = new CimEarthLineGraph();
line_graph.draw();
