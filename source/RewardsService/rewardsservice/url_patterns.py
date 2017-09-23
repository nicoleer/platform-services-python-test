from handlers.rewards_handler import RewardsHandler
from handlers.get_all_customers_handler import GetAllCustomersHandler
from handlers.get_rewards_handler import GetRewardsHandler
from handlers.set_rewards_handler import SetRewardsHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/customer/get_all', GetAllCustomersHandler),
    (r'/customer/get_rewards', GetRewardsHandler),
    (r'/customer/set_rewards', SetRewardsHandler),
]
