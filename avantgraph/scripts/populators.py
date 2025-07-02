
import json
import os
import random


class ReifiedData:
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.label_sets = []
        self.properties = []


class Populator:
    def __init__ (self, data_file):
        self.data_file = data_file
        self.entries = []

    def populate(self):
        if not os.path.exists(self.data_file):
            print(f"Data file {self.data_file} does not exist.")
            return
        
        with open(self.data_file, 'r') as f:
            for line in f:
                entry = json.loads(line.strip())
                if isinstance(entry, dict) and 'id' in entry:
                    self._append_entry(entry)

        return self
    
    def _append_entry(self, entry):
        """
        Append a single entry to the entries list.
        """
        self.entries.append({"id": str(entry['id'])})

    def select_random_entries(self, data, count=10):
        """
        Select a random sample of entries from the populated data.
        """
        if not self.entries:
            print("No entries to select from in: {}.".format(self.__class__.__name__))
            return []

        count = round(random.randint(1, count))
        
        data.nodes.extend(random.sample(self.entries, min(count, len(self.entries))))
        return data


class EdgePopulator(Populator):
    def __init__(self, data_file):
        super().__init__(data_file)

    def _append_entry(self, entry):
        """
        Append a single entry to the entries list with tags.
        """
        knows_entry = {
            "id": str(entry['id']),
            'source_id': str(entry['start']['id']),
            'target_id': str(entry['end']['id']),
        }
        self.entries.append(knows_entry)
        

    def select_random_entries(self, data, count=5):
        """
        Select a random sample of 'knows' relationships from the populated data.
        """
        if not self.entries:
            print("No entries to select from in: {}.".format(self.__class__.__name__))
            return []
        
        count = round(random.randint(1, count))

        selected_edges = random.sample(self.entries, min(count, len(self.entries)))
        data.edges.extend([{"id": entry['id']} for entry in selected_edges])

        # Select about 25% of the nodes
        nodes = set()
        for entry in selected_edges:
            nodes.add(entry['source_id'])
            nodes.add(entry['target_id'])

        node_ids = random.sample(list(nodes), min(len(nodes), round(len(nodes) * 0.25)))
        
        # Convert nodes to a list of dictionaries
        data.nodes.extend([{'id': node_id} for node_id in node_ids])
        
        return data
    
class PopulatorFactory:
    def __init__(self):
        self.populators = {}

    @staticmethod
    def create_populator(input_dir):
        """
        Factory method to create a populator based on the dataset type.
        """
        p = PopulatorFactory()
        
        nodes = ["Person.json"]
        for node in nodes:
            name = node.split('.')[0]
            data_file = os.path.join(input_dir, node)
            p.register_populator(name, Populator(data_file).populate())

        edges = ["knows.json", "organisationisLocatedIn.json"]
        for edge in edges:
            name = edge.split('.')[0]
            data_file = os.path.join(input_dir, edge)
            p.register_populator(name, EdgePopulator(data_file).populate())

        return p
    
    def register_populator(self, name, populator_class):
        """
        Register a new populator class.
        """
        if name in self.populators:
            raise ValueError(f"Populator for {name} already exists.")
        
        self.populators[name] = populator_class
    
    def generate_data(self):
        """
        Generates random data and returns it as a ReifiedData object.
        """
        data = ReifiedData()
        for _, populator in self.populators.items():
            # 10% chance to select random entries
            if random.random() > 0.1:
                continue
            
            random_entries = populator.select_random_entries(data, 10)
            if random_entries:
                data.nodes.extend(random_entries.nodes)
                data.edges.extend(random_entries.edges)
                data.label_sets.extend(random_entries.label_sets)
                data.properties.extend(random_entries.properties)

        return data
