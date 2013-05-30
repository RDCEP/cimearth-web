function CimEarthLineGraph() {
  /*
   Set up initial variables
   ------------------------
   General layout
   */
  var margin = {top: 0, right: 0, bottom: 0, left: 0},
    padding = {top: 20, right: 20, bottom: 60, left: 80},
    outer_width = 750,
    outer_height = 500,
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
    tooltip = d3.select('#wrapper').append('div').attr('id', 'tooltip'),
    graph,
    color,
    dots_layers,
    dots,
    paths,
    points,
    segments,
    y_grid,
    x_axis,
    y_axis,
    color_map = []
  ;
  /*
   End variables
   */
  d3.selectAll('input[name='+Options.check_axis+']')
    .each(function() {
      color_map.push(d3.select(this).attr('value'));
    });
  function flat_data(d, o) {
    /*
     Combine datum, region, and index into one object for rollover circles
     */
    _d = [];
    for (i=0; i<d.length; ++i) {
      _d.push({data: d[i], item: o.item, minor: o.minor});
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


  function draw_axes(data) {
    /*
     Redraw graph axes. Called from draw() and redraw().
     */
    y.domain(get_domain(data));
    x_axis.transition()
      .call(x_axis_ticks);
    y_axis.transition()
      .call(y_axis_ticks
        .tickFormat(d3.format('.2f'))
    );
    y_grid.transition()
      .call(y_axis_ticks
        .tickSize(-width, 0, 0)
        .tickFormat('')
    );
  }


  function get_color(d) {
    var color_list = [
      //d3.rgb(0, 0, 0),      // black
      d3.rgb(230, 159, 0),  // orange
      d3.rgb(86, 180, 233), // sky blue
      d3.rgb(0, 158, 115),  // bluish green
      d3.rgb(240, 228, 66), // yellow
      d3.rgb(0, 114, 178),  // blue
      d3.rgb(213, 94, 0),   // vermilion
      d3.rgb(204, 121, 167) // reddish purple
    ];
    color = d3.scale.ordinal()
      .domain(color_map)
      .range(color_list);
    return color(d[Options.check_axis])
      .darker(
        Math.floor(color_map.indexOf(d[Options.checks])/(color_list.length*2)) *.5
      );
  }


  function get_stroke(d) {
    /*
     Alternates between solid and dashed lines
     */
    if (Math.floor(color_map.indexOf(d[Options.check_axis])/7) % 2 == 1) {
      return '2,5';
    }
    return 'none';
  }


  function draw(data) {
    points = d3.max(data, function(d, i) {
      return d.data.length;
    });
    paths = graph.selectAll('.output-path')
      .data(data, function(d) {return data.indexOf(d);});
    paths.exit().transition()
      .remove();
    paths.enter()
      .append('path');
    paths.transition()
      .attr('d', function(d, i) { return line(d.data); })
      .attr('class', 'output-path')
      .style('stroke', function(d) { return get_color(d);})
      .style('stroke-linecap', 'round')
      .style('stroke-dasharray', function(d) {
        return get_stroke(d);
      });
    dots_layer.selectAll('.dot-layer').remove();
    dots_layers = dots_layer.selectAll('.dot-layer')
      .data(data)
      .enter()
      .append('g')
      .attr('class', 'dot-layer');
    dots_layers.selectAll('.dot').remove();
    dots = dots_layers.selectAll('.dot')
      .data(function(d, i) {return flat_data(d.data, d); });
    dots.exit().remove();
    dots.enter()
      .append('circle')
      .attr('r', 5)
      .attr('cx', function(d, i) { return x(i+start_year);})
      .attr('cy', function(d) { return y(d.data);})
      .attr('class', function(d, i) {
        return 'dot-' + i + ' dot-' + d.region + ' dot';
      });
  }
  this.redraw = function(data_set, data_table, axis) {
    /*
     Update graphs on <select> changes.
     */
    var url = 'http://cimearth.obstructures.org/json/'+data_set+'/'+data_table+'/'+axis.item+'/'+axis.minor;
    if (axis.major) {
      url += '/'+axis.major;
    }
    $.ajax({
      dataType: 'json',
      url: url,
      success: function(data) {
        draw_axes(data);
        draw(data);
      }
    });
  };
  this.build = function(url) {
    /*
     Draws initial graph on page load. Builds hover effects.
     */
    d3.json(url, function(error, data) {
      y_axis = svg.append('g')
        .attr('class', 'y axis')
        .attr('transform', 'translate(-20,0)');
      y_grid = svg.append('g')
        .attr('id', 'y_grid')
        .attr('class', 'grid');
      x_axis = svg.append("g")
        .attr('class', 'x axis')
        .attr('transform', 'translate(0,' + (height+20) + ')');
      graph = svg
        .append('g')
        .attr('class', 'output-area');
      dots_layer = svg
        .append('g')
        .attr('class', 'all-dots');
      draw_axes(data);
      draw(data);
      segments = svg.append('g')
        .attr('class', 'segments')
        .selectAll('.data-region')
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
          tooltip.html('');
          var tdots = d3.selectAll('.dot-'+i)
            .style('stroke', function(dd, ii) {
              return get_color(dd);})
            .style('fill', '#eee')
            .classed('visible', true)
            .sort(function(a, b) {
              return d3.descending(a.data, b.data);
            })
            .each(function(dd) {
//              console.log(dd);
              var _h = '<b style="color:' + get_color(dd) + '">';
              _h += dd[Options.check_axis] + '</b>: '+ dd.data + '<br>';
              tooltip
                .html(tooltip.html() + _h);
            });
          tooltip
            .style('left', (i * width / (points - 1) + padding.left + (width / (points - 1) / 2)) + 'px')
            .style('bottom', (height - d3.select(tdots[0][0]).attr('cy') + padding.bottom + 10) + 'px')
            .style('opacity', .8);
        })
        .on('mouseout', function(d, i) {
          d3.selectAll('.dot-'+i)
            .style('stroke', 'none')
            .style('fill', 'none')
            .classed('visible', false);
            tooltip.html('')
            .style('opacity', 0);
        });
      segments.append('g')
        .attr('transform', 'translate('+width / (points - 1)/2+', 0)')
        .attr('class', 'grid-roll')
        .append('line')
        .attr('x2', 0)
        .attr('y2', -height);
    });
  };
}
/*
 Instantiate graph and draw on page load.
 */
var line_graph = new CimEarthLineGraph();
var url = 'http://cimearth.obstructures.org/json/';
url += Options.data_set + '/' + Options.data_table + '/';
url += Options.item_code + '/' + Options.minor_code;
if (Options.major_code) {
  url += '/' + Options.major_code;
}
line_graph.build(url);