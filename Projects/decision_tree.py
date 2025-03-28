
"""
Pure python decision Tree (and string representation) with max depth, tested using custom datum objects
"""


ATTRIBUTES = ('Alternative', 'Bar', 'Friday/Saturday', 'Hungry', 'Patrons', 'Price', 'Raining',
              'Reservation', 'Type', 'Wait')


class Datum:
    def __init__(self, target, *values):
        self.target = target
        self.attributes = dict(zip(ATTRIBUTES, values))


data = (Datum(True, True, False, False, True, 'Some', '$$$', False, True, 'French', '0-10'),
        Datum(False, True, False, False, True, 'Full', '$', False, False, 'Thai', '30-60'),
        Datum(True, False, True, False, False, 'Some', '$', False, False, 'Burger', '0-10'),
        Datum(True, True, False, True, True, 'Full', '$', True, False, 'Thai', '10-30'),
        Datum(False, True, False, True, False, 'Full', '$$$', False, True, 'French', '>60'),
        Datum(True, False, True, False, True, 'Some', '$$', True, True, 'Italian', '0-10'),
        Datum(False, False, True, False, False, 'None', '$', True, False, 'Burger', '0-10'),
        Datum(True, False, False, False, True, 'Some', '$$', True, True, 'Thai', '0-10'),
        Datum(False, False, True, True, False, 'Full', '$', True, False, 'Burger', '>60'),
        Datum(False, True, True, True, True, 'Full', '$$$', False, True, 'Italian', '10-30'),
        Datum(False, False, False, False, False, 'None', '$', False, False, 'Thai', '0-10'),
        Datum(True, True, True, True, True, 'Full', '$', False, False, 'Burger', '30-60'))


def impurity(data):
    """
    :param data: A sequence of Datum objects.
    :return: The Gini impurity of the data, as per equation 6.1 on p. 197 of Géron.
    """
    samples = len(data)
    if samples == 0:
        return 1 #return worst possible value, needed for best_split
    trues = 0
    for datum in data:
        if datum.target:
            trues +=1
    falses = samples - trues
    return 1- (trues/samples)**2 - (falses/samples)**2 #only two classes: true or false, if more classes needed, use a dict


def split_cost(data, attribute, value):
    """
    :param data: A sequence of Datum objects.
    :param attribute: An attribute on which to split.
    :param value: The value to distinguish from other values at this node.
    :return: The cost of splitting in this way, as per equation 6.2 on p. 200 of Géron.
    """
    samples = len(data)
    if samples == 0:
        return float('inf') #return worst possible value, needed for best_split
    happend = []
    not_happened = []
    for datum in data:
        if datum.attributes[attribute] == value:
            happend.append(datum)
        else:
            not_happened.append(datum)
    g1 = impurity(happend) #gini score of the subsets
    g2 = impurity(not_happened)
    return (len(happend)/samples * g1)+(len(not_happened)/samples *g2) #formula in book



def best_split(data):
    """
    :param data: A sequence of Datum objects.
    :return: The best attribute and value to split on at this node.
    """

    living_map = {}
    for datum in data:
        for k,v in datum.attributes.items():
            if k not in living_map:
                living_map[k] = [v]
            else:
                if v not in living_map[k]:
                    living_map[k].append(v)
    """
    Creates a dictionary which maps attributes to an array of values. 
    works because it captures every attribute, and every value for that attribute, present in the data.
    useful because if new data is added the map will capture it
    Alternatively could put this inside the tree object as self.map or something
     
    I'd argue it only adds a constant coefficient amount of time to the complexity since it takes len(data) time and realistically
    there are other functions that are doing this same time complexity: if you have n time + n time you get 2n time which is just n time complexity  
    """

    best_attribute = None
    best_val = None
    best_cost = float('inf')

    for att in ATTRIBUTES:
        for val in living_map[att]:
            cost = split_cost(data, att, val)
            if cost < best_cost:
                best_cost = cost
                best_val = val
                best_attribute = att
    return best_attribute, best_val


class Tree:
    def __init__(self, data, max_depth = float('inf')): #default to no max depth
        if impurity(data) == 0 or max_depth == 0:
            self.prediction = data[0].target
            self.left = None
            self.right = None
        else:
            self.prediction = None
            self.attribute, self.value = best_split(data)
            sub1 = []
            sub2 = []
            for datum in data:
                if datum.attributes[self.attribute] == self.value:
                    sub1.append(datum)
                else:
                    sub2.append(datum)
            self.left = Tree(sub1, max_depth-1)
            self.right = Tree(sub2, max_depth-1)

    def __str__(self, indent = ''): #initial indent of no space
        if self.prediction is not None:
            return indent + str(self.prediction) + '\n'
        else:
            return indent + str(self.attribute) + '==' + str(self.value) + '\n' + self.left.__str__(indent + '  ') + self.right.__str__(indent + '  ')


    def predict(self, datum):
        """
        :param datum: A Datum object.
        :return: The tree's prediction for the attribute values of datum.
        """
        if self.prediction is not None:
            return self.prediction
        if datum.attributes[self.attribute] == self.value:
            return self.left.predict(datum)
        else:
            return self.right.predict(datum)

def main():
    tree = Tree(data, 4)
    print(tree)

if __name__ == '__main__':
    main()
