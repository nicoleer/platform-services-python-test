import requests
import unittest

from pymongo import MongoClient

API_URL = "http://localhost:7050/"

class TestRewardsService(unittest.TestCase):

  #TODO(nicole): Don't test using the real DB -- need to learn how this works
  @classmethod
  def setUpClass(cls):
    # client = MongoClient()
    # db = client['Rewards']
    pass


  def test_get_rewards(self):
      req = requests.get(API_URL + "rewards")
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
      req = requests.post(API_URL + "/customer/set_rewards",
              data = {
                  'email': 'test@testemail.com',
                  'order_total': 100.80
              })

      self.assertEqual(req.status_code, 404)

      # get customer out of db

      # self.assertEqual(customer.email, "test@testemail.com")
      # self.assertEqual(customer.points, 100)
      # self.assertEqual(customer.tier, "A")
      # self.assertEqual(customer.tier_name, "5% off purchase")
      # self.assertEqual(customer.next_tier, "B")
      # self.assertEqual(customer.next_tier_name, "10% off purchase")
      # self.assertEqual(customer.next_tier_progress, 0)

  '''
  Round a customer's progress percentage to two digits
  '''
  def test_set_customer_rewards_round_percentage(self):
      req = requests.post(API_URL + "/customer/set_rewards",
              data = {
                  'email': 'test@testemail.com',
                  'order_total': 879.00
              })

      self.assertEqual(req.status_code, 404)

      # get customer out of db
      
      # self.assertEqual(customer.email, "test@testemail.com")
      # self.assertEqual(customer.points, 879)
      # self.assertEqual(customer.tier, "H")
      # self.assertEqual(customer.tier_name, "40% off purchase")
      # self.assertEqual(customer.next_tier, "I")
      # self.assertEqual(customer.next_tier_name, "45% off purchase")
      # self.assertEqual(customer.next_tier_progress, 0.97)


  '''
  If the customer is in the top tier, they cannot earn additional rewards
  '''
  def test_set_customer_rewards_top_tier(self):
      req = requests.post(API_URL + "/customer/set_rewards",
              data = {
                  'email': 'test@testemail.com',
                  'order_total': 1000.80
              })

      self.assertEqual(req.status_code, 404)

      # get customer out of db
      
      # self.assertEqual(customer.email, "test@testemail.com")
      # self.assertEqual(customer.points, 1000)
      # self.assertEqual(customer.tier, "J")
      # self.assertEqual(customer.tier_name, "50% off purchase")
      # self.assertEqual(customer.next_tier, "")
      # self.assertEqual(customer.next_tier_name, "")
      # self.assertEqual(customer.next_tier_progress, 1)

  
  '''
  Update an existing customer's rewards data
  '''
  def test_set_existing_customer_rewards(self):
      pass


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


  # TODO(nicole): Implement teardown
  # def tearDown(self):
      # if a record exists for test@testemail.com, remove it

  @classmethod
  def tearDownClass(cls):
      pass


if __name__ == '__main__':
    unittest.main()