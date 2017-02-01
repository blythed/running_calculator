var weights_arr;
var w = 600;
var h = 600;

d3.csv("weights.csv", function(data) {

    dataset=data;
//    console.log(dataset);

    var svg = d3.select("body")
        .append("svg")
        .attr("width", w)
        .attr("height", h);

    var circles = svg.selectAll("circle")
         .data(dataset)
         .enter()
         .append("circle");
    console.log(circles);

    var xscale = d3.scale.linear()
        .domain([-0.01873,-0.01702])
        .range([0,600])

    var yscale = d3.scale.linear()
        .domain([-0.0672,0.0509])
        .range([0,600])

    var zscale = d3.scale.linear()
        .domain([-0.0615,0.1085])
        .range([.1,5])

    var colours = ["#6363FF", "#6373FF", "#63A3FF", "#63E3FF", "#63FFFB", "#63FFCB",
   "#63FF9B", "#63FF6B", "#7BFF63", "#BBFF63", "#DBFF63", "#FBFF63", 
   "#FFD363", "#FFB363", "#FF8363", "#FF7363", "#FF6364"];

    var heatmapColour = d3.scale.linear()
        .domain(d3.range(5.64, 9.58, (9.58-5.64) / (colours.length - 1)))
        .range(colours);

    circles.attr("cx", function(d) {
        return xscale(d.w1)
    })
        .attr("cy", function(d) {
        return yscale(d.w2)
    })
        .attr("r", function(d) {
        return zscale(d.w3)
    })
        .attr("fill", function(d) {
        return heatmapColour(d.spec)
    });

    
    var xAxis = d3.svg.axis(); 
    xAxis.scale(xscale);
    xAxis.orient("bottom");

    svg.append("g")
        .call(d3.svg.axis()
        .scale(xscale)
        .orient("bottom"));

    personal_circle = svg.append("circle")
        .attr("cx", 300)
        .attr("cy", 150) 
        .style("fill", "none")   
        .style("stroke", "black") 
        .attr("r", 25);

});

function showValue(newValue){
    document.getElementById("range").innerHTML=newValue;
    personal_circle.attr("r",newValue)
};
