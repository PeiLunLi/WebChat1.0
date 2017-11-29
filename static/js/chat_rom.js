$(document).ready(function() {

	$('#date_detail').click(function() {

		var id = $('#user_id').text();
		location.href = "/chatromshow?user_id="+id;
	});
    $('#date_group_detail').click(function() {
		var id = $('#group_id').text();
		location.href = "/chatromshow?group_id="+id;
	});

	 var ws = new WebSocket("ws://10.0.147.87:9999/chatstart");
        // var cookie = document.cookie.split("=")[1];

        //接收服务器推送的数据
        ws.onmessage = function(e){
            $("#show_left").append("<p>"+e.data+"</p>");
        };
        //给服务器发送数据
        $('#sendMessage').click(function() {
		var dataStr = $("#message").val();
            $("#show_right").append("<p>"+"------你自己说："+dataStr+"</p>");
            ws.send(dataStr);
            $("#message").val("");
	});
        //添加好友
         $('#add_frind').click(function() {
		var number = $("#add_message").val();
        location.href = "/frind?number="+number;
        alert('添加成功！')
	});
        //添加群
         $('#add_group').click(function() {
		var number = $("#add_message").val();
        location.href = "/group?number="+number;
        alert('添加成功！')
	});
    //清屏
    $('#_clear').click(function (){
        $("#show_left").empty();
        $("#show_right").empty();
    });

});