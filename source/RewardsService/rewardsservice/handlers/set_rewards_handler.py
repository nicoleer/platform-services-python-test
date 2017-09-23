import json
import math
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class SetRewardsHandler(tornado.web.RequestHandler):

    client = MongoClient('mongodb', 27017)
    db = client['Rewards']
    rewards = list(db.rewards.find({}, {'_id': 0}))

    highest_tier = max(tier['points'] for tier in rewards)


    def getTier(self, points):
        rounded_points = math.floor(points/100) * 100

        if rounded_points > self.highest_tier:
            rounded_points = self.highest_tier

        if rounded_points == 0:
            return {'tier': '', 'points': 0, 'rewardName': ''}            
        else:
            return next(tier for tier in self.rewards if tier['points']==rounded_points)


    def getTierProgress(self, points, next_tier_points):
        # if there isn't a next tier, progress is 100%
        if points > self.highest_tier:
            return 1
        else:
            progress = (points / next_tier_points)
            return float("{0:.2f}".format(progress))


    @coroutine
    def post(self):
        email = self.get_argument('email', None)
        order_total = self.get_argument('order_total', None)

        if email == None or order_total == None:
            self.write({"status": 1, "message": "Invalid parameters"})
            return

        points = int(float(order_total))

        # update point total if the customer already exists
        existing_customer = self.db.customers.find_one({'email': email})
        if existing_customer:
            points += existing_customer['points']

        current_tier = self.getTier(points)
        next_tier = self.getTier(current_tier['points'] + 100)

        progress = self.getTierProgress(points, next_tier['points'])

        # Considered setting _id = email, but realized that you can't change _id values.
        # Users may want to change their email address in the future. If I had more time
        # to spend learning about MongoDB, I would investigate indexing the email field.
        customer = { "email" : email,
                     "points" : points,
                     "tier" : current_tier["tier"],
                     "tier_name" : current_tier["rewardName"],
                     "next_tier" : next_tier["tier"],
                     "next_tier_name" : next_tier["rewardName"],
                     "next_tier_progress" : progress 
                   }

        # upsert=True required to insert a document if it doesn't already exist
        self.db.customers.update({'email': email}, customer, upsert=True)
        self.write(customer)