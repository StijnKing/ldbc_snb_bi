
class BasicNode:
    def __init__(self):
        self.id = None
        self.labels = []
        self.properties = {}

    def convert(self, data):
        self.id = data.get('id')
        for key in self.property_keys:
            if key in data:
                if key == 'length':
                    self.properties[key] = int(data[key])
                else:
                    self.properties[key] = str(data[key])

        return {
            "type": "node",
            "id": self.__class__.id_prefix + str(self.id),
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


# All dynamic convertes
class CommentConverter(BasicNode):
    id_prefix = ""

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
        self.start["id"] = CommentConverter.id_prefix + str(data.get('CommentId'))
        self.end["id"] = PersonConverter.id_prefix + str(data.get('PersonId'))
        return super().convert(data)

class CommentHasTagConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "hasTag"
        self.start["labels"] = CommentConverter().labels
        self.end["labels"] = TagConverter().labels
        self.property_keys = ["creationDate"]

    def convert(self, data):
        self.start["id"] = CommentConverter.id_prefix + str(data.get('CommentId'))
        self.end["id"] = TagConverter.id_prefix + str(data.get('TagId'))
        return super().convert(data)

class CommentIsLocatedInContryConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "isLocatedIn"
        self.start["labels"] = CommentConverter().labels
        self.end["labels"] = ["Place", "Country"]
        self.property_keys = ["creationDate"]

    def convert(self, data):
        self.start["id"] = CommentConverter.id_prefix + str(data.get('CommentId'))
        self.end["id"] = PlaceConverter.id_prefix + str(data.get('CountryId'))
        return super().convert(data)

class CommentReplyOfCommentConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "replyOf"
        self.start["labels"] = CommentConverter().labels
        self.end["labels"] = CommentConverter().labels
        self.property_keys = ["creationDate"]
    
    def convert(self, data):
        self.start["id"] = CommentConverter.id_prefix + str(data.get('CommentId'))
        self.end["id"] = CommentConverter.id_prefix + str(data.get('ReplyOfCommentId'))
        return super().convert(data)
    
class CommentReplyOfPostConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "replyOf"
        self.start["labels"] = CommentConverter().labels
        self.end["labels"] = PostConverter().labels
        self.property_keys = ["creationDate"]

    def convert(self, data):
        self.start["id"] = CommentConverter.id_prefix + str(data.get('CommentId'))
        self.end["id"] = PostConverter.id_prefix + str(data.get('PostId'))
        return super().convert(data)
    
class ForumConverter(BasicNode):
    id_prefix = "forum"

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
        self.start["id"] = ForumConverter.id_prefix + str(data.get('ForumId'))
        self.end["id"] = PostConverter.id_prefix + str(data.get('PostId'))
        return super().convert(data)
    
class ForumHasMemberPersonConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "hasMember"
        self.start["labels"] = ForumConverter().labels
        self.end["labels"] = PersonConverter().labels
        self.property_keys = ["creationDate"]

    def convert(self, data):
        self.start["id"] = ForumConverter.id_prefix + str(data.get('ForumId'))
        self.end["id"] = PersonConverter.id_prefix + str(data.get('PersonId'))
        return super().convert(data)
    
class ForumHasModeratorPersonConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "hasModerator"
        self.start["labels"] = ForumConverter().labels
        self.end["labels"] = PersonConverter().labels
        self.property_keys = ["creationDate"]

    def convert(self, data):
        self.start["id"] = ForumConverter.id_prefix + str(data.get('ForumId'))
        self.end["id"] = PersonConverter.id_prefix + str(data.get('PersonId'))
        return super().convert(data)
    
class ForumHasTagConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "hasTag"
        self.start["labels"] = ForumConverter().labels
        self.end["labels"] = TagConverter().labels
        self.property_keys = ["creationDate"]

    def convert(self, data):
        self.start["id"] = ForumConverter.id_prefix + str(data.get('ForumId'))
        self.end["id"] = TagConverter.id_prefix + str(data.get('TagId'))
        return super().convert(data)

class PersonConverter(BasicNode):
    id_prefix = "person"

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
        self.start["id"] = PersonConverter.id_prefix + str(data.get('PersonId'))
        self.end["id"] = TagConverter.id_prefix + str(data.get('TagId'))
        return super().convert(data)
    
class PersonIsLocatedInCityConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "isLocatedIn"
        self.start["labels"] = PersonConverter().labels
        self.end["labels"] = ["Place", "City"]
        self.property_keys = ["creationDate"]

    def convert(self, data):
        self.start["id"] = PersonConverter.id_prefix + str(data.get('PersonId'))
        self.end["id"] = PlaceConverter.id_prefix + str(data.get('CityId'))
        return super().convert(data)
    
class PersonKnowsPersonConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "knows"
        self.start["labels"] = PersonConverter().labels
        self.end["labels"] = PersonConverter().labels
        self.property_keys = ["creationDate"]

    def convert(self, data):
        self.start["id"] = PersonConverter.id_prefix + str(data.get('Person1Id'))
        self.end["id"] = PersonConverter.id_prefix + str(data.get('Person2Id'))
        return super().convert(data)
    
class PersonLikesCommentConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "likes"
        self.start["labels"] = PersonConverter().labels
        self.end["labels"] = CommentConverter().labels
        self.property_keys = ["creationDate"]

    def convert(self, data):
        self.start["id"] = PersonConverter.id_prefix + str(data.get('PersonId'))
        self.end["id"] = CommentConverter.id_prefix + str(data.get('CommentId'))
        return super().convert(data)
    
class PersonLikesPostConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "likes"
        self.start["labels"] = PersonConverter().labels
        self.end["labels"] = PostConverter().labels
        self.property_keys = ["creationDate"]
        
    def convert(self, data):
        self.start["id"] = PersonConverter.id_prefix + str(data.get('PersonId'))
        self.end["id"] = PostConverter.id_prefix + str(data.get('PostId'))
        return super().convert(data)
    
class PersonStudyAtUniversityConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "studyAt"
        self.start["labels"] = PersonConverter().labels
        self.end["labels"] = ["University", "Organisation"]
        self.property_keys = ["creationDate", "classYear"]

    def convert(self, data):
        self.start["id"] = PersonConverter.id_prefix + str(data.get('PersonId'))
        self.end["id"] = OrganisationConverter.id_prefix + str(data.get('UniversityId'))
        return super().convert(data)
    
class PersonWorkAtCompanyConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "workAt"
        self.start["labels"] = PersonConverter().labels
        self.end["labels"] = ["Company", "Organisation"]
        self.property_keys = ["creationDate", "workFrom"]

    def convert(self, data):
        self.start["id"] = PersonConverter.id_prefix + str(data.get('PersonId'))
        self.end["id"] = OrganisationConverter.id_prefix + str(data.get('CompanyId'))
        return super().convert(data)
    
class PostConverter(BasicNode):
    id_prefix = ""

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
        self.start["id"] = PostConverter.id_prefix + str(data.get('PostId'))
        self.end["id"] = PersonConverter.id_prefix + str(data.get('PersonId'))
        return super().convert(data)
    
class PostHasTagConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "hasTag"
        self.start["labels"] = PostConverter().labels
        self.end["labels"] = TagConverter().labels
        self.property_keys = ["creationDate"]

    def convert(self, data):
        self.start["id"] = PostConverter.id_prefix + str(data.get('PostId'))
        self.end["id"] = TagConverter.id_prefix + str(data.get('TagId'))
        return super().convert(data)
    
class PostIsLocatedInCountryConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "isLocatedIn"
        self.start["labels"] = PostConverter().labels
        self.end["labels"] = ["Place", "Country"]
        self.property_keys = ["creationDate"]

    def convert(self, data):
        self.start["id"] = PostConverter.id_prefix + str(data.get('PostId'))
        self.end["id"] = PlaceConverter.id_prefix + str(data.get('CountryId'))
        return super().convert(data)

# Additional static convertes
class OrganisationConverter(BasicNode):
    id_prefix = "organisation"
    mapping = {}  # Maps unique ID to "Company" or "University"

    def __init__(self):
        super().__init__()
        self.labels = ["Organisation"]
        self.property_keys = ["name", "url"]

    def convert(self, data):
        node = super().convert(data)
        node["labels"] = ["Organisation", data["type"]]
        OrganisationConverter.mapping[str(node["id"])] = data["type"]
        return node

class OrganisationIsLocatedInPlaceConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "isLocatedIn"
        self.start["labels"] = None
        self.end["labels"] = None
        self.property_keys = []

    def convert(self, data):
        self.start["id"] = OrganisationConverter.id_prefix + str(data.get('OrganisationId'))
        self.end["id"] = PlaceConverter.id_prefix + str(data.get('PlaceId'))

        type = OrganisationConverter.mapping.get(OrganisationConverter.id_prefix + str(data.get('OrganisationId')))
        assert type is not None, "Organisation type not found in mapping."

        if type == "Company":
            self.start["labels"] = ["Organisation", "Company"]
            self.end["labels"] = ["Place", "Country"]
        else:
            self.start["labels"] = ["Organisation", "University"]
            self.end["labels"] = ["Place", "City"]

        return super().convert(data)
    
class PlaceConverter(BasicNode):
    id_prefix = "place"
    places = {}  # Maps unique ID to "City" or "Country"

    def __init__(self):
        super().__init__()
        self.labels = ["Place"]
        self.property_keys = ["name", "url"]

    def convert(self, data):
        node = super().convert(data)
        node["labels"] = ["Place", data["type"]]
        
        PlaceConverter.places[str(node["id"])] = data["type"]

        return node

class PlaceIsPartOfPlaceConverter(BasicRelationship):
    def __init__(self):
        super().__init__()
        self.label = "isPartOf"
        self.start["labels"] = None
        self.end["labels"] = None
        self.property_keys = []

    def convert(self, data):
        self.start["id"] = PlaceConverter.id_prefix + str(data.get('Place1Id'))
        self.end["id"] = PlaceConverter.id_prefix + str(data.get('Place2Id'))
        edge = super().convert(data)
        edge["start"]["labels"] = ["Place", PlaceConverter.places.get(PlaceConverter.id_prefix + str(data.get('Place1Id')))]
        edge["end"]["labels"] = ["Place", PlaceConverter.places.get(PlaceConverter.id_prefix + str(data.get('Place2Id')))]
        return edge
    
class TagConverter(BasicNode):
    id_prefix = "tag"

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
        self.start["id"] = TagConverter.id_prefix + str(data.get('TagId'))
        self.end["id"] = TagClassConverter.id_prefix + str(data.get('TagClassId'))
        return super().convert(data)
    
class TagClassConverter(BasicNode):
    id_prefix = "tagclass"

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
        self.start["id"] = TagClassConverter.id_prefix + str(data.get('TagClass1Id'))
        self.end["id"] = TagClassConverter.id_prefix + str(data.get('TagClass2Id'))
        return super().convert(data)
