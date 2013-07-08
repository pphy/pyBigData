function selectAllTd(){
	var tds = d3.selectAll("tbody td").style("color",function(d,i){  //选择tbody下的所有td
			console.log("d is "+ d+" and i is " + i); //打印语句，因为没有绑定数据， 可以看到，d 输出的是 undefined,i则是下标，0，1，2，3 .....15
			return i%3 !== 0 ? null : "red";  //把所有 下标（下标从0开始） 为3倍数的td设为红色字体
	});	
	
}

function selectAllTdByTr(){
	//先选择tr，在选择td
	//实际形成的数据结构就相当于
	/*
						[[td,td,td,td],[td,td,td,td],[td,td,td,td],[td,td,td,td]]
	*/
	var tds = d3.selectAll("tbody tr")
		.attr("id",function(d,i){  //为了便于清楚  绑定的方式，给每个tr赋值
				return "tdId"+i;	
		})
		.selectAll("td");
		
	tds.style("color",function(d,i){ //这里就是分别遍历四个[td,td,td,td]中的td,那么下标应该为 0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3
			console.log(i);//打印下标
			return i%3 !== 0 ? null : "red"; 
			//i%3是为了证明 下标不是0~15 而是0~3. 如果是0~15那么 表格上显示的04就不是红色。因为04的下标是4。也可以根据控制台打印输出可以看出
	});	
	
}
