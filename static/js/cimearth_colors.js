var colors = d3.scale.ordinal()
.domain(d3.range(8))
.range([
    d3.rgb(0, 0, 0),      // black
    d3.rgb(230, 159, 0),  // orange
    d3.rgb(86, 180, 233), // sky blue
    d3.rgb(0, 158, 115),  // bluish green
    d3.rgb(240, 228, 66), // yellow
    d3.rgb(0, 114, 178),  // blue
    d3.rgb(213, 94, 0),   // vermilion
    d3.rgb(204, 121, 167) // reddish purple
  ])