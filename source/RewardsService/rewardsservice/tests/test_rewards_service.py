import requests
import unittest

from pymongo import MongoClient

API_URL = "http://localhost:7050"

class TestRewardsService(unittest.TestCase):

  #TODO(nicole): Don't test using the real DB -- need to learn how this works
  @classmethod
  def setUpClass(cls):
    # client = MongoClient()
    # db = client['Rewards']
    pass


  def test_get_rewards(self):
      req = requests.get(API_URL + "/rewards")
      response = req.json()

      points = 100
      for tier in response:
        self.assertEqual(tier['points'], points)
        points += 100


  '''
  A customer that spends 100.80 earns 100 points and belongs in Tier A.
  Their next tier is Tier B and their progress % is 0.50.
  '''
  def test_set_customer_rewards(self):
      email = "test@test.com"
      req = requests.post(API_URL + "/customer/set_rewards",
              data = {
                  'email': email,
                  'order_total': 100.80
              })

      customer = req.json()

      self.assertEqual(req.status_code, 200)
      self.assertEqual(customer["email"], "test@test.com")
      self.assertEqual(customer["points"], 100)
      self.assertEqual(customer["tier"], "A")
      self.assertEqual(customer["tier_name"], "5% off purchase")
      self.assertEqual(customer["next_tier"], "B")
      self.assertEqual(customer["next_tier_name"], "10% off purchase")
      self.assertEqual(customer["next_tier_progress"], 0.5)

  '''
  Round a customer's progress percentage to two digits
  '''
  def test_set_customer_rewards_round_percentage(self):
      req = requests.post(API_URL + "/customer/set_rewards",
              data = {
                  'email': 'round@test.com',
                  'order_total': 879.00
              })

      customer = req.json()

      self.assertEqual(req.status_code, 200)
      self.assertEqual(customer["email"], "round@test.com")
      self.assertEqual(customer["points"], 879)
      self.assertEqual(customer["tier"], "H")
      self.assertEqual(customer["tier_name"], "40% off purchase")
      self.assertEqual(customer["next_tier"], "I")
      self.assertEqual(customer["next_tier_name"], "45% off purchase")
      self.assertEqual(customer["next_tier_progress"], 0.98)


  '''
  If the customer is in the top tier, they cannot earn additional rewards
  '''
  def test_set_customer_rewards_top_tier(self):
      req = requests.post(API_URL + "/customer/set_rewards",
              data = {
                  'email': 'toptier@test.com',
                  'order_total': 1200.80
              })

      customer = req.json()

      self.assertEqual(req.status_code, 200)
      self.assertEqual(customer["email"], "toptier@test.com")
      self.assertEqual(customer["points"], 1200)
      self.assertEqual(customer["tier"], "J")
      self.assertEqual(customer["tier_name"], "50% off purchase")
      self.assertEqual(customer["next_tier"], "J")
      self.assertEqual(customer["next_tier_name"], "50% off purchase")
      self.assertEqual(customer["next_tier_progress"], 1)


  '''
  If the customer is below the lowest tier, handle that case
  '''
  def test_set_customer_rewards_no_tier(self):
      req = requests.post(API_URL + "/customer/set_rewards",
              data = {
                  'email': 'notier@test.com',
                  'order_total': 10.00
              })

      customer = req.json()

      self.assertEqual(req.status_code, 200)
      self.assertEqual(customer["email"], "notier@test.com")
      self.assertEqual(customer["points"], 10)
      self.assertEqual(customer["tier"], "")
      self.assertEqual(customer["tier_name"], "")
      self.assertEqual(customer["next_tier"], "A")
      self.assertEqual(customer["next_tier_name"], "5% off purchase")
      self.assertEqual(customer["next_tier_progress"], 0.10)

  
  '''
  Update an existing customer's rewards data
  '''
  def test_set_existing_customer_rewards(self):
      email = "existing@test.com"
      # req = requests.post(API_URL + "/customer/set_rewards",
      #         data = {
      #             'email': email,
      #             'order_total': 100.80
      #         })

      # customer = req.json()

      # self.assertEqual(req.status_code, 200)
      # self.assertEqual(customer["email"], "existing@test.com")
      # self.assertEqual(customer["points"], 100)


      # client = MongoClient()
      # db = client['Customers']
      # db.Customers.insertOne({"email": email},
      #               { "email" : email,
      #                 "points" : 100,
      #                 "tier" : "A",
      #                 "tier_name" : "Name",
      #                 "next_tier" : "B",
      #                 "next_tier_name" : "Tier B Name",
      #                 "next_tier_progress" : 0.5 
      #               }
      # )


      # email = "existing@test.com"
      # req = requests.post(API_URL + "/customer/set_rewards",
      #         data = {
      #             'email': email,
      #             'order_total': 150.40
      #         })

      # customer = req.json()

      # self.assertEqual(req.status_code, 200)
      # self.assertEqual(customer["email"], email)
      # self.assertEqual(customer["points"], 250)
      # self.assertEqual(customer["tier"], "B")
      # self.assertEqual(customer["tier_name"], "10% off purchase")
      # self.assertEqual(customer["next_tier"], "C")
      # self.assertEqual(customer["next_tier_name"], "15% off purchase")
      # self.assertEqual(customer["next_tier_progress"], 0.75)


  
  def test_set_customer_rewards_invalid_email(self):
      pass


  def test_set_customer_rewards_invalid_total(self):
      pass


  '''
  Accept a customer's email address, and return the customer's rewards data that was stored in Endpoint 1.
  '''
  def test_get_customer_rewards(self):
      pass


  '''
  Return the same rewards data as Endpoint 2 but for all customers.
  '''
  def test_get_all_customer_rewards(self):
      pass


  # def tearDown(self):
  #     testing_email = "test@testemail.com"
  #     # if a record exists for test@testemail.com, remove it
  #     customer = db[customers].find_one({ email : testing_email })
  #       if customer != None::
  #           db.customers.deleteOne( { email: testing_email } )


  @classmethod
  def tearDownClass(cls):
      pass


if __name__ == '__main__':
    unittest.main()