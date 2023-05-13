import math

DEBUG_VISUALS = False

BLOCK = False
if BLOCK:
    ANT_LENGTH = 18
    ANT_WIDTH = 8
else:
    ANT_LENGTH = 30
    ANT_WIDTH = 22

ANT_PIVOT = 0.5

MOVEMENT_SPEED = 1
TURNING_SPEED = 0.1  # Was 0.1
TURN_PROBABILITY = 0.01

ANT_HILL_COLOR = (170, 120, 35)
ANT_HILL_X = 600
ANT_HILL_Y = 200
ANT_HILL_RADIUS = 40

MAX_ANTS = 100
ANT_EVERY = 20
TICKS = 60

PHEROMONE_RADIUS = 10
PH_GRID = PHEROMONE_RADIUS
MAX_PHEROMONES = 100
PHEROMONE_LIFE = 500

PREDATOR_WIDTH = 80
PREDATOR_LENGTH = 160
PREDATOR_PIVOT = 0.5
PREDATOR_X = 150
PREDATOR_Y = 550
PREDATOR_TURN_PROBABILITY = 0.003

ANT_ESCAPING_SPEEDUP = 1.4
PREDATOR_DETECTION = 2

FOOD_LIFE = 51

GRAPH = [
    ((932, 142), [1]),
    ((600, 200), [0, 2, 21]),
    ((456, 128), [1, 3]),
    ((268, 185), [2, 4]),
    ((146, 123), [3, 5]),
    ((100, 200), [4, 6]),
    ((104, 303), [5, 7]),
    ((152, 389), [6, 8]),
    ((341, 389), [7, 9, 10]),
    ((370, 309), [8]),  # _|_
    ((418, 432), [8, 11]),
    ((416, 509), [10, 12, 14]),
    ((235, 535), [11, 13]),  # L
    ((118, 580), [12]),
    ((580, 578), [11, 15]),  # R
    ((685, 552), [14, 16]),
    ((761, 454), [15, 17]),
    ((843, 442), [16, 18, 19]),
    ((1013, 572), [17]),  # R
    ((854, 362), [17, 20, 21]),  # L
    ((936, 331), [19]),  # _|_
    ((600, 300), [19, 1]),
]


# Written based on pseudo code from Wikipedia
def Dijkstra(source_idx):
    dist = [math.inf for _ in range(len(GRAPH))]
    prev = [None for _ in range(len(GRAPH))]
    queue = set(idx for idx in range(len(GRAPH)))
    dist[source_idx] = 0

    while len(queue) > 0:
        min_idx, min_dist = min([(idx, dist[idx]) for idx in queue], key=lambda x: x[1])
        queue.remove(min_idx)

        for neighbor in GRAPH[min_idx][1]:
            if neighbor in queue:
                alt = dist[min_idx] + 1
                if alt < dist[neighbor]:
                    dist[neighbor] = alt
                    prev[neighbor] = min_idx

    return dist, prev


ah_dist, ah_prev = Dijkstra(1)
AntHillDijkstra = {'dist': ah_dist, 'prev': ah_prev}



def get_nearest_point(x, y):
    min_dist = math.inf
    nearest_point = None
    for point, _ in GRAPH:
        dist = (point[0] - x) ** 2 + (point[1] - y) ** 2
        if dist < min_dist:
            min_dist = dist
            nearest_point = point
    return nearest_point


def get_dist(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
