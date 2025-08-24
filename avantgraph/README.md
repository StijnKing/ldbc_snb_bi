
# AvantGraph Implementation for LDBC SNB BI Workload

This directory contains an implementation of the [LDBC Social Network Benchmark Business Intelligence (BI) workload](https://ldbcouncil.org/ldbc_snb_docs/ldbc-snb-specification.pdf) using [AvantGraph](https://github.com/AvantGraph/avantgraph), a modern graph database system with Meta Property Graph (MPG) support.

## Overview

AvantGraph is a high-performance graph database that supports the Meta Property Graph (MPG) model, making it well-suited for complex analytical workloads like the LDBC SNB BI benchmark. This implementation leverages AvantGraph's native MPG capabilities to efficiently represent and query the social network data.

**Important:** This implementation extends the original LDBC SNB BI dataset by automatically generating and adding reified sub-structures. This extension transforms the standard property graph data into a richer Meta Property Graph format, enabling more sophisticated relationship modeling and querying capabilities.

## Scientific Purpose and Research Context

This implementation serves as a **starting benchmark for the Meta Property Graph (MPG) data model** in graph databases. It is designed for **scientific research purposes** to:

- Evaluate the performance and expressiveness of MPG systems compared to traditional property graph databases
- Provide an initial benchmark for measuring MPG-specific features like native reification support
- Enable research into advanced graph analytical workloads that benefit from meta-property modeling

The reification extensions added to the original dataset are specifically designed to showcase MPG capabilities and provide meaningful benchmark scenarios for this emerging graph data model.

## Prerequisites

- Docker (for running AvantGraph container)
- Python 3.x
- Generated LDBC SNB BI dataset in JSON format

## Data Generation

First, generate the dataset using the [LDBC SNB Datagen Spark](https://github.com/ldbc/ldbc_snb_datagen_spark/) repository:

```bash
./tools/run.py -- --format json --scale-factor 0.3 --mode bi --explode-attrs --explode-edges
```

## Setup and Loading

### Environment Configuration

The AvantGraph container image can be configured using the `AG_IMAGE` environment variable:

```bash
# Use default image
./seed.sh

# Use custom image
AG_IMAGE=your-custom-image:tag ./seed.sh
```

### Data Loading

Run the seeding script to prepare and load the data:

```bash
./seed.sh
```

This script performs the following operations:
1. Merges loose JSON files into a single graph file
2. Transforms the data into AvantGraph's import format
3. Creates the graph schema with vertices and edges
4. **Generates and adds reification data structures** to extend the original dataset with MPG-specific features
5. Loads the complete enhanced dataset into AvantGraph using the provided image

## Architecture

### Schema Design

The implementation creates a comprehensive MPG schema that includes:

**Vertex Types:**
- `Person`: Social network users with demographic information
- `Post`/`Comment`: Messages in the network (with reification)
- `Forum`: Discussion groups
- `Organisation`: Companies and universities
- `Place`: Geographic locations (countries, cities, continents)
- `Tag`/`TagClass`: Content categorization

**Edge Types:**
- Social relationships: `knows`, `likes`
- Content relationships: `hasCreator`, `hasTag`, `replyOf`
- Geographic relationships: `isLocatedIn`, `isPartOf`
- Organizational relationships: `studyAt`, `workAt`
- Forum relationships: `hasMember`, `hasModerator`, `containerOf`

## Benchmarking

### Running Queries

Execute individual BI queries using the query implementations:

```python
python3 benchmark.py --scale_factor 0.3 [--test]
```

**Options:**
- `--scale_factor`: Specify the scale factor used for data generation
- `--test`: Run in test mode (1 query per batch)

## Performance Notes

- AvantGraph's MPG model provides efficient support for the complex relationship patterns in SNB BI
- Reification is handled natively within AvantGraph
- The implementation takes advantage of AvantGraph's analytical query optimization

## Troubleshooting

If you encounter issues:

1. **Container execution errors**: Ensure Docker is running and the AvantGraph image is accessible
2. **Schema creation failures**: Check that the data files are properly mounted in the container
3. **Query timeouts**: Consider adjusting the scale factor or query parameters

For more information, consult the [AvantGraph documentation](https://github.com/avantlab/avantgraph) and the [LDBC SNB BI specification](https://ldbcouncil.org/ldbc_snb_docs/ldbc-snb-specification.pdf).

