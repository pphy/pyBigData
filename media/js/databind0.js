var dataset0 = [1,"A",2,"B",3]; 

function  bindData(){
	/*
		selector.data(dataset)  
		d3使用函数data(collection)绑定数据。默认是按下标绑定数据的。 collection表示数组
	*/
	var p = d3.select("div")  //选择一个div  
	.selectAll("p")   //选择div下的所有p元素
 	.data(dataset0) // ######绑定数据。
	.text(String);
	/*.text(function(d,i){  //i：当前数组下标，d:当然数组下标所对应的值
		var text = "遍历到该节点的数组下标是："+i+"    数组数据是： "+d;
		return text;
	});*/
	/*
	######
	text() 表示向添加的元素中加入数据，类似的 函数还有html()等。
	其中可以传入 匿名函数, 匿名函数可以接收两个参数，表示遍历到该元素时的数组下标和数组的值。
	这个匿名函数在多处都可以使用。等下在页面看一下效果就清楚是什么意思了。
	*/
	//如果p中填充的内容就是当前的数组下标所指向的内容也可以这样写
	/*
	var p = d3.select("div")
	.selectAll("p")
 	.data(dataset0) 
	.text(String);
	*/
}
