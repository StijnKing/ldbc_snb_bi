import os
import json
import sys

from converters import (
    CommentConverter,
    PersonConverter,
    ForumConverter,
    PostConverter,
    PlaceConverter,
    TagClassConverter,
    TagConverter,
    OrganisationConverter,
    CommentHasCreatorPersonConverter,
    CommentHasTagConverter,
    CommentIsLocatedInContryConverter,
    CommentReplyOfCommentConverter,
    CommentReplyOfPostConverter,
    ForumContainerOfPostConverter,
    ForumHasMemberPersonConverter,
    ForumHasModeratorPersonConverter,
    ForumHasTagConverter,
    PersonHasInterestTagConverter,
    PersonIsLocatedInCityConverter,
    PersonKnowsPersonConverter,
    PersonLikesCommentConverter,
    PersonLikesPostConverter,
    PersonStudyAtUniversityConverter,
    PersonWorkAtCompanyConverter,
    PostHasCreatorPersonConverter,
    PostHasTagConverter,
    PostIsLocatedInCountryConverter,
    OrganisationIsLocatedInPlaceConverter,
    PlaceIsPartOfPlaceConverter,
    TagHasTypeTagClassConverter,
    TagClassIsSubclassOfTagClassConverter
)

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
    "name": "Forum",
    "converter": ForumConverter(),
}, {
    "layer": "dynamic",
    "name": "Post",
    "converter": PostConverter(),
}, {
    "layer": "static",
    "name": "Place",
    "converter": PlaceConverter(),
}, {
    "layer": "static",
    "name": "TagClass",
    "converter": TagClassConverter(),
}, {
    "layer": "static",
    "name": "Tag",
    "converter": TagConverter(),
}, {
    "layer": "static",
    "name": "Organisation",
    "converter": OrganisationConverter(),
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
    "name": "Organisation_isLocatedIn_Place",
    "converter": OrganisationIsLocatedInPlaceConverter(),
}, {
    "layer": "static",
    "name": "Place_isPartOf_Place",
    "converter": PlaceIsPartOfPlaceConverter(),
}, {
    "layer": "static",
    "name": "Tag_hasType_TagClass",
    "converter": TagHasTypeTagClassConverter(),
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
