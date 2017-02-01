$(document).ready(function() {

    distances = ['100m','200m','400m','800m','1500m','Mile','5k','10k', 'HM', 'Mar'];
    function checkIfArrayIsUnique(myArray) {
        return myArray.length === new Set(myArray).size;
    }

    function count_objects(arr) {
        var counts = {};
        for(var i = 0; i< arr.length; i++) {
            var num = arr[i];
            counts[num] = counts[num] ? counts[num]+1 : 1;
        }
        return Object.keys(counts).length
    }

    console.log(count_objects([1,2,2,2]))
    root = 'http://127.0.0.1:8000/'

    $("#predict_button").click(function (e) { 
        e.preventDefault(); 
        var svg = d3.select("#visualA")
        svg.selectAll("*").remove();
        var svg = d3.select("#visualB")
        svg.selectAll("*").remove();
        $("#prediction").text("Calculating result..."); 
        var callback = function (data) { 
            data = data.split(',')
            $("#prediction").html("<font size='6'>"+data[0]+"</font><br><font size='3'>"+data[1]+"</font>");
        }   
        var dp = $("#id_to_predict").val().concat("/")
        var g = $("#id_first_name").val().concat("/")

        try {
            var t1 = $("#id_form-0-url").val().concat("/")
            var dd1 = $("#id_form-0-anchor").val().concat("/")
            try {
                var t2 = $("#id_form-1-url").val().concat("/")
                var dd2 = $("#id_form-1-anchor").val().concat("/")
            }
            catch(err) {
                var t2 = '0/'
                var dd2 = 'None/'
                var t3 = '0/'
                var dd3 = 'None/'
                var distt = [dp,dd1]
            }

            try {
                var t3 = $("#id_form-2-url").val().concat("/")
                var dd3 = $("#id_form-2-anchor").val().concat("/")
                var distt = [dp,dd1,dd2,dd3]
            }
            catch(err) {
                var t3 = '0/'
                var dd3 = 'None/'
                var distt = [dp,dd1,dd2]
            }

            if ($('#id_form-3-anchor').length>0) {
                throw "too_many"
            }

            if (checkIfArrayIsUnique(distt)) { 
                console.log('unique')
            }
            else {
                throw "unique"
                console.log('not unique')
            }

            var url = "calculateresult/".concat(dp,g,dd1,t1,dd2,t2,dd3,t3)
            $.get(url, [], callback);
        }
        catch(err) {
            if (err=='unique') {
                $('#prediction').html('distances must all be distinct')
            }
            else {
                if (err=='too_many') {
                    $('#prediction').html('At most 3 distances may be specified')
                }
                else {
                    $('#prediction').html('At least one prior attempt required') 
                }
            }
        }
            

    }); 

    $("#tns_button").click(function (e) { 
        try {
            e.preventDefault(); 
            $("#prediction").html("Calculating Result...");

            var def = ['0','0','0','0','0','0','0','0','0','0'];
            var i = 0;
            var stem = "id_form-";
            while (true) {
                var name = stem.concat(i.toString(),"-anchor");
                var time = stem.concat(i.toString(),"-url");
                if($("#" + name).length == 0) {
                    break;
                }    
                var eve = $("#" + name).val();
                var t = $("#" + time).val();
                if (t=='') {
                    throw "empty"
                }
                def[eve] = t;
                i++;
            }
            if (i>count_objects(def)-1) {
                throw "unique"
            }
            if ($('#id_form-1-anchor').length==0) {
                throw "insufficient"
            }
            if ($('#id_form-2-anchor').length==0) {
                throw "insufficient"
            }
            

            strz = def.join('/');
            urlz = "threenumbersummary/".concat(strz);

            var x;
            var v1 = [-0.12908975, -0.16466912, -0.20474848, -0.24656139, -0.28428027, -0.28921643, -0.35394203, -0.39203391, -0.43267206, -0.47209468];
            var v2 = [ 0.44729982,  0.47206714,  0.52648191,  0.30452078,  0.07975834, 0.08055933, -0.15965357, -0.19827593, -0.22793142, -0.2784831 ];
            var v3 = [-0.1749561 , -0.20042658, -0.11452939,  0.22240156,  0.32629829, 0.30918102,  0.31568395,  0.27168964, -0.11531519, -0.69123616];


            $.get(urlz, [], function (data) {
                x = data;
                var splitted = x.split('<br>');
                var table = '<table cellpadding="5"><tr>'
                for (i = 0; i < 10; i++) {
                    table = table+'<td>'+distances[i]+'</td>'
                }
                table = table+'</tr><tr>'
                var times = splitted[1].split(',')
                for (i = 0; i < 10; i++) {
                    table = table+'<td id="record_time_'+i.toString()+'">'+times[i]+'</td>'
                }
                table = table+'</tr><table>'
                $("#prediction").html(table);
                if (splitted[0]!='err') {
                    var dat = JSON.parse(splitted[0]);

                    var weights_arr;
                    var w = 600;
                    var h = 600;
                                

                    d3.csv(root+"weights.csv", function(data) {

                        dataset=data;
                    //    console.log(dataset);

                        var svg = d3.select("#visualB")

                        var circles = svg.selectAll("circle")
                             .data(dataset)
                             .enter()
                             .append("circle");

                        console.log(circles);
                        
                        padding = 50;

                        var xscale = d3.scale.linear()
                            .domain([-20.81,-18.90])
                            .range([padding,600-padding])

                        var yscale = d3.scale.linear()
                            .domain([-0.517,0.39])
                            .range([600-padding,padding])

                        var zscale = d3.scale.linear()
                            .domain([-0.285,0.51])
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
                            .attr("transform", "translate(0," + (w - padding) + ")")
                            .call(xAxis)

                        var yAxis = d3.svg.axis()
                                    .scale(yscale)
                                    .orient("left")

                        svg.append("g")
                            .attr("transform", "translate("+ padding + ",0)")
                            .call(yAxis);

                        svg.append('text').attr('x',35).attr('y',33).text('SV2')
                        svg.append('text').attr('x',530).attr('y',540).text('SV1')

                        drawKey(5.64,9.58,100,400,20);

                        svg.append('text').attr('x',270).attr('y',45).text('specialization [m]')
                        svg.append('text').attr('x',450).attr('y',500).text('Size of marker = SV3')


                    });

                    times = splitted[1].split(',')

                    var svg = d3.select("#visualA")
                    svg.selectAll("*").remove();
                    
                    var padding = 50;

                    var xscale = d3.scale.log()
                        .domain([50,43000])
                        .range([padding,w-padding])

                    var yscale = d3.scale.log()
                        .domain([3,10])
                        .range([h-padding,padding])

                    var xscale2 = d3.scale.linear()
                        .domain([-20.81,-18.90])
                        .range([padding,w-padding])

                    var yscale2 = d3.scale.linear()
                        .domain([-0.517,0.39])
                        .range([h-padding,padding])

                    var zscale2 = d3.scale.linear()
                        .domain([-0.285,0.51])
                        .range([.3,15])

                    var height_to_speed = function (f) {
                        return yscale.invert(f);
                    };

                    var three_number_summary = function (time_x) {
                        var w1 = 0;
                        var w2 = 0;
                        var w3 = 0;
                        for (i = 0; i < 10; i++) {
                            w1 = w1 + Math.log(time_x[i])*v1[i];
                            w2 = w2 + Math.log(time_x[i])*v2[i];
                            w3 = w3 + Math.log(time_x[i])*v3[i];
                        }
                        return [w1,w2,w3];
                    }

                    var denoised_curve = function(time_x) {
                        var TNZ = three_number_summary(time_x);
                        curve = [0,0,0,0,0,0,0,0,0,0];
                        for (i = 0; i < 10; i++) { 
                            curve[i] = dat[i][1]/Math.exp(v1[i]*TNZ[0]+v2[i]*TNZ[1]+v3[i]*TNZ[2]);
                        }
                        return curve;
                    }

                    var line = d3.svg.line()
                        .x(function(d) { 
                            return xscale(d[0])
                        })
                        .y(function(d) { 
                            return yscale(d[1]); 
                        })

                    var xAxis = d3.svg.axis();
                    xAxis.scale(xscale);
                    xAxis.orient("bottom");
                    xAxis.tickValues([100,1000,10000]);

                    svg.append("g")
                        .attr("transform", "translate(0," + (h - padding) + ")")
                        .call(xAxis);

                    var yAxis = d3.svg.axis()
                                    .scale(yscale)
                                    .orient("left")

                    svg.append("g")
                        .attr("transform", "translate("+ padding + ",0)")
                        .call(yAxis);

                    svg.append('text').attr('x',1).attr('y',30).text('average speed [m/s]')
                    svg.append('text').attr('x',530).attr('y',540).text('distance [m]')

                    svg.append('text').attr('x',400).attr('y',40).text('Drag the points to')
                    svg.append('text').attr('x',400).attr('y',50).text('observe effect on ')
                    svg.append('text').attr('x',400).attr('y',60).text('three number summary')

                    var get_times = function () {
                        var timez = [];
                        for (i = 0; i < 10; i++) {
                            timez.push(dat[i][1]/yscale.invert(parseFloat(d3.select('#point_'+i.toString()).attr('cy'))));
                        }
                        return timez;
                    }

                    var drag = d3.behavior.drag()  
                        .on('dragstart', function() { circles.style('fill', 'red'); })
                        .on('drag', function() { d3.select(this).attr('cy', d3.event.y); 
                            // update time according to point
                            var a = d3.select(this).attr('id');
                            var number = a.split('_')[1];
                            var integer = parseInt(number);
                            var dist = d3.select('#distance_label_'.concat(number));
                            dist.attr('y',d3.event.y-40);
                            var tim = d3.select('#time_label_'.concat(number));
                            tim.attr('y',d3.event.y-20);
                            var speed = height_to_speed(d3.event.y);
                            var distance = dat[number][1];
                            var seconds = distance/speed;
                            var strz = moment().startOf('day')
                                .seconds(seconds)
                                .format('H:mm:ss.SS');
                            var seconds = seconds.toString()
                            seconds = seconds.split('.')
                            var micro = seconds[1].substr(0,2);
                            var full_seconds = strz.substr(0,8);
                            tim.text(full_seconds+micro);
                            var tab_el = d3.select('#record_time_'+number)
                            tab_el.html(full_seconds+micro)
                            var all_timez = get_times();
                            var pc = d3.select('#personal_circle');
                            var pt = d3.select('#personal_text');
                            var tns = three_number_summary(all_timez);
                            var tns_tab = d3.select('#tns_0').html(tns[0].toString().substr(0,7))
                            var tns_tab = d3.select('#tns_1').html(tns[1].toString().substr(0,7))
                            var tns_tab = d3.select('#tns_2').html(tns[2].toString().substr(0,7))
                            pc.attr('cy',yscale2(tns[1]));
                            pc.attr('cx',xscale2(tns[0]));
                            pc.attr('r',zscale2(tns[2]));
                            pt.attr('y',yscale2(tns[1]));
                            pt.attr('x',xscale2(tns[0])+12);
                            var curve = denoised_curve(all_timez);
                            var data_aug = [
                                        [dat[0][1],curve[0]],
                                        [dat[1][1],curve[1]],
                                        [dat[2][1],curve[2]],
                                        [dat[3][1],curve[3]],
                                        [dat[4][1],curve[4]],
                                        [dat[5][1],curve[5]],
                                        [dat[6][1],curve[6]],
                                        [dat[7][1],curve[7]],
                                        [dat[8][1],curve[8]],
                                        [dat[9][1],curve[9]],
                                        ]
                            var pathz = d3.select('#denoised_curve')
                            pathz.attr('d',line(data_aug))
                        })
                        .on('dragend', function() { circles.style('fill', 'red'); });

                    var circles = svg.selectAll('.draggableCircle')  
                        .data(dat)
                        .enter()
                        .append('svg:circle')
                        .attr('class', 'draggableCircle')
                        .attr('cx', function(d) { return xscale(d[1]); })
                        .attr('cy', function(d) { return yscale(d[0]); })
                        .attr('r', function(d) { return 10; })
                        .attr('id',function(d,i) { return 'point_'.concat(i.toString());})
                        .call(drag)
                        .style('fill', 'red');

                    dstem = 'distance_label_'
                    for (i = 0; i < 10; i++) { 
                        var test = svg.append('text')
                            .text(distances[i])
                            .attr('x',xscale(dat[i][1]))
                            .attr('y',yscale(dat[i][0])-40)
                            .attr('id',dstem.concat(i.toString()));
                        var test = svg.append('text')
                            .text(times[i])
                            .attr('x',xscale(dat[i][1]))
                            .attr('y',yscale(dat[i][0])-20)
                            .attr('id','time_label_'.concat(i.toString()));
                    }

                    var scat = d3.select("#visualB")
                    scat.selectAll("*").remove();
                    
                    var sp = get_times()
                    console.log(sp)
                    
                    var TNS = three_number_summary(sp)
                    console.log(TNS)
                    
                    var tab_tns = '<table><tr><td>SV1</td><td>SV2</td><td>SV3</td></tr>'
                    tab_tns = tab_tns.concat('<tr><td id="tns_0">'+TNS[0].toString().substr(0,7)+'</td><td id="tns_1">'+TNS[1].toString().substr(0,7)+'</td><td id="tns_2">'+TNS[2].toString().substr(0,7)+'</td></tr></table>')
                    var tab = d3.select('#prediction').append("table")
                    tab.html(tab_tns)
                    
                    var curve = denoised_curve(sp);
                    console.log(curve)

                    personal_circle = scat.append("circle")
                        .attr("cx", xscale2(TNS[0]))
                        .attr("cy", yscale2(TNS[1])) 
                        .style("fill", "black")   
                        .style("stroke", "black") 
                        .attr("id",'personal_circle')
                        .attr("r", zscale2(TNS[2]));
                

                    var personal_text = scat.append('text')
                        .text("Athlete")
                        .attr('x',xscale2(TNS[0])+12)
                        .attr('y',yscale2(TNS[1]))
                        .attr('id','personal_text')


                    var data_aug = [
                                [dat[0][1],curve[0]],
                                [dat[1][1],curve[1]],
                                [dat[2][1],curve[2]],
                                [dat[3][1],curve[3]],
                                [dat[4][1],curve[4]],
                                [dat[5][1],curve[5]],
                                [dat[6][1],curve[6]],
                                [dat[7][1],curve[7]],
                                [dat[8][1],curve[8]],
                                [dat[9][1],curve[9]],
                                ]

                    svg.append('svg:path')
                       .attr('d', line(data_aug))
                       .attr('stroke', 'black')
                       .attr('stroke-width', 2)
                       .attr('fill', 'none')
                       .attr('id','denoised_curve');
                    console.log(dat)
                }
            });
        }
        catch(err) {
            if (err=="unique") {
                $('#prediction').html('All events must be distinct')
            }
            console.log(err)
            if (err=="empty") {
                $('#prediction').html('Specify the time in the right hand box')
            }
            if (err=="insufficient") {
                $('#prediction').html('At least three events required for three number summary')
            }
        }
    }); 
});

