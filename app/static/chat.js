$(function(){
    var socket;
    var all_users=[];
        socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
        socket.on('connect', function() {
            socket.emit('joined room', {});
                return false;
                });

            socket.on('join message', function(data) {
                var current_user = $('#user_name').text();
                if (current_user == data.sender_name){
                    var html = '<p>'+data.sender_name+" "+data.translated_msg+'</p><br>';
                    $('.chat-con').append(html);
                }else{
                    socket.emit('join message to others',data);
                    return false;
                }
            });
            socket.on('send join message to others',function(data){
                 var html = '<p>'+data.username+" " + data.translated_msg+'</p><br>';
                $('.chat-con').append(html);
            });
            socket.on('left message', function(data) {
                var html = '<p>'+data.translated_msg+'</p><br>';
                $('.chat-con').append(html);
            });
            socket.on('receiveMessage',function(data){
    		    var receiver_name = $('#user_name').text();
//    		    console.log("receiveMessage:")
//    		    console.log(data)
    		    showMessage(data,receiver_name);
				});

            $('#text').keypress(function(e) {
                var code = e.keyCode || e.which;
                if (code == 13) {
                    var txt = $('#text').val();
                    $('#text').val('');
                    var name = $('#user_name').text();
                    if(txt){
                        socket.emit('sendMessage',txt);
                        }
                    }
            });

            $('#send_text').click(function(){
                var txt = $('#text').val();
    		    $('#text').val('');
    		    var name = $('#user_name').text();
    		    if(txt){
        	        socket.emit('sendMessage',txt);
        	        return false;

    			    }
				});

		function sendMessage(){
    	    var txt = $('#text').val();
    		$('#text').val('');
    		var name = $('#user_name').text();
    		if(txt){
        	    socket.emit('sendMessage',{username:name,message:txt});
    			}
			};

		function showMessage(data,current_user){
    	    var html;
    		if(data.sender_name === current_user){
        		html = '<div class="chat-item item-right clearfix"><span class="img fr"></span><span class="message fr">'+data.message+'</span></div>'
    		    $('.chat-con').append(html);

    		}else{
        		html='<div class="chat-item item-left clearfix rela"><span class="abs uname">'+data.sender_name+'</span><span class="img fl"></span><span class="fl message">'+data.message+'</span></div>'
    			$('.chat-con').append(html);
                socket.emit('translate message',data);
    			}

    		return false;
			};

			socket.on('sendback translated message',function(data){
        		var html;
        		html='<div class="chat-item item-left-2 clearfix rela"><span class="abs uname" text="translated">[Translated] '+data.message.sender_name+' </span><span class="img fl"></span><span class="fl message 2">'+data.message.translated_msg+'</span></div>'
                $('.chat-con').append(html);
                return false;
			});

        $('#link_to_leave').click(function(){
        leave_room();
        return false;
        });
        function leave_room() {

            socket.emit('left room', {}, function() {
                socket.disconnect();
                // go back to the login page
                window.location.href = "http://" + document.domain + ':' + location.port;
            });
            };
});


