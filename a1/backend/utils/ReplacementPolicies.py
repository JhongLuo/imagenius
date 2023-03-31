from enum import Enum

class ReplacementPolicies(Enum):
    LRU = 0
    RANDOM = 1
    @staticmethod
    def policy2str(policy):
        if policy == ReplacementPolicies.LRU:
            return 'LRU'
        elif policy == ReplacementPolicies.RANDOM:
            return 'random'
        else:
            raise Exception('Invalid policy')
    @staticmethod 
    def str2policy(policy_str):
        if policy_str == 'LRU':
            return ReplacementPolicies.LRU
        elif policy_str == 'random':
            return ReplacementPolicies.RANDOM
        else:
            raise Exception('Invalid policy')
    @staticmethod
    def int2policy(policy_int):
        if policy_int == 0:
            return ReplacementPolicies.LRU
        elif policy_int == 1:
            return ReplacementPolicies.RANDOM
        else:
            raise Exception('Invalid policy')