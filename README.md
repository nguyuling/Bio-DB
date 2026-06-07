(Pleaese use the ⋮☰ to better navigate the contents :)

# T1 — Introduction to Bioinformatics Databases

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

# T2 — Relational Databases for Biological Big Data

### 1. ACID (Relational DB)
- **ACID**
    | ACID | Description |
    | --- | --- |
    | Atomicity | A transaction is either completes fully or not at all |
    | Consistency | A transaction moves the database from one valid state to another |
    | Isolation | Concurrent transactions do not interfere with each other |
    | Durability | Committed data survives crashes |

- **Costs of ACID**
    | Costs | Description |
    | --- | --- |
    | Locking mechanism | Ensure atomicity and isolation by preventing concurrent access |
    | Index lookup | Maintain consistency by performing index lookup on every insert |
    | Transaction logs | Ensure durability by requiring physical logging before confirming the commit |

- **Limitations of Relational DB**
    | Limitations | Description |
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

# T3 — Introduction to NoSQL
### 1. NoSQL
- **NoSQL** is DBMS that is designed to handle large volume, unstructured or semi-structured data suitable for big data apps and real-time web apps.

- **Characteristics of NoSQL:**
    | Characteristics | Description |
    | --- | --- |
    | Schema Flexibility | Handle evolving data structures |
    | Horizontal Scalability | Distribute across multiple servers or nodes to handle heavy traffic |
    | High Performance | Offer faster read and write operations, especially for large scale apps |
    | Various Data Models | Such as file-based, graph, key-value |
    | Distributed Architecture | Run on cluster for high availabiltity |

- **Types of NoSQL:**
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

# T4 — Introduction to MongoDB

### 1. Features
| Features | Description |
| --- | --- |
| Document-oriented Storage | Using BSON, allow complex and nested structure |
| Schema Flexibility | do not require predefined schema and different documents in the same collection can have different structures |
| Scalability | Support horizontal scaling through sharding and distributing data across multiple machiens |
| Powerful Query Language | Support filtering, sorting, aggregation, geospatial queries and full-text search |
| Aggregation Framework | For data transformation and analytics |
| Integration with Modern Tech | Include programming languages and cloud deployment |

### 2. MongoDB Terminologies
```
     Cluster
        ↓
     Database
        ↓
    Collection
        ↓
     Document
```

### 3. Environments
| Environments | Description |
| --- | --- |
| Database Tool (CLI) | Backup, restore, migration |
| Compass (GUI) | Querying, perform basic CRUD and has descriptive analytics on the schema of the collection |
| Shell (CLI) | Default interface for Compass |
| Atlas | Fully managed cloud-hosted database-as-a-service |
| Community Server | Self-managed software |
| Charts | Built-in visualization tool to create dashboards and charts |
| BI Connector | For SQL-based BI tools to query data |

### 4. Import and Export of Collection:
```
                        mongoexport           mongoimport
    MongoDB Collection  —————————————>  JSON  —————————————>  MongoDB Collection
        (Site A)        <—————————————  BSON  <—————————————        (Site B)
                        mongodumb             mongostore
```
- Export
```
mongoexport --uri "mongodb+srv://<username>:<password>@<cluster>.dklylwy.mongodb.net/" --db <db> --collection <collection> --out <file>.json
```

- Import
```
mongoimport --uri "mongodb+srv://<username>:<password>@<cluster>.dklylwy.mongodb.net/" --db <db> --collection <collection> --drop --jsonArray --file <file>.json
```

### 5. Data Modeling
- **Referencing** (normalised): Store relationships between data using references
- **Embedding** (denormalised): Embed all related data into a single document

# T5 — MongoDB: Querying

### 1. Create / insert data
- `insertOne()`: Create a single data
```
    db.<collection>.insertOne(
        { field: value }
    )
```
- `insertMany()`: Create multiple data
```
    db.<collection>.insertMany(
        { field_1: value },
        { field_2: value },
            ⋮
    )
```

### 2. Update data
- `updateMany()`: First parameter is the matching criteris, second paramater is the updated data
```
    db.<collection>.updateMany(
        { field: value },
        { $set: { "field": "value" } }
    )
```

### 3. Find data
- `find()`: Find and select what to show
```
    db.<collection>.find(
        { field: value },
        { _id: 0, name: 1 }
    )
```

### 4. Sort
- `sort()`: 1 is ascending order, -1 is descending order
```
    db.<collection>.sort(
        { age: 1 }
    )
```

### 5. Query operator
- **Comparison operator:**
    - `$eq`: Equal to
    - `$ne`: Not equal to
    - `gt`: Greater than
    - `gte`: Greater than or equal to
    - `lt`: Less than
    - `lte`: Less than or equal to
```
    db.<collection>.<query>({
        <field>: { $op: value,... }
    })
```

- **Logical operator:**
    - `$and`
    - `$or`
    - `$nor`: Negate the query requirement
    - `$not`
```
    db.<collection>.<query>({
        $and/or/nor: [ 
            { statement 1 }, 
            { statement 2 }
        ]
    })
```
```
    db.<collection>.<query>({
        $not: { statement }
    })
```

### 6. Array
- `$all`: Match all, array contains all the specified values
- `$in`: Match at least one , array contains >=1 of the specified values
- `$size`: Size of array must match the specified value
- `$elemMatch`: Array contains the exact element
```
    db.<collection>.<query>({
        <array>: { $all/in: [ value_1, value_2,...] }
    })
```
```
    db.<collection>.<query>({
        <array>: { $size: value }
    })
```
```
    db.<collection>.<query>({
        <array>: { $elemMatch: { <field>: value } }
    })
```

# T6 — MongoDB Aggregation FrameWork
### 1. Aggregation framework
```
    db.<collection>.aggregate([
        { stage_1 },
        { stage_2 },
        ⋮
    ])
```

### 2. Matching
```
    db.<collection>.aggregate([{
        $match: { <field>: value,... }
    }])
```

### 3. Grouping
```
    db.<collection>.aggregate([{
        $group: {
            _id: "$field",
            <new field>: { $avg/sum/mean/max/count: "$field"/1 }
        }
    }])
```

### 4. Projection
```
    db.<collection>.aggregate([{
        $project: {
            <field_1>: 1
            <field_2>: 0
        }
    }])
```

### 5. Sorting
```
    db.<collection>.aggregate([{
        $sort: {
            <field_1>: 1,
            <field_2>: -1
        }
    }])
```

### 6. Limit
```
    db.<collection>.aggregate([{
        $limit: n
    }])
```

### 7. Unwind array
```
    db.<collection>.aggregate([{
        $unwind: "$array"
    }])
```

# T7 — Application Programming Interface

### 1. API
- **API** is a set of rules or protocols or functions that allows software programs to interact with one another.

- **Importance of API:**
    | Importances | Description |
    | --- | --- |
    | Data Accessibility | APIs provide structured way to access data without the need to understand the underlying database structure |
    | Time Efficiency | APIs provide predefined functions for common task |
    | Interoperability | APIs allow communication of different software systems involved in any workflow |
    | Data Consistency | APIs provide standardized rules to access data and hence reduce the risk of errors |
    | Security | APIs implement access controls and validation checks |

- **Types of APIs:**
    - **Web APIs**: Can be accessed over internet using HTTP protocol and are RESTful, data are returned in JSON or XML format.
    - **Library/Package APIs**: Language-specific interfaces like Python libraries that provide function and classes for working with data.

- **APIs workflow:**
    1. Client (program/script/tool) sends a request to the API endpoint.
    2. Server hosting the API receives the request and processes it based on the parameters, then server performs query to the data source at backend.
    3. Server returns the data requested or error notification (if any) to the client as a response.

### 2. RESTful API
- REST is **Representational State Transfer**, which is a set of guiding principles for building web services.

- **Core of REST:**
    | Cores | Description |
    | --- | --- |
    | Client-Server Architecture | Client and server are separated, where client requests data through UI and server handles data storage and processing |
    | Statelessness | Server do not store any session about the client between requests |
    | Uniform Interface (resource-based) | API are built around resources rather than action |
    | Representation | Server do not send the actual database but a representation of the state of the resource |

- **HTTP methods:**
    | Methods | Description |
    | --- | --- |
    | GET (read) | Retrieve data and never change the database |
    | POST (create) | Submit new data to the database |
    | PUT / PATCH (update) | Update existing records, PUT replace entire resource while PATCH update partial fields |
    | DELETE (delete) | Remove specific resources |

- **HTTP status codes:**
<table>
    <thead><tr><th colspan="2">Status codes</th><th>Description</th></tr></thead>
    <tbody>
        <tr><td rowspan="2">Success</td><td>200 OK</td><td>Successful HTTP request</td></tr>
        <tr><td>201 Created</td><td>Successful request and new resource was created</td></tr>
        <tr><td rowspan="3">Client Error</td><td>400 Bad Request</td><td>Server cannot understand the request due to invalid syntax</td></tr>
        <tr><td>404 Not Found</td><td>Server cannot find the requested resource</td></tr>
        <tr><td>422 Unprocessable Content</td><td>Data in JASON failed validation</td></tr>
        <tr><td>Server Error</td><td>500 Internal Server Error</td><td>Server encountered unexpected condition</td></tr>
    </tbody>
</table>

### 3. FastApi
- FastAPI is a high performance web framework for building APIs with Python.

- **Key features:**
    | Features | Desription |
    | --- | --- |
    | Asynchronous | Allow handling of multiple request concurrently |
    | Automatic Open API Documentation | Automatically generate interactive API documentation |
    | Security and Authentication | Support different authentication methods |
    | Pythonic Syntax | Easy to be implemented with Python workflows |