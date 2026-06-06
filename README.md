# Introduction to Bioinformatics Databases & Big Data

### 1. Bioinformatics Database
- **Bioinformatics** is the science of collecting, storing, organizing and analyzing biological data using computational tools and statistical method to gain meaningful insights.
- **Central Dogma Omics Data:**
```
Genomics -> Transciptomics -> Proteomics
(genome)    (transriptome)    (protein)
```
- **Biosignals** is the time series of physiological processes.
- **Biometrics** is the data of fingerprints, facial geometry and retinal scan used in identification.
- **Centres of Excellence (CoE):**
    - National Center for Biotechnology Institute (NCBI)
    - European Bioinformatics Institute (EMBL-EBI)
    - National Institute of Genetics (NGI)
- **Workflow in bioinformatics:**
```
    Data sotrage <- Source data from experiments and discoveries
                 <-> Data analysed and processed using computational method and algorithm
                 <-> Analysis result used for further interpretation and visualization
                 <-> Multiple data used for integrated analysis and knowledge sharing
```

### 2. Biological Big Data
- **5V**
    | 5V | Description
    | --- | --- |
    | Volume | Massive amounts of data generated |
    | Velocity | Speed of generation of data |
    | Veracity | Quality and reliability of the data | 
    | Value | Meaningful and able to generate actiionable insights |
    | Variety | Multiple formats and structures |

- **Chanllenges in Biological Data Management**
    | Chanllenges | Description
    | --- | --- |
    | Heterogeneity | biolofical data vary in structures and completeness, and a fixed schema cannot handle the complexity |
    | Versioning | Biological data is not static and versioning is needed for update and query |
    | Integration and interoperability | Absence of globally  agreed identifiers for biological entities | 
    | Scale and performance | Standard relational database may not be adequate for intensive workloads |

# Relational Databases for Biological Big Data

### 1. ACID (Relational DB)
- **ACID**
    | ACID | Discription |
    | --- | --- |
    | Atomicity | A transaction is either completes fully or not at all |
    | Consistency | A transaction moves the database from one valid state to another |
    | Isolation | Concurrent transactions do not interfere with each other |
    | Durability | Committed data survives crashes |

- **Costs of ACID**
    | Costs | Discription |
    | --- | --- |
    | Locking mechanism | Ensure atomicity and isolation by preventing concurrent access |
    | Index lookup | Maintain consistency by performing index lookup on every insert |
    | Transaction logs | Ensure durability by requiring physical logging before confirming the commit |

- **Limitations of Relational DB**
    | Limitations | Discription |
    | --- | --- |
    | Schema rigidity | Heterogenous biological data cannot be stored in fixed uniform relational table |
    | JOIN operation | Joining massive biological data stored in different tables costs time and space |
    | Schema evolution | Advancement in biological knowledge requires modification of DB schema, which can be risky and slow |

### 2. CAP Theorem (Distributed DB)
- **CAP**
    | CAP | Description |
    | --- | --- |
    | Consistency | Every read returns the most recent writes |
    | Availability | Every request receives a non-error response |
    | Partition Tolerance | System continues operating despite network failures |

- At most **2/3 of CAP**
    - **CP** (No availability): Rejects request to prevent reading the wrong data
    - **AP** (No consistency): Answers request with stale data to stay online

### 3. BASE Model (NoSQL)
    | BASE | Description |
    | --- | --- |
    | Basically Available | System guarantees availability | 
    | Soft State | Data states change as replica independently converge over time |
    | Eventually consistent | All replicas will eventually converge to the identical value |

# Introduction to NoSQL
### 1. NoSQL
- **NoSQL** is DBMS that is designed to handle large volume, unstructured or semi-structured data suitable for big data apps and real-time web apps.

- **Characteristics of NoSQL**
    | Characteristics | Description |
    | --- | --- |
    | Schema Flexibility | Handle evolving data structures |
    | Horizontal Scalability | Distribute across multiple servers or nodes to handle heavy traffic |
    | High Performance | Offer faster read and write operations, especially for large scale apps |
    | Various Data Models | Such as file-based, graph, key-value |
    | Distributed Architecture | Run on cluster for high availabiltity |

- **Types of NoSQL**
    | Types | Description |
    | --- | --- |
    | Document-oriented | JSON-liked documents with flexible fields per document, suitable for hierarchical or nested data |
    | Key-value | Key-value pairs, supporting high speed lookups, suitable for caching or session storage |
    | Column family | Optimized for heavy workloads and time-series data |
    | Graph | Store entities in nodes and relationships in edges, suitable for modeling biological networks |

### 2. SQL vs NoSQL
    | Aspects | SQL | NoSQL |
    | --- | --- | --- |
    | Data Model | Structured and tabular with predefined schema | Flexible and dynamic schema |
    | Consistency Model | Strong consistency (ACID) | Eventually consistent (BASE) |
    | Data Relationships | Strong support via join and foreign key | Limited for join, denormalized data |
    | Examples | MySQL, PostgreSQL, Oracle | MongoDB, Redis, Cassandra |

### 3. Characteristics of Biological Database
    | Characteristics | Description | Needs |
    | --- | --- | --- |
    | High Volume | Data is generated in massive quantity | Scalable storage and fast access |
    | Heterogenous | Data comes in various sources and modalities | Flexible schema |
    | Flexible in Structure | Data evolves over time and frequent updates | Dynamic fields |

# Introduction to MongoDB

# MongoDB: Querying

# MongoDB Aggregation FrameWork

# Application Programming Interface