import os
import json
import sys


class BasicNode:
    def __init__(self):
        self.id = None
        self.labels = []
        self.properties = {}

    def convert(self, data):
        self.id = data.get('id')
        for key in self.property_keys:
            if key in data:
                self.properties[key] = str(data[key])

        return {
            "id": str(self.id),
            "labels": self.labels,
            "properties": self.properties
        }
    
class BasicRelationship:
    def __init__(self):
        self.next_id = 1
        self.id = None
        self.label = None
        self.start = {"labels": [], "id": None}
        self.end = {"labels": [], "id": None}
        self.properties = {}

    def convert(self, data):
        self.id = self.next_id
        self.next_id += 1
        for key in self.property_keys:
            if key in data:
                self.properties[key] = str(data[key])

        return {
            "id": str(self.id),
            "label": self.label,
            "start": self.start,
            "end": self.end,
            "properties": self.properties
        }



class CommentConverter(BasicNode):
    def __init__(self):
        super().__init__()
        self.labels = ["Comment"]
        self.property_keys = ["creationDate", "locationIP", "browserUsed", "content", "length"]

class PersonConverter(BasicNode):
    def __init__(self):
        super().__init__()
        self.labels = ["Person"]
        self.property_keys = ["creationDate", "firstName", "lastName", "gender", "birthday", "locationIP", "browserUsed", "language", "email"]

class CommentHasCreatorPersonConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "hasCreator"
        self.start["labels"] = ["Comment"]
        self.end["labels"] = ["Person"]
        self.property_keys = ["creationDate"]

    def convert(self, data):
        self.start["id"] = str(data.get('CommentId'))
        self.end["id"] = str(data.get('PersonId'))
        return super().convert(data)

def merge_json_files(input_dir, output_file):
    imports = [{
        "layer": "dynamic",
        "name": "Comment",
        "converter": CommentConverter(),
    }, {
        "layer": "dynamic",
        "name": "Person",
        "converter": PersonConverter(),
    }, {
        "layer": "dynamic",
        "name": "Comment_hasCreator_Person",
        "converter": CommentHasCreatorPersonConverter(),
    }]

    # Clean input file if exists
    if os.path.exists(output_file):
        os.remove(output_file)

    # Write merged data to output file
    print(f"Writing merged data to {output_file}")
    with open(output_file, 'w', encoding='utf-8') as out:
        for object in imports:
            root = object['layer']
            key = object['name']
            input_folder = os.path.join(input_dir, root, key)
            for filename in os.listdir(input_folder):
                if filename.endswith('.json'):
                    file_path = os.path.join(input_folder, filename)
                    print(f"Processing file: {file_path}")
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            origional = json.loads(line.strip())
                            # Convert the data if a converter is defined
                            converter = object['converter']
                            converted = converter.convert(origional)
                            out.write(json.dumps(converted, ensure_ascii=False) + '\n')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input_dir> <output_file>")
        sys.exit(1)
    input_dir = sys.argv[1]
    output_file = sys.argv[2]
    merge_json_files(input_dir, output_file)
