import os
import json
from random import random
import sys

from populators import PopulatorFactory
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
    "outputName": "Comment"
}, {
    "layer": "dynamic",
    "name": "Person",
    "converter": PersonConverter(),
    "outputName": "Person"
}, {
    "layer": "dynamic",
    "name": "Forum",
    "converter": ForumConverter(),
    "outputName": "Forum"
}, {
    "layer": "dynamic",
    "name": "Post",
    "converter": PostConverter(),
    "outputName": "Post"
}, {
    "layer": "static",
    "name": "Place",
    "converter": PlaceConverter(),
    "outputName": "Place"
}, {
    "layer": "static",
    "name": "TagClass",
    "converter": TagClassConverter(),
    "outputName": "TagClass"
}, {
    "layer": "static",
    "name": "Tag",
    "converter": TagConverter(),
    "outputName": "Tag"
}, {
    "layer": "static",
    "name": "Organisation",
    "converter": OrganisationConverter(),
    "outputName": "Organisation"
}, {
    "layer": "dynamic",
    "name": "Comment_hasCreator_Person",
    "converter": CommentHasCreatorPersonConverter(),
    "outputName": "hasCreator"
}, {
    "layer": "dynamic",
    "name": "Comment_hasTag_Tag",
    "converter": CommentHasTagConverter(),
    "outputName": "hasTag"
}, {
    "layer": "dynamic",
    "name": "Comment_isLocatedIn_Country",
    "converter": CommentIsLocatedInContryConverter(),
    "outputName": "commentisLocatedIn"
}, {
    "layer": "dynamic",
    "name": "Comment_replyOf_Comment",
    "converter": CommentReplyOfCommentConverter(),
    "outputName": "replyOf"
}, {
    "layer": "dynamic",
    "name": "Comment_replyOf_Post",
    "converter": CommentReplyOfPostConverter(),
    "outputName": "replyOf"
}, {
    "layer": "dynamic",
    "name": "Forum_containerOf_Post",
    "converter": ForumContainerOfPostConverter(),
    "outputName": "containerOf"
}, {
    "layer": "dynamic",
    "name": "Forum_hasMember_Person",
    "converter": ForumHasMemberPersonConverter(),
    "outputName": "hasMember"
}, {
    "layer": "dynamic",
    "name": "Forum_hasModerator_Person",
    "converter": ForumHasModeratorPersonConverter(),
    "outputName": "hasModerator"
}, {
    "layer": "dynamic",
    "name": "Forum_hasTag_Tag",
    "converter": ForumHasTagConverter(),
    "outputName": "hasTag"
}, {
    "layer": "dynamic",
    "name": "Person_hasInterest_Tag",
    "converter": PersonHasInterestTagConverter(),
    "outputName": "hasInterest"
}, {
    "layer": "dynamic",
    "name": "Person_isLocatedIn_City",
    "converter": PersonIsLocatedInCityConverter(),
    "outputName": "personisLocatedIn"
}, {
    "layer": "dynamic",
    "name": "Person_knows_Person",
    "converter": PersonKnowsPersonConverter(),
    "outputName": "knows"
}, {
    "layer": "dynamic",
    "name": "Person_likes_Comment",
    "converter": PersonLikesCommentConverter(),
    "outputName": "likes"
}, {
    "layer": "dynamic",
    "name": "Person_likes_Post",
    "converter": PersonLikesPostConverter(),
    "outputName": "likes"
}, {
    "layer": "dynamic",
    "name": "Person_studyAt_University",
    "converter": PersonStudyAtUniversityConverter(),
    "outputName": "studyAt"
}, {
    "layer": "dynamic",
    "name": "Person_workAt_Company",
    "converter": PersonWorkAtCompanyConverter(),
    "outputName": "workAt"
}, {
    "layer": "dynamic",
    "name": "Post_hasCreator_Person",
    "converter": PostHasCreatorPersonConverter(),
    "outputName": "hasCreator"
}, {
    "layer": "dynamic",
    "name": "Post_hasTag_Tag",
    "converter": PostHasTagConverter(),
    "outputName": "hasTag"
}, {
    "layer": "dynamic",
    "name": "Post_isLocatedIn_Country",
    "converter": PostIsLocatedInCountryConverter(),
    "outputName": "postisLocatedIn"
}, {
    "layer": "static",
    "name": "Organisation_isLocatedIn_Place",
    "converter": OrganisationIsLocatedInPlaceConverter(),
    "outputName": "organisationisLocatedIn"
}, {
    "layer": "static",
    "name": "Place_isPartOf_Place",
    "converter": PlaceIsPartOfPlaceConverter(),
    "outputName": "isPartOf"
}, {
    "layer": "static",
    "name": "Tag_hasType_TagClass",
    "converter": TagHasTypeTagClassConverter(),
    "outputName": "hasType"
}, {
    "layer": "static",
    "name": "TagClass_isSubclassOf_TagClass",
    "converter": TagClassIsSubclassOfTagClassConverter(),
    "outputName": "isSubclassOf"
}]

def merge_json_files(input_dir, output_file):
    # Clean input file if exists
    if os.path.exists(output_file):
        os.remove(output_file)

    with open(output_file, 'w', encoding='utf-8') as out:
        for root, _, files in os.walk(input_dir):
            # Sort files to ensure capitalized files are processed first
            files.sort(key=lambda x: (not x[0].isupper(), x))
            for file in files:
                if file.endswith('.json'):
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        for line in f:
                            out.write(line)

def populate_reification_data(working_dir):
    """
    Populate reification data from the input directory and write to output file.
    Only applies for Comment and Post data.
    """
    populator = PopulatorFactory.create_populator(working_dir)

    for file_name in ["Comment.json", "Post.json"]:
        input_file = os.path.join(working_dir, file_name)
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file {input_file} does not exist.")
        
        with open(input_file, 'r', encoding='utf-8') as f:
            with open(os.path.join(working_dir, 'Reified_' + file_name), 'a', encoding='utf-8') as out:
                for line in f:
                    original = json.loads(line.strip())
                    # 25% chance to select random entries
                    if random() > 0.25:
                        out.write(json.dumps(original, ensure_ascii=False) + '\n')
                        continue

                    data = populator.generate_data()
                    original['reified_nodes'] = data.nodes
                    original['reified_edges'] = data.edges
                    original['reified_label_sets'] = data.label_sets
                    original['reified_properties'] = data.properties
                    out.write(json.dumps(original, ensure_ascii=False) + '\n')

    for file_name in ["Comment.json", "Post.json"]:
        # Remove origional file
        input_file = os.path.join(working_dir, file_name)
        if os.path.exists(input_file):
            os.remove(input_file)
        else:
            print(f"Input file {input_file} does not exist, skipping removal.")

def convert_json_file(input_file, output_file, converter):
    """
    Convert a single JSON file using the specified converter.
    """
    if not os.path.exists(input_file):
        print(f"Input file {input_file} does not exist.")
        return

    print(f"Converting {input_file} to {output_file}")
    with open(output_file, 'w', encoding='utf-8') as out:
        with open(input_file, 'r', encoding='utf-8') as f:
            for line in f:
                original = json.loads(line.strip())
                converted = converter.convert(original)
                out.write(json.dumps(converted, ensure_ascii=False) + '\n')

def find_json_file(input_dir):
    """
    Find the json file in the input directory.
    """
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.json'):
                return os.path.join(root, file)
    raise FileNotFoundError(f"No JSON file found in {input_dir}.")

def convert_all_json_files(input_dir, output_dir):
    """
    Convert all JSON files in the input directory using the specified converters.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_folder = os.path.join(output_dir)

    # Clear all files except .gitignore in the output folder
    for file in os.listdir(output_folder):
        if file != '.gitignore':
            file_path = os.path.join(output_folder, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

    for object in imports:
        root = object['layer']
        key = object['name']
        output_file_name = object['outputName'] + '.json'
        input_folder = os.path.join(input_dir, root, key)
        output_file = os.path.join(output_folder, output_file_name)

        if os.path.exists(output_file):
            os.remove(output_file)
        
        if not os.path.exists(input_folder):
            print(f"Input folder {input_folder} does not exist.")
            continue

        converter = object['converter']
        file_path = find_json_file(input_folder)
        convert_json_file(file_path, output_file, converter)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input_dir> <output_file>")
        sys.exit(1)
    input_dir = sys.argv[1]
    output_file = sys.argv[2]

    scratch_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../scratch')

    print(f"Converting JSON files from {input_dir} to {scratch_dir}")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    convert_all_json_files(input_dir, scratch_dir)
    print("Conversion completed.")

    print("Populating reification data...")
    populate_reification_data(scratch_dir)
    print("Reification data populated.")

    # Merge the converted files into a single file for importing
    # This is needed to import all reified IDs into avantgraph
    print("Merging JSON files...")
    merge_json_files(scratch_dir, output_file)
    print(f"Merged data written to {output_file}")
