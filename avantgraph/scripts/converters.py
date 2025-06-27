
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
    next_id = 1

    def __init__(self):
        self.id = None
        self.label = None
        self.start = {"labels": [], "id": None}
        self.end = {"labels": [], "id": None}
        self.properties = {}

    def convert(self, data):
        self.id = BasicRelationship.next_id
        BasicRelationship.next_id += 1
        for key in self.property_keys:
            if key in data:
                self.properties[key] = str(data[key])

        self.properties["id"] = str(self.id)

        return {
            "type": "relationship",
            "id": str(self.id),
            "label": self.label,
            "start": self.start,
            "end": self.end,
            "properties": self.properties
        }

class ReificationNode(BasicNode):
    def __init__(self):
        super().__init__()
        self.reified_nodes = []
        self.reified_edges = []
        self.reified_label_sets = []
        self.reified_properties = []

    def populate_reified_data(self):
        pass

    def convert(self, data):
        self.populate_reified_data()
        data = super().convert(data)

        data["reified_nodes"] = self.reified_nodes
        data["reified_edges"] = self.reified_edges
        data["reified_label_sets"] = self.reified_label_sets
        data["reified_properties"] = self.reified_properties

        return data

# All dynamic convertes
class CommentConverter(ReificationNode):
    def __init__(self):
        super().__init__()
        self.labels = ["Comment", "Message"]
        self.property_keys = ["creationDate", "locationIP", "browserUsed", "content", "length"]

class CommentHasCreatorPersonConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "hasCreator"
        self.start["labels"] = CommentConverter().labels
        self.end["labels"] = PersonConverter().labels
        self.property_keys = ["creationDate"]

    def convert(self, data):
        self.start["id"] = str(data.get('CommentId'))
        self.end["id"] = str(data.get('PersonId'))
        return super().convert(data)

class CommentHasTagConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "hasTag"
        self.start["labels"] = CommentConverter().labels
        self.end["labels"] = TagConverter().labels
        self.property_keys = ["creationDate"]

    def convert(self, data):
        self.start["id"] = str(data.get('CommentId'))
        self.end["id"] = str(data.get('TagId'))
        return super().convert(data)

class CommentIsLocatedInContryConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "isLocatedIn"
        self.start["labels"] = CommentConverter().labels
        self.end["labels"] = PlaceConverter().labels
        self.property_keys = ["creationDate"]

    def convert(self, data):
        self.start["id"] = str(data.get('CommentId'))
        self.end["id"] = str(data.get('CountryId'))
        return super().convert(data)

class CommentReplyOfCommentConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "replyOf"
        self.start["labels"] = CommentConverter().labels
        self.end["labels"] = CommentConverter().labels
        self.property_keys = ["creationDate"]
    
    def convert(self, data):
        self.start["id"] = str(data.get('CommentId'))
        self.end["id"] = str(data.get('ReplyOfCommentId'))
        return super().convert(data)
    
class CommentReplyOfPostConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "replyOf"
        self.start["labels"] = CommentConverter().labels
        self.end["labels"] = PostConverter().labels
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
        self.start["labels"] = ForumConverter().labels
        self.end["labels"] = PostConverter().labels
        self.property_keys = ["creationDate"]

    def convert(self, data):
        self.start["id"] = str(data.get('ForumId'))
        self.end["id"] = str(data.get('PostId'))
        return super().convert(data)
    
class ForumHasMemberPersonConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "hasMember"
        self.start["labels"] = ForumConverter().labels
        self.end["labels"] = PersonConverter().labels
        self.property_keys = ["creationDate"]

    def convert(self, data):
        self.start["id"] = str(data.get('ForumId'))
        self.end["id"] = str(data.get('PersonId'))
        return super().convert(data)
    
class ForumHasModeratorPersonConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "hasModerator"
        self.start["labels"] = ForumConverter().labels
        self.end["labels"] = PersonConverter().labels
        self.property_keys = ["creationDate"]

    def convert(self, data):
        self.start["id"] = str(data.get('ForumId'))
        self.end["id"] = str(data.get('PersonId'))
        return super().convert(data)
    
class ForumHasTagConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "hasTag"
        self.start["labels"] = ForumConverter().labels
        self.end["labels"] = TagConverter().labels
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
        self.start["labels"] = PersonConverter().labels
        self.end["labels"] = TagConverter().labels
        self.property_keys = ["creationDate"]

    def convert(self, data):
        self.start["id"] = str(data.get('PersonId'))
        self.end["id"] = str(data.get('TagId'))
        return super().convert(data)
    
class PersonIsLocatedInCityConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "isLocatedIn"
        self.start["labels"] = PersonConverter().labels
        self.end["labels"] = PlaceConverter().labels
        self.property_keys = ["creationDate"]

    def convert(self, data):
        self.start["id"] = str(data.get('PersonId'))
        self.end["id"] = str(data.get('CityId'))
        return super().convert(data)
    
class PersonKnowsPersonConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "knows"
        self.start["labels"] = PersonConverter().labels
        self.end["labels"] = PersonConverter().labels
        self.property_keys = ["creationDate"]

    def convert(self, data):
        self.start["id"] = str(data.get('PersonId'))
        self.end["id"] = str(data.get('KnowsPersonId'))
        return super().convert(data)
    
class PersonLikesCommentConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "likes"
        self.start["labels"] = PersonConverter().labels
        self.end["labels"] = CommentConverter().labels
        self.property_keys = ["creationDate"]

    def convert(self, data):
        self.start["id"] = str(data.get('PersonId'))
        self.end["id"] = str(data.get('CommentId'))
        return super().convert(data)
    
class PersonLikesPostConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "likes"
        self.start["labels"] = PersonConverter().labels
        self.end["labels"] = PostConverter().labels
        self.property_keys = ["creationDate"]
        
    def convert(self, data):
        self.start["id"] = str(data.get('PersonId'))
        self.end["id"] = str(data.get('PostId'))
        return super().convert(data)
    
class PersonStudyAtUniversityConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "studyAt"
        self.start["labels"] = PersonConverter().labels
        self.end["labels"] = OrganisationConverter().labels
        self.property_keys = ["creationDate", "classYear"]

    def convert(self, data):
        self.start["id"] = str(data.get('PersonId'))
        self.end["id"] = str(data.get('UniversityId'))
        return super().convert(data)
    
class PersonWorkAtCompanyConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "workAt"
        self.start["labels"] = PersonConverter().labels
        self.end["labels"] = OrganisationConverter().labels
        self.property_keys = ["creationDate", "workFrom"]

    def convert(self, data):
        self.start["id"] = str(data.get('PersonId'))
        self.end["id"] = str(data.get('CompanyId'))
        return super().convert(data)
    
class PostConverter(ReificationNode):
    def __init__(self):
        super().__init__()
        self.labels = ["Post", "Message"]
        self.property_keys = ["creationDate", "imageFile", "locationIP", "browserUsed", "content", "length"]

class PostHasCreatorPersonConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "hasCreator"
        self.start["labels"] = PostConverter().labels
        self.end["labels"] = PersonConverter().labels
        self.property_keys = ["creationDate"]

    def convert(self, data):
        self.start["id"] = str(data.get('PostId'))
        self.end["id"] = str(data.get('PersonId'))
        return super().convert(data)
    
class PostHasTagConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "hasTag"
        self.start["labels"] = PostConverter().labels
        self.end["labels"] = TagConverter().labels
        self.property_keys = ["creationDate"]

    def convert(self, data):
        self.start["id"] = str(data.get('PostId'))
        self.end["id"] = str(data.get('TagId'))
        return super().convert(data)
    
class PostIsLocatedInCountryConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "isLocatedIn"
        self.start["labels"] = PostConverter().labels
        self.end["labels"] = PlaceConverter().labels
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
        self.start["labels"] = OrganisationConverter().labels
        self.end["labels"] = PlaceConverter().labels
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
        self.start["labels"] = PlaceConverter().labels
        self.end["labels"] = PlaceConverter().labels
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
        self.start["labels"] = TagConverter().labels
        self.end["labels"] = TagClassConverter().labels
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
        self.start["labels"] = TagClassConverter().labels
        self.end["labels"] = TagClassConverter().labels
        self.property_keys = []

    def convert(self, data):
        self.start["id"] = str(data.get('TagClass1Id'))
        self.end["id"] = str(data.get('TagClass2Id'))
        return super().convert(data)
