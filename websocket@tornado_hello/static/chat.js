$(document).ready(function() {
	var $msg = $('#msg');
	var $text = $('#text');
	
	var socket = new WebSocket('ws://localhost:8888/chat/ws');
	if(socket) {
		socket.onmessage = function(event) {
			$msg.append('<p>' + event.data + '</p>');
		}
	
		$('form').submit(function() {
			socket.send($text.val());
			$text.val('').select();
			return false;
		});
	} else {
		var error_sleep_time = 500;
		
		function poll() {
			$.ajax({
				url: '/chat',
				type: 'GET',
				success: function(event) {
					$msg.append('<p>' + event.data + '</p>');
					error_sleep_time = 500;
					poll()
				},
				error: function() {
					error_sleep_time *= 2;
					setTimeout(poll, error_sleep_time);
				}
			});
		}
		
		poll();
		$('form').submit(function() {
			$.ajax({
				url: '/chat',
				type: 'POST',
				data: { text: $text.val() },
				success: function() {
					$text.val('').select();
				}
			})
			return false;
		});
	}
});
