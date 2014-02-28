import logging
import os.path
import uuid

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web

def send_message(message):
	for chater in ChatSocketHandler.chaters:
		try:
			chater.write_message(message)
		except:
			logging.error('sending message error', exc_info=True)
	for callback in ChatHandler.callbacks:
		try:
			callback(message)
		except:
			logging.error('sending message error', exc_info=True)
	ChatHandler.callbacks = set()


class ChatSocketHandler(tornado.websocket.WebSocketHandler):
	chaters = set()
	
	def open(self):
		ChatSocketHandler.chaters.add(self)		
		send_message('A new chater has entered.')

	def on_close(self):
		ChatSocketHandler.chaters.remove(self)	
		send_message('A chater has left.')
		
	def on_message(self, message):
		send_message(message)


class ChatHandler(tornado.web.RequestHandler):
	callbacks = set()
	chaters = set()
	
	@tornado.web.asynchronous
	def get(self):
		print('A new chater has entered.')
		ChatHandler.callback.add(self.on_message)
		self.chater = chater = self.get_cooket('chater')
		if not user:
			self.user = user = str(uuid.uuid4())
			self.set_cooket('chater', chater)
		if chater not in ChatHandler.chaters:
			ChatHandler.chaters.add(chater)
			send_message('A new chater has entered.')
		
	def on_close(self):
		ChatHandler.callback.remove(self.on_message)
		ChatHandler.chaters.discard(self.chater)
		send_message('A chater has left.')
	
	def on_message(self, message):
		if self.request.connection.stream.closed():
			return
		self.write(message);
		self.finish()
	
	def post(self):
		send_message(self.get_argument('text'))
		

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('index.html')

if __name__ == '__main__':
	settings = {
		'template_path':os.path.join(os.path.dirname(__file__), 'templates'),
		'static_path':os.path.join(os.path.dirname(__file__), 'static')
	}
	
	application = tornado.web.Application([
		(r'/', MainHandler),
		(r'/chat', ChatHandler),
		(r'/chat/ws', ChatSocketHandler)
	], **settings)
	
	tornado.httpserver.HTTPServer(application).listen(8888)
	tornado.ioloop.IOLoop.instance().start()
