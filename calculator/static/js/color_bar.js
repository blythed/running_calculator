function drawKey(min, max, left, width, height) {
    var colorRange = ["#6363FF", "#6373FF", "#63A3FF", "#63E3FF", "#63FFFB", "#63FFCB",
                   "#63FF9B", "#63FF6B", "#7BFF63", "#BBFF63", "#DBFF63", "#FBFF63", 
                   "#FFD363", "#FFB363", "#FF8363", "#FF7363", "#FF6364"];

   var color = d3.scale.linear()
        .domain(d3.range(5.64, 9.58, (9.58-5.64) / (colorRange.length - 1)))
        .range(colorRange);

      x = d3.scale.linear()
        .domain([min, max])
        .range([0, width])

  var notches = d3.range(5.64, 9.58 + (9.58-5.64) / (colorRange.length - 1), (9.58-5.64) / (colorRange.length - 1))

  var x = d3.scale.linear()
    .domain([min, max])
    .range([0, width])

  var svg = d3.select('#visualB')

  // SVG defs
  var defs = svg
    .datum(notches)
    .append('svg:defs')

  // Gradient defs
  for (i=0;i<notches.length-1;i++) {
      var gradient = defs.append('svg:linearGradient')
        .attr('id', 'gradient'+i.toString())
      // Gradient stop 1
      gradient.append('svg:stop')
        .datum(notches[i])
        .attr('stop-color', function(d) { return color(d) })
        .attr('offset', '0%')
      // Gradient stop 2
      gradient.append('svg:stop')
        .datum(notches[i+1])
        .attr('stop-color', function(d) { return color(d) })
        .attr('offset', '100%')
      svg
        .datum([notches[i],notches[i+1]])
        .append('svg:rect')
          .attr('id', 'gradient'+i.toString()+'-bar')
          .attr('fill', 'url(#gradient'+i.toString()+')')
          .attr('transform', function(d) { 
            return 'translate(' + (left + x(d[0])) + ',0)'
            })
          .attr('width', function(d) { return x(d[1])-x(d[0]) })
          .attr('height', height)
  }

  color_scale = d3.scale.log().domain([282,14525]).range([0,width])

  // Append axis
  var axis = d3.svg.axis()
      .scale(color_scale)
      .tickFormat(d3.format('g'))
      .tickValues([400,1000,5000,10000])

  svg.append('g').attr('class', 'axis')

  svg.selectAll('.axis')
    .attr('transform', 'translate('+(left)+','+(height)+')')
    .call(axis)
}
