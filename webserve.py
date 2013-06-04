import tornado
import tornado.httpserver 
import tornado.ioloop
import tornado.options
import tornado.web
import pymongo
#from bson.objectid import ObjectId
from tornado.options import define, options
import os
import json
import logging
import tornado.log 
import pprint

scriptdir = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(scriptdir, 'app')


define("port", default=8000, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self, dbname):
        handlers = [
            (r'/', DefaultHandler),
            (r"/phones", tornado.web.RedirectHandler, {"url": "/"}),
            (r'/((?:js|lib|css|img|partials)/.*)', tornado.web.StaticFileHandler, { 'path' : static_path}),
            (r"/api/(\w+)", PhoneListHandler),
            (r"/api/(\w+)/([^/]+)", PhoneDetailHandler)
            ]
        conn = pymongo.Connection("localhost", 27017)
        self.db = conn[dbname]
#       tornado.web.Application.__init__(self, handlers,  error_handler=ErrorHandler, debug=True)
        tornado.web.Application.__init__(self, handlers, debug=True)

# class ErrorHandler(tornado.web.ErrorHandler): 
#     def get_error_html(self, status_code, **kwargs):
#         print "ERROR"
#         if status_code == 404: 
#             return self.render_string('app/index.html') 
            
class DefaultHandler(tornado.web.RequestHandler):
    def get(self):
          logging.info("DefaultHandler")
          return  self.render("app/index.html")
        
def ok(o):
    #return json.dumps( { "ok" : o }) 
    return json.dumps(o)
    
class PhoneListHandler(tornado.web.RequestHandler):
    def get(self, collection):
        coll = self.application.db[collection]
        phones = list(coll.find())
        
        logging.info("PhoneListHandler: GET ")
        with open("dump", "w") as f:
            pprint.pprint(phones, stream=f, indent=4)
        #logging.info("PhoneListHandler: GET " +  json.dumps(phones)[:60] + "...")
        self.write(ok(phones))

    def post(self, collection):
        #logging.info("PhoneListHandler: PUT '%s' BODY '%s'" % (collection,  str(self.request.body)))
        coll = self.application.db[collection]
        doc = json.loads(self.request.body)
        logging.info("insert phone_id:"+doc['_id'])
        coll.insert(doc)

    def put(self, *args):
        logging.info("PUT - PhoneListHandler", str(map(str, args))) 
        
class PhoneDetailHandler(tornado.web.RequestHandler):
    def get(self, collection, phone_id):
        logging.info("PhoneHandler: collection='%(collection)s', phone_id='%(phone_id)s'" % vars())
        coll = self.application.db[collection]
        phone = coll.find_one({"_id": phone_id})
        if phone:
            self.write(ok(phone))
        else:
            #self.set_status(404)
            self.write({"error": "Unknown phone '{0}' in collection '{1}' ".format(phone_id, collection)})
            #raise tornado.web.HTTPError(404)

    def delete(self, collection, phone_id):
        logging.info("PhoneDetailHandler: DELETE collection='%(collection)s', phone_id='%(phone_id)s'" % vars())
        coll = self.application.db[collection]
        coll.remove({ '_id' : phone_id})

    def put(self, collection, phone_id):
        logging.info("PhoneDetailHandler: PUT collection='%(collection)s', phone_id='%(phone_id)s'" % vars())
        # logging.info("POST - PhoneDetailHandler")
        # #logging.info("PhoneListHandler: PUT '%s' BODY '%s'" % (collection,  str(self.request.body)))
        coll = self.application.db[collection]
        doc = json.loads(self.request.body)
        # logging.info("update phone_id:"+doc['_id'])
        coll.save(doc)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = Application("PhoneCat")
    http_server = tornado.httpserver.HTTPServer(app)
    #logging.info("PhoneDetailHandler.SUPPORTED_METHODS:" + str(PhoneDetailHandler.SUPPORTED_METHODS))
    http_server.listen(options.port) 
    tornado.ioloop.IOLoop.instance().start()
