from bson.json_util import dumps
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class GetAllCustomersHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        client = MongoClient('mongodb', 27017)
        customer_db = client['Customers']
        
        customers_bson  = customer_db.Customers.find()

        # reformat the list into a dictionary, with email as the keys
        customers = dict((item['email'], item) for item in customers_bson)
        self.write(dumps(customers))