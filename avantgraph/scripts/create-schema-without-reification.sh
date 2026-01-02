#!/bin/bash

GRAPH_FILE=${GRAPH_FILE:-/data/snb-bi}

rm $GRAPH_FILE -r  || true

mkdir $GRAPH_FILE

# Create schema & load data
ag-schema create-graph $GRAPH_FILE

# Create vertex table
ag-schema create-vertex-table $GRAPH_FILE --vertex-label=Comment --vertex-label=Message --vertex-property=id=CHAR_STRING --vertex-property=creationDate=CHAR_STRING --vertex-property=locationIP=CHAR_STRING --vertex-property=browserUsed=CHAR_STRING --vertex-property=content=CHAR_STRING --vertex-property=length=S64
ag-schema create-vertex-table $GRAPH_FILE --vertex-label=Person --vertex-property=id=CHAR_STRING --vertex-property=creationDate=CHAR_STRING --vertex-property=firstName=CHAR_STRING --vertex-property=lastName=CHAR_STRING --vertex-property=gender=CHAR_STRING --vertex-property=birthday=CHAR_STRING --vertex-property=locationIP=CHAR_STRING --vertex-property=browserUsed=CHAR_STRING --vertex-property=language=CHAR_STRING --vertex-property=email=CHAR_STRING
ag-schema create-vertex-table $GRAPH_FILE --vertex-label=Post --vertex-label=Message --vertex-property=id=CHAR_STRING --vertex-property=imageFile=CHAR_STRING --vertex-property=locationIP=CHAR_STRING --vertex-property=browserUsed=CHAR_STRING --vertex-property=content=CHAR_STRING --vertex-property=length=S64
ag-schema create-vertex-table $GRAPH_FILE --vertex-label=Forum --vertex-property=id=CHAR_STRING --vertex-property=creationDate=CHAR_STRING --vertex-property=title=CHAR_STRING

# Static
ag-schema create-vertex-table $GRAPH_FILE --vertex-label=Organisation --vertex-label=Company --vertex-property=id=CHAR_STRING --vertex-property=name=CHAR_STRING --vertex-property=url=CHAR_STRING
ag-schema create-vertex-table $GRAPH_FILE --vertex-label=Organisation --vertex-label=University --vertex-property=id=CHAR_STRING --vertex-property=name=CHAR_STRING --vertex-property=url=CHAR_STRING
ag-schema create-vertex-table $GRAPH_FILE --vertex-label=Place --vertex-label=Country --vertex-property=id=CHAR_STRING --vertex-property=name=CHAR_STRING --vertex-property=url=CHAR_STRING
ag-schema create-vertex-table $GRAPH_FILE --vertex-label=Place --vertex-label=City --vertex-property=id=CHAR_STRING --vertex-property=name=CHAR_STRING --vertex-property=url=CHAR_STRING
ag-schema create-vertex-table $GRAPH_FILE --vertex-label=Place --vertex-label=Continent --vertex-property=id=CHAR_STRING --vertex-property=name=CHAR_STRING --vertex-property=url=CHAR_STRING
ag-schema create-vertex-table $GRAPH_FILE --vertex-label=Tag --vertex-property=id=CHAR_STRING --vertex-property=name=CHAR_STRING --vertex-property=url=CHAR_STRING
ag-schema create-vertex-table $GRAPH_FILE --vertex-label=TagClass --vertex-property=id=CHAR_STRING --vertex-property=name=CHAR_STRING --vertex-property=url=CHAR_STRING

# Create edge tables
ag-schema create-edge-table $GRAPH_FILE --edge-label=hasCreator --src-labels=Comment --src-labels=Message --trg-labels=Person --edge-property=creationDate=CHAR_STRING --edge-property=id=CHAR_STRING
ag-schema create-edge-table $GRAPH_FILE --edge-label=hasTag --src-labels=Comment --src-labels=Message --trg-labels=Tag --edge-property=creationDate=CHAR_STRING --edge-property=id=CHAR_STRING
ag-schema create-edge-table $GRAPH_FILE --edge-label=isLocatedIn --src-labels=Comment --src-labels=Message --trg-labels=Place --trg-labels=Country --edge-property=creationDate=CHAR_STRING --edge-property=id=CHAR_STRING
ag-schema create-edge-table $GRAPH_FILE --edge-label=replyOf --src-labels=Comment --src-labels=Message --trg-labels=Comment --trg-labels=Message --edge-property=creationDate=CHAR_STRING --edge-property=id=CHAR_STRING
ag-schema create-edge-table $GRAPH_FILE --edge-label=replyOf --src-labels=Comment --src-labels=Message --trg-labels=Post --trg-labels=Message --edge-property=creationDate=CHAR_STRING --edge-property=id=CHAR_STRING
ag-schema create-edge-table $GRAPH_FILE --edge-label=containerOf --src-labels=Forum --trg-labels=Post --trg-labels=Message --edge-property=creationDate=CHAR_STRING --edge-property=id=CHAR_STRING
ag-schema create-edge-table $GRAPH_FILE --edge-label=hasMember --src-labels=Forum --trg-labels=Person --edge-property=creationDate=CHAR_STRING --edge-property=id=CHAR_STRING
ag-schema create-edge-table $GRAPH_FILE --edge-label=hasModerator --src-labels=Forum --trg-labels=Person --edge-property=creationDate=CHAR_STRING --edge-property=id=CHAR_STRING
ag-schema create-edge-table $GRAPH_FILE --edge-label=hasTag --src-labels=Forum --trg-labels=Tag --edge-property=creationDate=CHAR_STRING --edge-property=id=CHAR_STRING
ag-schema create-edge-table $GRAPH_FILE --edge-label=hasInterest --src-labels=Person --trg-labels=Tag --edge-property=creationDate=CHAR_STRING --edge-property=id=CHAR_STRING
ag-schema create-edge-table $GRAPH_FILE --edge-label=isLocatedIn --src-labels=Person --trg-labels=Place --trg-labels=City --edge-property=creationDate=CHAR_STRING --edge-property=id=CHAR_STRING
ag-schema create-edge-table $GRAPH_FILE --edge-label=knows --src-labels=Person --trg-labels=Person --edge-property=creationDate=CHAR_STRING --edge-property=id=CHAR_STRING
ag-schema create-edge-table $GRAPH_FILE --edge-label=likes --src-labels=Person --trg-labels=Comment --trg-labels=Message --edge-property=creationDate=CHAR_STRING --edge-property=id=CHAR_STRING
ag-schema create-edge-table $GRAPH_FILE --edge-label=likes --src-labels=Person --trg-labels=Post --trg-labels=Message --edge-property=creationDate=CHAR_STRING --edge-property=id=CHAR_STRING
ag-schema create-edge-table $GRAPH_FILE --edge-label=studyAt --src-labels=Person --trg-labels=Organisation --trg-labels=University --edge-property=creationDate=CHAR_STRING --edge-property=id=CHAR_STRING
ag-schema create-edge-table $GRAPH_FILE --edge-label=workAt --src-labels=Person --trg-labels=Organisation --trg-labels=Company --edge-property=creationDate=CHAR_STRING --edge-property=id=CHAR_STRING --edge-property=workFrom=CHAR_STRING
ag-schema create-edge-table $GRAPH_FILE --edge-label=hasCreator --src-labels=Post --src-labels=Message --trg-labels=Person --edge-property=creationDate=CHAR_STRING --edge-property=id=CHAR_STRING
ag-schema create-edge-table $GRAPH_FILE --edge-label=hasTag --src-labels=Post --src-labels=Message --trg-labels=Tag --edge-property=creationDate=CHAR_STRING --edge-property=id=CHAR_STRING
ag-schema create-edge-table $GRAPH_FILE --edge-label=isLocatedIn --src-labels=Post --src-labels=Message --trg-labels=Place --trg-labels=Country --edge-property=creationDate=CHAR_STRING --edge-property=id=CHAR_STRING

# Static
ag-schema create-edge-table $GRAPH_FILE --edge-label=isLocatedIn --src-labels=Organisation --src-labels=Company --trg-labels=Place --trg-labels=Country --edge-property=id=CHAR_STRING
ag-schema create-edge-table $GRAPH_FILE --edge-label=isLocatedIn --src-labels=Organisation --src-labels=University --trg-labels=Place --trg-labels=City --edge-property=id=CHAR_STRING
ag-schema create-edge-table $GRAPH_FILE --edge-label=isPartOf --src-labels=Place --src-labels=City --trg-labels=Place --trg-labels=Country --edge-property=id=CHAR_STRING
ag-schema create-edge-table $GRAPH_FILE --edge-label=isPartOf --src-labels=Place --src-labels=Country --trg-labels=Place --trg-labels=Continent --edge-property=id=CHAR_STRING
ag-schema create-edge-table $GRAPH_FILE --edge-label=hasType --src-labels=Tag --trg-labels=TagClass --edge-property=id=CHAR_STRING
ag-schema create-edge-table $GRAPH_FILE --edge-label=isSubclassOf --src-labels=TagClass --trg-labels=TagClass --edge-property=id=CHAR_STRING
