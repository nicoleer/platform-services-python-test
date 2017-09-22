from handlers.rewards_handler import RewardsHandler
from handlers.set_rewards_handler import SetRewardsHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/customer/set_rewards', SetRewardsHandler),
]
