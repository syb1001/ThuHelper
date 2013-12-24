urls = ["http://zhjw.cic.tsinghua.edu.cn/pk.classroomctrl.do?m=qyClassroomState&classroom=%D2%BB%BD%CC&weeknumber=1&mobile=true&cxrq=",
"http://zhjw.cic.tsinghua.edu.cn/pk.classroomctrl.do?m=qyClassroomState&classroom=%B6%FE%BD%CC&weeknumber=1&mobile=true&cxrq=",
"http://zhjw.cic.tsinghua.edu.cn/pk.classroomctrl.do?m=qyClassroomState&classroom=%C8%FD%BD%CC&weeknumber=1&mobile=true&cxrq=",
"http://zhjw.cic.tsinghua.edu.cn/pk.classroomctrl.do?m=qyClassroomState&classroom=%CB%C4%BD%CC&weeknumber=1&mobile=true&cxrq=",
"http://zhjw.cic.tsinghua.edu.cn/pk.classroomctrl.do?m=qyClassroomState&classroom=%CE%E5%BD%CC&weeknumber=1&mobile=true&cxrq=",
"http://zhjw.cic.tsinghua.edu.cn/pk.classroomctrl.do?m=qyClassroomState&classroom=%C1%F9%BD%CC&weeknumber=1&mobile=true&cxrq="];
//for(var i = 0;i<;i++){
	//setTimeout(function () {
		//window.location = urls[i];
	//}, i * 1000);
//}
function showdate(n) { 
	var uom = new Date(new Date()-0+n*86400000); 
	uom = uom.getFullYear() + "-" + (uom.getMonth()+1) + "-" + uom.getDate(); 
	return uom; 
} 
ymdates = [];
for(var i = 0;i<7;i++){
	ymdates.push(showdate(i));
}

fullurls = [];
for(var i = 0;i<6;i++){
	for(var j = 0;j<7;j++){
		url = urls[i]+ymdates[j];
		fullurls.push(url);
		
	}
}
/*for(i=0;i<fullurls.length;i++){
	window.open(fullurls[i]);
}
*/
i = 0;
function fun() {
	window.open(fullurls[i]);
	i++;
	if (i < fullurls.length) {
		setTimeout("fun()", 1000);
	}
}
fun();


/*var int=self.setInterval("openurls()",500)
var i = 0;
function openurls(){
	if(i>=urls.length)
		int=window.clearInterval(int);
	window.open(urls[i]);
	i++;
}*/