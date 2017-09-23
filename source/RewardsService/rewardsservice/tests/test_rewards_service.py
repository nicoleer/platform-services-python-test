import requests
import unittest

from pymongo import MongoClient

API_URL = "http://localhost:7050"
EMAIL = "test@test.com"

class TestRewardsService(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
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
      req = requests.post(API_URL + "/customer/set_rewards",
              data = {
                  'email': EMAIL,
                  'order_total': 100.80
              })

      customer = req.json()

      self.assertEqual(req.status_code, 200)
      self.assertEqual(customer["email"], EMAIL)
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
                  'email': EMAIL,
                  'order_total': 879.00
              })

      customer = req.json()

      self.assertEqual(req.status_code, 200)
      self.assertEqual(customer["email"], EMAIL)
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
                  'email': EMAIL,
                  'order_total': 1200.80
              })

      customer = req.json()

      self.assertEqual(req.status_code, 200)
      self.assertEqual(customer["email"], EMAIL)
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
                  'email': EMAIL,
                  'order_total': 10.00
              })

      customer = req.json()

      self.assertEqual(req.status_code, 200)
      self.assertEqual(customer["email"], EMAIL)
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
      client = MongoClient()
      db = client['Customers']
      db.Customers.insert(
                    { "email" : EMAIL,
                      "points" : 100,
                      "tier" : "A",
                      "tier_name" : "5% off purchase",
                      "next_tier" : "B",
                      "next_tier_name" : "10% off purchase",
                      "next_tier_progress" : 0.5 
                    }
      )
      existing_customer = db.Customers.find_one({'email': EMAIL})

      self.assertIsNotNone(existing_customer)

      req = requests.post(API_URL + "/customer/set_rewards",
              data = {
                  'email': EMAIL,
                  'order_total': 150.40
              })

      customer = req.json()

      self.assertEqual(req.status_code, 200)
      self.assertEqual(customer["email"], EMAIL)
      self.assertEqual(customer["points"], 250)
      self.assertEqual(customer["tier"], "B")
      self.assertEqual(customer["tier_name"], "10% off purchase")
      self.assertEqual(customer["next_tier"], "C")
      self.assertEqual(customer["next_tier_name"], "15% off purchase")
      self.assertEqual(customer["next_tier_progress"], 0.83)


  def test_set_customer_rewards_invalid_email(self):
      req = requests.post(API_URL + "/customer/set_rewards",
              data = {
                  'order_total': 100.00
              })

      response = req.json()

      self.assertEqual(response["status"], 1)
      self.assertEqual(response["message"], "Invalid parameters")


  def test_set_customer_rewards_invalid_total(self):
      req = requests.post(API_URL + "/customer/set_rewards",
              data = {
                  'email': EMAIL
              })

      response = req.json()

      self.assertEqual(response["status"], 1)
      self.assertEqual(response["message"], "Invalid parameters")


  '''
  Accept a customer's email address, and return the customer's rewards data
  '''
  def test_get_customer_rewards(self):
      client = MongoClient()
      db = client['Customers']
      db.Customers.insert(
                    { "email" : EMAIL,
                      "points" : 100,
                      "tier" : "A",
                      "tier_name" : "5% off purchase",
                      "next_tier" : "B",
                      "next_tier_name" : "10% off purchase",
                      "next_tier_progress" : 0.5 
                    }
      )
      existing_customer = db.Customers.find_one({'email': EMAIL})

      self.assertIsNotNone(existing_customer)

      req = requests.post(API_URL + "/customer/get_rewards",
              data = {
                  'email': EMAIL
              })

      response = req.json()

      self.assertEqual(req.status_code, 200)
      self.assertEqual(response["email"], EMAIL)
      self.assertEqual(response["points"], 100)
      self.assertEqual(response["tier"], "A")
      self.assertEqual(response["tier_name"], "5% off purchase")
      self.assertEqual(response["next_tier"], "B")
      self.assertEqual(response["next_tier_name"], "10% off purchase")
      self.assertEqual(response["next_tier_progress"], 0.5)


  def test_get_customer_rewards_customer_not_found(self):
      email = "userdoesntexist@test.com"
      req = requests.post(API_URL + "/customer/get_rewards",
              data = {
                  'email': email
              })

      response = req.json()

      self.assertEqual(req.status_code, 200)
      self.assertEqual(response['status'], 1)
      self.assertEqual(response['message'], "No customer found for email address [%s]" % email)


  '''
  Return rewards data for all customers
  '''
  def test_get_all_customer_rewards(self):
      client = MongoClient()
      db = client['Customers']

      db.Customers.insert({"email" : "email1@test.com", "points" : 100, "tier" : "A", "tier_name" : "5% off purchase",
                           "next_tier" : "B", "next_tier_name" : "10% off purchase", "next_tier_progress" : 0.5 })
      db.Customers.insert({"email" : "email2@test.com", "points" : 100, "tier" : "A", "tier_name" : "5% off purchase",
                           "next_tier" : "B", "next_tier_name" : "10% off purchase", "next_tier_progress" : 0.5 })
      db.Customers.insert({"email" : "email3@test.com", "points" : 100, "tier" : "A", "tier_name" : "5% off purchase",
                           "next_tier" : "B", "next_tier_name" : "10% off purchase", "next_tier_progress" : 0.5 })

      req = requests.get(API_URL + "/customer/get_all")
      response = req.json()

      self.assertEqual(req.status_code, 200)
      self.assertEqual(len(response), 3)
      self.assertIsNotNone(response.get('email1@test.com', None))
      self.assertIsNotNone(response.get('email2@test.com', None))
      self.assertIsNotNone(response.get('email3@test.com', None))


  def tearDown(self):
      # if a record exists for test@testemail.com, remove it
      client = MongoClient()
      db = client['Customers']
      customer = db.Customers.find_one({'email': EMAIL})
      if customer != None:
          db.Customers.delete_many({'email': EMAIL})


  @classmethod
  def tearDownClass(cls):
      client = MongoClient()
      db = client['Customers']
      db.Customers.remove()



if __name__ == '__main__':
    unittest.main()