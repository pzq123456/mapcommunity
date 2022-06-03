var map = new BMapGL.Map("container");

var point = new BMapGL.Point(120.131267, 36.005814);//学校南门
map.centerAndZoom(point, 15);// 创建地图实例 

var width=700;
var height=500;

var displayData= function(data){
            for (let i = 0; i < data.length; i++) 
            {
                let vpoint = new BMapGL.Point(data[i].lon,data[i].lat);//学校南门
                let title=data[i].user+"的留言";
                add_simple_infowindow_on_map(map,vpoint,width,height,title,data[i].content);                            
            } 
        }
        $.ajax({
            url: "/JSON",
            type: "GET",
            dataType: "json",
            success: 
            function (data) {
                displayData(data)
            }
        });





var html_content=[
'            <form action = "{{ request.path }}" method = "post">                          ',
'            <label for = "lon" class="lables" style="visibility:visible;">经度</label><br>',
'            <input type = "float" name = "lon" placeholder ="120.131267" class="lables" style="visibility:visible;"/><br>',
'   ',
'            <label for = "lat" class="lables" style="visibility:visible;">纬度</label><br>',
'            <input type = "float" name = "lat" placeholder ="36.005814" class="lables" style="visibility:visible;"/><br>',
'   ',
'            <label for = "content" class="lables" >留言内容</label><br>',
'            <textarea name = "content" placeholder = "Hello World!" class="textareastyle"></textarea><br>',
'   ',
'            <input type = "submit" class="button" value = "Submit" />',
'         </form>','</center>'
].join("");

html_content=html_content+"<br><hr/>{%- for message in get_flashed_messages() %}{{ message }}{%- endfor %}"


map.addEventListener('click', function (e) {
    alert('点击位置经纬度：' +'经度：'+ e.latlng.lng + '纬度：'+ e.latlng.lat+ " 请将鼠标移至点上进行留言");

    var new_point=new BMapGL.Point(e.latlng.lng, e.latlng.lat);
    add_html_infowindow_on_map(map,new_point,width,height,"<center><h7 style='color:#4798cf;'>地图留言板：</h7></center>",html_content);




});


//封装进函数 创建简单信息窗口（不含HTML）
function add_simple_infowindow_on_map(map,my_point,win_width,win_height,title_text,content_text) {

	var marker = new BMapGL.Marker(my_point);  // 创建标注
    map.addOverlay(marker);              // 将标注添加到地图中

	var opts = {
	    width : win_width,     // 信息窗口宽度
	    height: win_height,     // 信息窗口高度
	    title : title_text , // 信息窗口标题
	   
	}

var infoWindow = new BMapGL.InfoWindow(content_text, opts);  // 创建信息窗口对象 

marker.addEventListener('mouseover', function(){          
		map.openInfoWindow(infoWindow, my_point); //开启信息窗口
        /*
        //此处可以加js代码来操控信息窗口的内容！
        var active_info_bubble=document.querySelector('.BMap_bubble_pop');//获取当前打开的信息窗口
        var active_info_win_content=document.querySelector('.BMap_bubble_content');//获取当前打开的信息窗口
        //=active_info_win_content.querySelector("button");//获取信息窗口内的按钮
        var but_in_win=active_info_win_content.querySelectorAll("button");
        
        but_in_win[0].addEventListener("click",but_1_fun);//添加事件处理程序
        function but_1_fun(){alert("按钮1的事件处理程序!");}
        but_in_win[1].addEventListener("click",vut_2_fun);//添加事件处理程序
        function vut_2_fun(){alert("按钮2的事件处理程序!");}
        infoWindow.addEventListener("close",function(){alert("信息窗口已关闭!");infoWindow.removeEventListener('close');but_in_win[0].removeEventListener("click",but_1_fun);but_in_win[1].removeEventListener("click",vut_2_fun);})
        */
        
	}); 
     
}



map.enableScrollWheelZoom(true);   //开启鼠标滚轮缩放



function add_html_infowindow_on_map(map,my_point,win_width,win_height,title_text,content_text) {

var marker = new BMapGL.Marker(my_point);  // 创建标注
map.addOverlay(marker);              // 将标注添加到地图中

var opts = {
    width : win_width,     // 信息窗口宽度
    height: win_height,     // 信息窗口高度
    title : title_text , // 信息窗口标题
   
}

var infoWindow = new BMapGL.InfoWindow(content_text, opts);  // 创建信息窗口对象 

marker.addEventListener('mouseover', function(){          
    map.openInfoWindow(infoWindow, my_point); //开启信息窗口
    
    //此处可以加js代码来操控信息窗口的内容！
    var active_info_bubble=document.querySelector('.BMap_bubble_pop');//获取当前打开的信息窗口
    var active_info_win_content=document.querySelector('.BMap_bubble_content');//获取当前打开的信息窗口
    var form= active_info_win_content.querySelector('form');
    
    var lon=form.childNodes[4];
    lon.value=my_point.lng;
    //lon.textContent=my_point.lng;
    //alert(lon.value);
    var lat=form.childNodes[10];
    lat.textContent=my_point.lat;
    lat.value=my_point.lat;
    //alert(lat.value);


    
    //infoWindow.addEventListener("close",function(){alert("信息窗口已关闭!");infoWindow.removeEventListener('close');but_in_win[0].removeEventListener("click",but_1_fun);but_in_win[1].removeEventListener("click",vut_2_fun);})
    
    
}); 
 
}



