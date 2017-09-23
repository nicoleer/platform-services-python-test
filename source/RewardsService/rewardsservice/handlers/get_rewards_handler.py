from bson.json_util import dumps
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class GetRewardsHandler(tornado.web.RequestHandler):

    @coroutine
    def post(self):
        client = MongoClient('mongodb', 27017)
        customer_db = client['Customers']

        email = self.get_argument('email', None)
        customer  = customer_db.Customers.find_one({'email': email})

        if customer is None:
            response = {
                "status": 1,
                "message": "No customer found for email address [%s]" % email
            }
        else:
            response = dumps(customer)

        self.write(response)