
strs = ['.d1j','.d2j','.d3j','.d4j','.d5j','.d6j'];
classrooms = [];
status = "";
goodstatus = status;
buildings = ['%D2%BB%BD%CC','%B6%FE%BD%CC','%C8%FD%BD%CC','%CB%C4%BD%CC','%CE%E5%BD%CC','%C1%F9%BD%CC'];
for(var i = 0;i<6;i++){
	if(buildings[i]== window.location.href.substring(81,93))
		break;
}
building = i+1;
window.location.href.substring(81,93)
for(var i = 0;i<6;i++){
	arrays = $(strs[i]);
	for(var j = 0;j<arrays.length;j++){
		if(arrays[j].className[3] == 'x'){
			status+='0';
		}
		else{
			status+='1';
		}
	}
}
length = status.length/6;


for(var i = 0;i<status.length;i++){
	goodstatus+=status[(i%6)*length+Math.floor((i)/6)];
	//goodstatus[(i%length)*6+Math.floor((i)/length)] = status[i];
}
	
//alert(goodstatus);
arrays = $('.d1j');
for(var i = 0;i<arrays.length;i++){
	classrooms.push(arrays[i].className.substring(9));
}

finalstatus = [];
for(var i = 0;i<length;i++){
	var singleclassroom = {};
	singleclassroom["name"] = classrooms[i];
	singleclassroom["status"] = goodstatus.substring(i*6,i*6+6);
	
	finalstatus.push(singleclassroom);
}
hehehe = $('option[selected = "selected"]')[0];

weekdaystr = $(hehehe).html().substring(11,12);
weekdays = ["一","二","三","四","五","六","七"];
for(var i = 0;i<7;i++){
	if(weekdaystr == weekdays[i])
		break;
}
weekday = i+1;
$.post('http://thuhelper11.duapp.com/dataupdate/', {status:finalstatus,weekday:weekday,building:building}, function (data) {
	//alert(1);
	alert(data.message);
}, 'json')


