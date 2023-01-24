function realtimeClock(){
    
    var rtClock = new Date;
    var dname = rtClock.getDay(),
        mo = rtClock.getMonth(),
        dnum = rtClock.getDate(),
        hours = rtClock.getHours(),
        minutes = rtClock.getMinutes();

    // 00月 00日 0曜日
    var month = ["1月","2月","3月","4月","5月","6月","7月","8月","9月","10月","11月","12月"];
    var week = ["日曜日","月曜日","火曜日","水曜日","木曜日","金曜日","土曜日"];
    var days = [
        "1日","2日","3日","4日","5日","6日","7日","8日","9日","10日",
        "11日","12日","13日","14日","15日","16日","17日","18日","19日","20日",
        "21日","22日","23日","24日","25日","26日","27日","28日","29日","30日",
        "31日"];
    var ids = ["month", "daynum", "dayname"];
    var values = [month[mo], days[dnum-1], week[dname]];
    for(var i = 0; i < ids.length; i++)
    document.getElementById(ids[i]).firstChild.nodeValue = values[i];

    // Pad the hours, minutes and seconds with leading zeros
    hours = ("0" + hours).slice(-2);
    minutes = ("0" + minutes).slice(-2);

    // Display the clock
    document.getElementById('clock').innerHTML =
        hours + ":" + minutes;
    var t = setTimeout(realtimeClock, 500); 
}