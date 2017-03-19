import googlemaps
from itertools import combinations
from pathlib import Path
import pandas as pd
import numpy as np
import random
from deap import algorithms, base, creator, tools
from tqdm import tqdm
from pprint import pprint as pp
import os


class TehranUniversityTrip:

    way_points_name = [
        'University of Tehran, Tehran, Tehran Province',
        'Sharif University of Technology, Tehran',
        'Shahid Beheshti University, Daneshjou Boulevard, Tehran, Tehran Province',
        'Amirkabir University of Technology (Polytechnic), Rasht Street, Tehran, Tehran Province',
        'Iran University of Science and Technology',
        'K. N. Toosi University of Technology, Mirdamad Boulevard, Tehran, Tehran Province',
        'Allameh Tabataba’i University, Tehran, Tehran Province',
        'imam hossein university',
        'Imam Sadiq University, Tehran, Tehran Province',
        'Iran University of Medical Sciences',
        'Malek Ashtar University of Technology, Shabanlou, Tehran, Tehran Province',
        'Tarbiat Modares University, Tehran, Tehran Province',
        'Shahed University, Tehran, Tehran Province',
        'Kharazmi University, Tehran, Tehran Province',
        'Alzahra University',
        'Imam Ali University, Emam Khomeyni Street, Tehran, Tehran Province',
        'Institute for management and planning studies, Shafei, Tehran, Tehran Province',
        'Institute for Studies in Theoretical Physics and Mathematics',
        'Iran Polymer and Petrochemical Institute',
        'Police University Amin',
        'shahid rajaee teacher training university'
    ]

    def __init__(self):
        self.way_point_distances = {}
        self.way_point_durations = {}
        self.all_way_points = set()
        self.raw_data_name = 'data.tsv'

    def fetch_way_points_data(self):
        gmap = googlemaps.Client(open('.api_key').read())
        for (wp1, wp2) in combinations(self.way_points_name, 2):
            route = gmap.distance_matrix(origins=[wp1],
                                         destinations=[wp2],
                                         language='English',
                                         mode='driving',
                                         units='metric')
            distance = route['rows'][0]['elements'][0]['distance']['value']
            duration = route['rows'][0]['elements'][0]['duration']['value'] / 60.
            self.way_point_distances[frozenset([wp1, wp2])] = distance
            self.way_point_durations[frozenset([wp1, wp2])] = duration
            self._persist_data()

    def _persist_data(self):
        with open(self.raw_data_name, 'w') as f:
            f.write('\t'.join(['way_point_1', 'way_point_2', 'distance_meters', 'duration_minutes']))
            for wp1, wp2 in self.way_point_distances:
                f.write('\n')
                f.write('\t'.join([
                    wp1,
                    wp2,
                    str(self.way_point_distances[frozenset([wp1, wp2])]),
                    str(self.way_point_durations[frozenset([wp1, wp2])])
                ]))

    def get_data_file(self):
        file = Path(self.raw_data_name)
        if file.is_file():
            return file
        else:
            print("Fetching Data From Google ...")
            self.fetch_way_points_data()
            return file

    def get_data(self):
        way_points_data = pd.read_csv(self.get_data_file().absolute(), sep="\t")
        for i, row in way_points_data.iterrows():
            self.way_point_distances[frozenset([row.way_point_1, row.way_point_2])] = row.distance_meters
            self.way_point_durations[frozenset([row.way_point_1, row.way_point_2])] = row.duration_minutes
            self.all_way_points.update([row.way_point_1, row.way_point_2])
        return self


class GenerateOptimizeRoute:

    total_gens = 400

    def __init__(self, data):
        self.all_way_points = data.all_way_points
        self.way_point_durations = data.way_point_durations
        self.way_point_distances = data.way_point_distances
        self.toolbox = base.Toolbox()
        self.stats = tools.Statistics()
        self.pbar = tqdm(total=self.total_gens)
        self.hof = tools.ParetoFront(similar=self._pareto_eq)

    def _create_tools(self):
        creator.create('FitnessMulti', base.Fitness, weights=(1.0, -1.0))
        creator.create('Individual', list, fitness=creator.FitnessMulti)
        self.toolbox.register('way_points', random.sample, self.all_way_points, random.randint(2, 21))
        self.toolbox.register('individual', tools.initIterate, creator.Individual, self.toolbox.way_points)
        self.toolbox.register('population', tools.initRepeat, list, self.toolbox.individual)

    def run_genetic_algorithm(self):
        self._create_tools()
        self.toolbox.register('evaluate', self._eval_trip)
        self.toolbox.register('mutate', self._mutation_operator)
        self.toolbox.register('select', self._pareto_selection_operator)
        pop = self.toolbox.population(n=1000)
        self.stats.register('Progress', lambda x: self.pbar.update())
        algorithms.eaSimple(
            pop, self.toolbox, cxpb=0., mutpb=1.0, ngen=self.total_gens,
            stats=self.stats, halloffame=self.hof, verbose=False
        )
        self.pbar.close()
        self.create_animated_road_trip_map(reversed(self.hof))

    @staticmethod
    def _pareto_eq(ind1, ind2):
        return np.all(ind1.fitness.values == ind2.fitness.values)

    @staticmethod
    def _pareto_selection_operator(individuals, k):
        return tools.selNSGA2(individuals, int(k / 5.)) * 5

    def _eval_trip(self, individual):
        trip_length = 0.
        individual = list(individual)
        individual += [individual[0]]
        for index in range(1, len(individual)):
            wp1 = individual[index - 1]
            wp2 = individual[index]
            trip_length += self.way_point_distances[frozenset([wp1, wp2])]
        return len(set(individual)), trip_length

    def _mutation_operator(self, individual):
        possible_mutations = ['swap']

        if len(individual) < len(self.all_way_points):
            possible_mutations.append('insert')
            possible_mutations.append('point')
        if len(individual) > 2:
            possible_mutations.append('delete')

        mutation_type = random.sample(possible_mutations, 1)[0]

        if mutation_type == 'insert':
            waypoint_to_add = individual[0]
            while waypoint_to_add in individual:
                waypoint_to_add = random.sample(self.all_way_points, 1)[0]

            index_to_insert = random.randint(0, len(individual) - 1)
            individual.insert(index_to_insert, waypoint_to_add)

        elif mutation_type == 'delete':
            index_to_delete = random.randint(0, len(individual) - 1)
            del individual[index_to_delete]

        elif mutation_type == 'point':
            waypoint_to_add = individual[0]
            while waypoint_to_add in individual:
                waypoint_to_add = random.sample(self.all_way_points, 1)[0]

            index_to_replace = random.randint(0, len(individual) - 1)
            individual[index_to_replace] = waypoint_to_add

        elif mutation_type == 'swap':
            index1 = random.randint(0, len(individual) - 1)
            index2 = index1
            while index2 == index1:
                index2 = random.randint(0, len(individual) - 1)

            individual[index1], individual[index2] = individual[index2], individual[index1]

        return individual,

    @staticmethod
    def create_animated_road_trip_map(optimized_routes):
        optimized_routes = [list(route) + [route[0]] for route in optimized_routes]
        html_template = open('./html_template.html').read()
        with open('tehran-universities-animated-map.html', 'w') as output_file:
            html_template = html_template.replace('@@PLACE_HOLDER@@', ''.join(
                ['allRoutes.push({});'.format(str(route)) for route in optimized_routes]))
            output_file.write(html_template)


pp(GenerateOptimizeRoute(TehranUniversityTrip().get_data()).run_genetic_algorithm())
os.system('open tehran-universities-animated-map.html')
