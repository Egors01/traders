import random
from itertools import combinations
from numpy.random import choice
from collections import Counter


class Trader:
    def __init__(self, strategy):
        self.strategy_name = strategy
        self.opponent_history = []
        self.money = 0
        self.STRATEGY_TO_FUNCTION = {'altruist': self.altruist_strategy,
                                     'kidala': self.kidala_strategy,
                                     'hitrez': self.hitrez_strategy,
                                     'random': self.random_strategy,
                                     'zlop': self.zlopam_strategy,
                                     'ushly': self.ushly_strategy
                                     }
        self.strategy_function = self.STRATEGY_TO_FUNCTION.get(strategy)
        #
        # print('strategy ',str( self.strategy_function))

    def make_move(self):
        final_decision = self.strategy_function()
        return final_decision

    def record_history(self, opponent_move):
        self.opponent_history.append(opponent_move)

    def add_money(self, amount):
        self.money += amount
        return

    def altruist_strategy(self):
        decision = choice(['good', 'bad'], p=[0.05, 0.95])
        return decision

    def kidala_strategy(self):
        decision = choice(['good', 'bad'], p=[0.95, 0.05])
        return decision

    def hitrez_strategy(self):
        if self.opponent_history == []:
            decision = choice(['good', 'bad'], p=[0.05, 0.95])
        else:
            decision = self.opponent_history.pop()
        return decision

    def random_strategy(self):
        decision = choice(['good', 'bad'], p=[0.5, 0.5])
        return decision

    def zlopam_strategy(self):
        if 'bad' in self.opponent_history:
            decision = choice(['good', 'bad'], p=[0.05, 0.95])
        else:
            decision = choice(['good', 'bad'], p=[0.95, 0.05])
        return decision

    def ushly_strategy(self):
        decision = 'ERROR ushly'
        if len(self.opponent_history) > 4:
            if 'bad' in self.opponent_history:
                self.strategy_function = self.kidala_strategy
                decision = choice(['good', 'bad'], p=[0.95, 0.05])
                print('LOG strategy_change')
        elif len(self.opponent_history) == 1:
            decision = choice(['good', 'bad'], p=[0.05, 0.95])  # bad after first move
        else:
            decision = choice(['good', 'bad'], p=[0.95, 0.05])  # good on first third fourth
        return decision

    def reset_round_memory(self):
        self.opponent_history = []
        self.strategy_function = self.STRATEGY_TO_FUNCTION.get(self.strategy_name)
        return


class AnnualTrading:
    def __init__(self, strategies, input_traders_list):
        self.STRATEGIES = strategies
        self.outsider_strategy = None
        self.best_strategy = None
        self.traders_list = input_traders_list
        self.n_traders = len(self.traders_list)
        self.end_of_year_traders_list = self.process_annual_round()

    def process_deal_for_pair(self, traider_one, traider_two):
        first_decision = traider_one.make_move()
        second_decision = traider_two.make_move()

        [value_one, value_two] = [None, None]
        if first_decision == 'good' and second_decision == 'good':
            value_one = 4
            value_two = 4
        elif first_decision == 'bad' and second_decision == 'bad':
            value_one = 2
            value_two = 2
        elif first_decision == 'good' and second_decision == 'bad':
            value_one = 1
            value_two = 5
        elif first_decision == 'bad' and second_decision == 'good':
            value_one = 5
            value_two = 1
        else:
            print('cannot process decision')

        traider_one.add_money(value_one)
        traider_two.add_money(value_two)
        traider_one.record_history(second_decision)
        traider_two.record_history(first_decision)
        return

    def process_annual_round(self):
        for traiders_pair in combinations(self.traders_list, 2):
            n_deals = random.randint(5, 10)
            for round in range(0, n_deals):
                self.process_deal_for_pair(traiders_pair[0], traiders_pair[1])
                traiders_pair[0].reset_round_memory()
                traiders_pair[1].reset_round_memory()

        sorted_traders_list = sorted(self.traders_list, key=lambda trader: trader.money, reverse=True)
        self.best_strategy = sorted_traders_list[0].strategy_name
        self.outsider_strategy = sorted_traders_list[-1].strategy_name
        return sorted_traders_list

    def print_annual_stats(self):
        print('Trading year results')
        print('%s strategy is on top' % self.best_strategy)
        print('%s strategy is outsider' % self.outsider_strategy)


def generate_updated_traders_list(previous_traders_list):
    sorted_previous_traders_list = \
        sorted(previous_traders_list, key=lambda trader: trader.money, reverse=True)
    staying_traders_list = sorted_previous_traders_list[:48]
    newcommers_traders_list = []
    for trader in staying_traders_list[:12]:
        copy_strategy = trader.strategy_name
        newcommers_traders_list.append(Trader(copy_strategy))
    new_traders_list = staying_traders_list + newcommers_traders_list
    return new_traders_list


def generate_initial_trader_list(strategies):
    traders_list = []
    for strategy in strategies:
        traders_list += [Trader(strategy)] * 10
    return traders_list


if __name__ == '__main__':
    stats = []
    for sim in range(0, 2):
        open_strategies = ['altruist', 'kidala', 'random', 'hitrez', 'ushly', 'zlop']
        n_years = 5
        traders_list = generate_initial_trader_list(open_strategies)
        for year in range(0, n_years):
            annual_trade = AnnualTrading(strategies=open_strategies, input_traders_list=traders_list)
            annual_trade.print_annual_stats()
            traders_list = generate_updated_traders_list(annual_trade.end_of_year_traders_list)
        print('20 years passed ')
        stats.append(annual_trade.best_strategy)
    print('Strategy in sim stats \n', stats)
    statist_obj = Counter(stats)
    most_occur = statist_obj.most_common(10)
    print('Strategy occurences')
    print(most_occur)
