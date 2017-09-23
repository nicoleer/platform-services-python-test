from handlers.rewards_handler import RewardsHandler
from handlers.get_rewards_handler import GetRewardsHandler
from handlers.set_rewards_handler import SetRewardsHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/customer/get_rewards', GetRewardsHandler),
    (r'/customer/set_rewards', SetRewardsHandler),
]
