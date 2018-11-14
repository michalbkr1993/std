from random import randint
from random import choice


class Creature:

    def __init__(self, cooperator):
        self.credits = randint(0, 10)
        self.cooperator = cooperator

    def give_help(self):
        a = randint(1, 10)
        if self.cooperator and a < self.credits:
            self.credits -= a
            return a
        else:
            return 0

    def take_help(self, c):
        self.credits += c

    def is_cooperator(self):
        return self.cooperator

    def get_credits(self):
        return self.credits


class Group:

    def __init__(self, list_of_creatures):
        self.creatures = list_of_creatures

    def child(self):
        lucky_member = randint(0, len(self.creatures) - 1)
        if self.creatures[lucky_member].get_credits() >= randint(0, 10):
            self.creatures.append(Creature(self.creatures[lucky_member].is_cooperator()))

    def interaction_in_group(self):
        self.creatures[randint(0, self.number_of_creatures() - 1)].take_help(
            self.creatures[randint(0, self.number_of_creatures() - 1)].give_help())

    def new_member(self, cooperator):
        self.creatures.append(Creature(cooperator))

    def number_of_creatures(self):
        return len(self.creatures)

    def get_creatures(self):
        return self.creatures


class Enviroment:

    def __init__(self, initial_group_size, initial_groups_number, max_groups_number=10, max_group_size=100):
        self.max_groups_number = max_groups_number
        self.max_group_size = max_group_size
        self.groups = [Group([Creature(choice([True, False])) for x in range(0, initial_group_size)]) for x in range(0, initial_groups_number)]

    def get_groups(self):
        return self.groups

    def child(self):
        lucky_group = randint(0, len(self.groups) - 1)
        self.groups[lucky_group].child()
        if self.groups[lucky_group].number_of_creatures() > self.max_group_size:
            if len(self.groups) == self.max_groups_number:
                a = self.groups[lucky_group]
                self.groups.pop(lucky_group)
                self.groups.pop(randint(0, len(self.groups)))
                self.groups.append(a[:a.number_of_creatures()/2])
                self.groups.append(a[a.number_of_creatures()/2:])
            else:
                a = self.groups[lucky_group]
                print(a.get_creatures())
                self.groups[lucky_group] = a[:a.number_of_creatures()/2]
                self.groups.append(a[a.number_of_creatures()/2:])

    def interaction(self):
        for group in self.groups:
            group.interaction_in_group()

    def cooperators_to_defectors(self):
        c = 0
        d = 0
        for x in self.groups:
            for y in x.get_creatures():
                if y.is_cooperator():
                    c += 1
                else:
                    d += 1
        return float(c)/float(d)


if __name__ == '__main__':
    # a = [Group([Creature(choice([True, False])) for x in range(0, 5)]) for x in range(0, 2)]
    # print (a[0].get_creatures())
    env = Enviroment(2, 2, 10, 20)
    print (env.get_groups()[0].get_creatures())
    print(env.cooperators_to_defectors())
    for x in range(0, 100000):
        env.interaction()
        if x % 10 == 0:
            env.child()
    print(env.cooperators_to_defectors())
