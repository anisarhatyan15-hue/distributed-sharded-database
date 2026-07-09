Distributed Sharded Database System with Automated Failover
This project is a Horizontally Scalable and Fault-Tolerant distributed database system simulation built from scratch using Python and SQLite. The core objective of this project is to demonstrate critical Site Reliability Engineering (SRE) principles and advanced Backend Architecture concepts—specifically, cryptographic data sharding and automated disaster recovery (Failover).

 System Architecture
The infrastructure consists of three physically isolated SQLite databases managed dynamically by a centralized Query Router:

database_shard_1.db — Primary Database Node 1 (Master Shard 1).

database_shard_2.db — Primary Database Node 2 (Master Shard 2).

database_replica.db — Shared Backup Database (Asynchronous/Synchronous Replica).

 Core Engineering Features
1. Consistent Sharding Logic
To ensure an even data distribution across the cluster and prevent data hotspots, the system utilizes a deterministic algorithmic approach:

The incoming user_id is processed through a cryptographic MD5 hashing function.

The resulting hexadecimal hash is converted into a base-10 integer.

A modulo operation (% 2) is applied to dynamically route the request to the correct target shard.

2. High Availability Data Replication
To achieve Data Loss Prevention (DLP), a replication layer is embedded within the architecture. Every successful INSERT or mutation query executed on a Master Shard is instantly duplicated into the global database_replica.db node, preserving state across the cluster.

3. Automated Failover (Self-Healing Router)
The Query Router implements active runtime Health Checking during read operations (SELECT). If a primary Master Shard goes offline or becomes unreachable:

The active try...except block intercepts the database connection exception.

The system automatically triggers a Failover Mechanism, seamlessly rerouting the read traffic to the Replica database.

This ensures zero downtime and high system availability from the user's perspective.

Technical Stack Breakdown
Language: Python 3

Storage Engine: SQLite3 (Isolated DB files acting as distributed nodes)

Core Concepts: Systems Design, Data Integrity, Cryptographic Hashing, Fault Tolerance, SRE Automation.


