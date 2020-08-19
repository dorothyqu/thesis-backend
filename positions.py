
import networkx as nx

oldmin = -1
oldmax = 1
newmin = 0
newmax = 1000

# change the scale to match the canvas
def get_new_value(old):
    return (((old - oldmin) * (newmax - newmin)) / (oldmax - oldmin)) + newmin

# returns a list of tuples (x,y) locations
def get_locations(n, p):
    G = nx.fast_gnp_random_graph(n, p)
    pos = nx.spring_layout(G)
    locations = []
    for node in pos.values():
        # x and y values
        xy = get_new_value(node[0]), get_new_value(node[1])
        locations.append(xy)
    # nx.draw(G)
    # print(locations)
    # plt.show()
    return locations