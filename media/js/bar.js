function svgBarChart(){
    var data = [4, 8, 15, 16, 23, 42];
    var chart = d3.select("div#svg").append("svg")
    .attr("class", "chart")
    .attr("width", 440)
    .attr("height", 140)
    .append("g")
    .attr("transform", "translate(10,15)");//设置位移俩 可以在条形统计图上右键--审查元素。看看是实际效果
    
    
    
    var x = d3.scale.linear()
    .domain([0, d3.max(data)])
    .range([0, 420]);
    
    var y = d3.scale.ordinal()
    .domain(data)
    .rangeBands([0, 120]);
      
    chart.selectAll("rect")
    .data(data)
    .enter().append("rect")
    .attr("y", y)
    .attr("width", x)
    .attr("height", y.rangeBand());
    
    
    chart.selectAll("text")
    .data(data)
    .enter().append("text")
    .attr("x", x)
    .attr("y", function(d) { return y(d) + y.rangeBand() / 2; })
    .attr("dx", -3) // padding-right
    .attr("dy", ".35em") // vertical-align: middle
    .attr("text-anchor", "end") // text-align: right
    .text(String);
    
    
    chart.selectAll("line")
    .data(x.ticks(10))
    .enter().append("line")
    .attr("x1", x)
    .attr("x2", x)
    .attr("y1", 0)
    .attr("y2", 120)
    .style("stroke", "#ccc");
    
    chart.selectAll(".rule")
    .data(x.ticks(10))
    .enter().append("text")
    .attr("class", "rule")
    .attr("x", x)
    .attr("y", 0)
    .attr("dy", -3)
    .attr("text-anchor", "middle")
    .text(String);

    chart.append("line")
    .attr("y1", 0)
    .attr("y2", 120)
    .style("stroke", "#000");
}

function svgVirBarChart(pythondata){
// var data = [4, 8, 15, 16, 23, 100, 33];
//    var name = ["a", "b", "c", "d", "n", "r", "k"];
// var height = 440;
// var width = 500;
    var data = pythondata;
 var height = 800
 var width = 1000
 var chart = d3.select("div#vir").append("svg")
    .attr("class", "chart")
    .attr("width", width)
    .attr("height", height)
    .append("g")
    .attr("transform", "translate(30,-8)");//图形水平位移量
    
 var y = d3.scale.linear()
    .domain([0, d3.max(data)])
    .range([0, 420]);//设置权重计算
    
 var x = d3.scale.ordinal()
    .domain(data)
    .rangeBands([0, 480]);
    //散列值 把480平均分配到data的每个数据段（这里是6个） 0~80，80~160,...值为（0，80，160，...）域宽80
    
 chart.selectAll("rect").data(data).enter().append("rect")
 .attr("x",x)//相当于function(d){return x(d);}
 .attr("y",function(d){return height-y(d)})//svg的坐标以左上角为原点，同过高度运算转成原点在左下角的效果
 .attr("width",x.rangeBand()) //获取散列值每段的长度 为矩形的宽
 .attr("height",y); // 通过函数1  function(d){return  (420/42)*d}  得到矩形的高
 
  //添加矩形上方的数字
 chart.selectAll("text")
    .data(data)
    .enter().append("text")
    .attr("x", function(d) { return x(d) + x.rangeBand() / 2; })  //散列值+散列宽度的一半
    .attr("y",function(d){return height-y(d)})
    .attr("dx", ".35em") //  horizontal-align: middle 居中对齐
    .attr("dy", 0) // vertical-align: middle //垂直方向无偏移
    .attr("text-anchor", "end") // text-align: right
    .text(String); //设置数据为显示值 相当于.text(function(d){ return d;})

// chart.selectAll("text")
//     .data(name)
//     .enter().append("text")
//     .attr("x", function(d) { return x(d) + x.rangeBand() / 2; })  //散列值+散列宽度的一半
//     .attr("y",function(d){return height})
//     .attr("dx", ".35em") //  horizontal-align: middle 居中对齐
//     .attr("dy", 0) // vertical-align: middle //垂直方向无偏移
//     .attr("text-anchor", "end") // text-align: right
//     .text(String); //设置数据为显示值 相当于.text(function(d){ return d;})

    
 
  chart.selectAll("line") //加横线 线 有关svg的标签请查看w3chool
    .data(y.ticks(10))   //y.ticks 根据权重 把数据进行划分层次，增加可读性。可以自己改变ticks的值察看效果来理解
    .enter().append("line")
    .attr("x1", 0)
    .attr("x2", 480)
    .attr("y1", function(d){return height -y(d)})
    .attr("y2", function(d){return height -y(d)})  //画线 （x1,y1） ------> (x2,y2)
    .style("stroke", "#ccc");
 
 
 chart.selectAll(".rule")
    .data(y.ticks(10))
    .enter().append("text")
    .attr("class", "rule")
    .attr("y",function(d){return height-y(d)})
    .attr("dy",5)
    .attr("dx",-8)
    .attr("text-anchor", "middle")
    .text(String); //添加Y 轴方向的数字
    
    chart.append("line")
    .attr("x1", 0)
    .attr("x2", width)
    .attr("y1",height)
    .attr("y2",height)
    .style("stroke", "#000");//添加x轴方向的线
    
    chart.append("line") //添加Y轴方向的线
    .attr("x1", 0)
    .attr("x2",0)
    .attr("y1",0)
    .attr("y2",height)
    .style("stroke", "#000");
  
}

//window.onload = function(){
//  //  divBarChart();
//    svgBarChart();
//    svgVirBarChart();
//};
