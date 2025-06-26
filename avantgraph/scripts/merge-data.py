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
            "type": "node",
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
            "type": "relationship",
            "id": str(self.id),
            "label": self.label,
            "start": self.start,
            "end": self.end,
            "properties": self.properties
        }

# All dynamic convertes
class CommentConverter(BasicNode):
    def __init__(self):
        super().__init__()
        self.labels = ["Comment"]
        self.property_keys = ["creationDate", "locationIP", "browserUsed", "content", "length"]

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

class CommentHasTagConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "hasTag"
        self.start["labels"] = ["Comment"]
        self.end["labels"] = ["Tag"]
        self.property_keys = ["creationDate"]

    def convert(self, data):
        self.start["id"] = str(data.get('CommentId'))
        self.end["id"] = str(data.get('TagId'))
        return super().convert(data)

class CommentIsLocatedInContryConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "isLocatedIn"
        self.start["labels"] = ["Comment"]
        self.end["labels"] = ["Place"]
        self.property_keys = ["creationDate"]

    def convert(self, data):
        self.start["id"] = str(data.get('CommentId'))
        self.end["id"] = str(data.get('CountryId'))
        return super().convert(data)

class CommentReplyOfCommentConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "replyOf"
        self.start["labels"] = ["Comment"]
        self.end["labels"] = ["Comment"]
        self.property_keys = ["creationDate"]
    
    def convert(self, data):
        self.start["id"] = str(data.get('CommentId'))
        self.end["id"] = str(data.get('ReplyOfCommentId'))
        return super().convert(data)
    
class CommentReplyOfPostConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "replyOf"
        self.start["labels"] = ["Comment"]
        self.end["labels"] = ["Post"]
        self.property_keys = ["creationDate"]

    def convert(self, data):
        self.start["id"] = str(data.get('CommentId'))
        self.end["id"] = str(data.get('PostId'))
        return super().convert(data)
    
class ForumConverter(BasicNode):
    def __init__(self):
        super().__init__()
        self.labels = ["Forum"]
        self.property_keys = ["creationDate", "title"]

class ForumContainerOfPostConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "containerOf"
        self.start["labels"] = ["Forum"]
        self.end["labels"] = ["Post"]
        self.property_keys = ["creationDate"]

    def convert(self, data):
        self.start["id"] = str(data.get('ForumId'))
        self.end["id"] = str(data.get('PostId'))
        return super().convert(data)
    
class ForumHasMemberPersonConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "hasMember"
        self.start["labels"] = ["Forum"]
        self.end["labels"] = ["Person"]
        self.property_keys = ["creationDate"]

    def convert(self, data):
        self.start["id"] = str(data.get('ForumId'))
        self.end["id"] = str(data.get('PersonId'))
        return super().convert(data)
    
class ForumHasModeratorPersonConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "hasModerator"
        self.start["labels"] = ["Forum"]
        self.end["labels"] = ["Person"]
        self.property_keys = ["creationDate"]

    def convert(self, data):
        self.start["id"] = str(data.get('ForumId'))
        self.end["id"] = str(data.get('PersonId'))
        return super().convert(data)
    
class ForumHasTagConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "hasTag"
        self.start["labels"] = ["Forum"]
        self.end["labels"] = ["Tag"]
        self.property_keys = ["creationDate"]

    def convert(self, data):
        self.start["id"] = str(data.get('ForumId'))
        self.end["id"] = str(data.get('TagId'))
        return super().convert(data)

class PersonConverter(BasicNode):
    def __init__(self):
        super().__init__()
        self.labels = ["Person"]
        self.property_keys = ["creationDate", "firstName", "lastName", "gender", "birthday", "locationIP", "browserUsed", "language", "email"]

class PersonHasInterestTagConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "hasInterest"
        self.start["labels"] = ["Person"]
        self.end["labels"] = ["Tag"]
        self.property_keys = ["creationDate"]

    def convert(self, data):
        self.start["id"] = str(data.get('PersonId'))
        self.end["id"] = str(data.get('TagId'))
        return super().convert(data)
    
class PersonIsLocatedInCityConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "isLocatedIn"
        self.start["labels"] = ["Person"]
        self.end["labels"] = ["Place"]
        self.property_keys = ["creationDate"]

    def convert(self, data):
        self.start["id"] = str(data.get('PersonId'))
        self.end["id"] = str(data.get('CityId'))
        return super().convert(data)
    
class PersonKnowsPersonConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "knows"
        self.start["labels"] = ["Person"]
        self.end["labels"] = ["Person"]
        self.property_keys = ["creationDate"]

    def convert(self, data):
        self.start["id"] = str(data.get('PersonId'))
        self.end["id"] = str(data.get('KnowsPersonId'))
        return super().convert(data)
    
class PersonLikesCommentConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "likes"
        self.start["labels"] = ["Person"]
        self.end["labels"] = ["Comment"]
        self.property_keys = ["creationDate"]

    def convert(self, data):
        self.start["id"] = str(data.get('PersonId'))
        self.end["id"] = str(data.get('CommentId'))
        return super().convert(data)
    
class PersonLikesPostConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "likes"
        self.start["labels"] = ["Person"]
        self.end["labels"] = ["Post"]
        self.property_keys = ["creationDate"]
        
    def convert(self, data):
        self.start["id"] = str(data.get('PersonId'))
        self.end["id"] = str(data.get('PostId'))
        return super().convert(data)
    
class PersonStudyAtUniversityConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "studyAt"
        self.start["labels"] = ["Person"]
        self.end["labels"] = ["Organisation"]
        self.property_keys = ["creationDate", "classYear"]

    def convert(self, data):
        self.start["id"] = str(data.get('PersonId'))
        self.end["id"] = str(data.get('UniversityId'))
        return super().convert(data)
    
class PersonWorkAtCompanyConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "workAt"
        self.start["labels"] = ["Person"]
        self.end["labels"] = ["Organisation"]
        self.property_keys = ["creationDate", "workFrom"]

    def convert(self, data):
        self.start["id"] = str(data.get('PersonId'))
        self.end["id"] = str(data.get('CompanyId'))
        return super().convert(data)
    
class PostConverter(BasicNode):
    def __init__(self):
        super().__init__()
        self.labels = ["Post"]
        self.property_keys = ["creationDate", "imageFile", "locationIP", "browserUsed", "content", "length"]

class PostHasCreatorPersonConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "hasCreator"
        self.start["labels"] = ["Post"]
        self.end["labels"] = ["Person"]
        self.property_keys = ["creationDate"]

    def convert(self, data):
        self.start["id"] = str(data.get('PostId'))
        self.end["id"] = str(data.get('PersonId'))
        return super().convert(data)
    
class PostHasTagConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "hasTag"
        self.start["labels"] = ["Post"]
        self.end["labels"] = ["Tag"]
        self.property_keys = ["creationDate"]

    def convert(self, data):
        self.start["id"] = str(data.get('PostId'))
        self.end["id"] = str(data.get('TagId'))
        return super().convert(data)
    
class PostIsLocatedInCountryConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "isLocatedIn"
        self.start["labels"] = ["Post"]
        self.end["labels"] = ["Place"]
        self.property_keys = ["creationDate"]

    def convert(self, data):
        self.start["id"] = str(data.get('PostId'))
        self.end["id"] = str(data.get('CountryId'))
        return super().convert(data)

# Additional static convertes
class OrganisationConverter(BasicNode):
    def __init__(self):
        super().__init__()
        self.labels = ["Organisation"]
        self.property_keys = ["type", "name", "url"]

class OrganisationIsLocatedInPlaceConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "isLocatedIn"
        self.start["labels"] = ["Organisation"]
        self.end["labels"] = ["Place"]
        self.property_keys = []

    def convert(self, data):
        self.start["id"] = str(data.get('OrganisationId'))
        self.end["id"] = str(data.get('PlaceId'))
        return super().convert(data)
    
class PlaceConverter(BasicNode):
    def __init__(self):
        super().__init__()
        self.labels = ["Place"]
        self.property_keys = ["name", "url", "type"]

class PlaceIsPartOfPlaceConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "isPartOf"
        self.start["labels"] = ["Place"]
        self.end["labels"] = ["Place"]
        self.property_keys = []

    def convert(self, data):
        self.start["id"] = str(data.get('PlaceId'))
        self.end["id"] = str(data.get('PartOfPlaceId'))
        return super().convert(data)
    
class TagConverter(BasicNode):
    def __init__(self):
        super().__init__()
        self.labels = ["Tag"]
        self.property_keys = ["name", "url"]

class TagHasTypeTagClassConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "hasType"
        self.start["labels"] = ["Tag"]
        self.end["labels"] = ["TagClass"]
        self.property_keys = []

    def convert(self, data):
        self.start["id"] = str(data.get('TagId'))
        self.end["id"] = str(data.get('TagClassId'))
        return super().convert(data)
    
class TagClassConverter(BasicNode):
    def __init__(self):
        super().__init__()
        self.labels = ["TagClass"]
        self.property_keys = ["name", "url"]

class TagClassIsSubclassOfTagClassConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "isSubclassOf"
        self.start["labels"] = ["TagClass"]
        self.end["labels"] = ["TagClass"]
        self.property_keys = []

    def convert(self, data):
        self.start["id"] = str(data.get('TagClass1Id'))
        self.end["id"] = str(data.get('TagClass2Id'))
        return super().convert(data)

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
}, {
    "layer": "dynamic",
    "name": "Comment_hasTag_Tag",
    "converter": CommentHasTagConverter(),
}, {
    "layer": "dynamic",
    "name": "Comment_isLocatedIn_Country",
    "converter": CommentIsLocatedInContryConverter(),
}, {
    "layer": "dynamic",
    "name": "Comment_replyOf_Comment",
    "converter": CommentReplyOfCommentConverter(),
}, {
    "layer": "dynamic",
    "name": "Comment_replyOf_Post",
    "converter": CommentReplyOfPostConverter(),
}, {
    "layer": "dynamic",
    "name": "Forum",
    "converter": ForumConverter(),
}, {
    "layer": "dynamic",
    "name": "Forum_containerOf_Post",
    "converter": ForumContainerOfPostConverter(),
}, {
    "layer": "dynamic",
    "name": "Forum_hasMember_Person",
    "converter": ForumHasMemberPersonConverter(),
}, {
    "layer": "dynamic",
    "name": "Forum_hasModerator_Person",
    "converter": ForumHasModeratorPersonConverter(),
}, {
    "layer": "dynamic",
    "name": "Forum_hasTag_Tag",
    "converter": ForumHasTagConverter(),
}, {
    "layer": "dynamic",
    "name": "Person_hasInterest_Tag",
    "converter": PersonHasInterestTagConverter(),
}, {
    "layer": "dynamic",
    "name": "Person_isLocatedIn_City",
    "converter": PersonIsLocatedInCityConverter(),
}, {
    "layer": "dynamic",
    "name": "Person_knows_Person",
    "converter": PersonKnowsPersonConverter(),
}, {
    "layer": "dynamic",
    "name": "Person_likes_Comment",
    "converter": PersonLikesCommentConverter(),
}, {
    "layer": "dynamic",
    "name": "Person_likes_Post",
    "converter": PersonLikesPostConverter(),
}, {
    "layer": "dynamic",
    "name": "Person_studyAt_University",
    "converter": PersonStudyAtUniversityConverter(),
}, {
    "layer": "dynamic",
    "name": "Person_workAt_Company",
    "converter": PersonWorkAtCompanyConverter(),
}, {
    "layer": "dynamic",
    "name": "Post",
    "converter": PostConverter(),
}, {
    "layer": "dynamic",
    "name": "Post_hasCreator_Person",
    "converter": PostHasCreatorPersonConverter(),
}, {
    "layer": "dynamic",
    "name": "Post_hasTag_Tag",
    "converter": PostHasTagConverter(),
}, {
    "layer": "dynamic",
    "name": "Post_isLocatedIn_Country",
    "converter": PostIsLocatedInCountryConverter(),
}, {
    "layer": "static",
    "name": "Organisation",
    "converter": OrganisationConverter(),
}, {
    "layer": "static",
    "name": "Organisation_isLocatedIn_Place",
    "converter": OrganisationIsLocatedInPlaceConverter(),
}, {
    "layer": "static",
    "name": "Place",
    "converter": PlaceConverter(),
}, {
    "layer": "static",
    "name": "Place_isPartOf_Place",
    "converter": PlaceIsPartOfPlaceConverter(),
}, {
    "layer": "static",
    "name": "Tag",
    "converter": TagConverter(),
}, {
    "layer": "static",
    "name": "Tag_hasType_TagClass",
    "converter": TagHasTypeTagClassConverter(),
}, {
    "layer": "static",
    "name": "TagClass",
    "converter": TagClassConverter(),
}, {
    "layer": "static",
    "name": "TagClass_isSubclassOf_TagClass",
    "converter": TagClassIsSubclassOfTagClassConverter(),
}]


def merge_json_files(input_dir, output_file):

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
