# Atlan-Lily: Real-Time Metadata Platform using Atlan
## Table of Contents
- [Summary](#context--summary)
- [Design Goals & Principles](#design-goals--principles)
- [System Architecture Overview](#system-architecture-overview)
- [Data Flow (Inbound & Outbound)](#data-flow-inbound--outbound)
- [Metadata Store Strategy](#metadata-store-strategy)
- [Security & Multi-Tenancy](#security--multi-tenancy)
- [Prototype Use Cases](#prototype-use-cases)
- [Cost, Scalability & Observability](#cost-scalability--observability)
- [Technology Choices (Side Notes)](#technology-choices-side-notes)

---

# Summary

Atlan Lily delivers a comprehensive three-tier architecture that enables real-time metadata flow between internal and external systems, providing a dynamic metadata plane within the data stack, powering data observability, governance, and automation requirements.

This system will be built for scale, and modularity, with authentication, authorization, extensibility, and operational observability. By leveraging an event-driven approach and supporting pre-ingest/post-consume transformation hooks, Atlan Lily ensures seamless metadata flow across diverse data ecosystems, including SaaS tools like Monte Carlo.

---

## Design Goals & Principles

### Goals

- Near-real-time metadata capture, enrichment and propagation.
- Scalable and cost effective metadata storage with a capability to process large datasets
- Secure multi-tenant setup with data isolation and compliance
- Entensible architecure with pre/post processing hooks.

### Principles
- **Simplicity:** Use cloud-native components that integrate well with the Atlan platform.
- **Modularity:** Enable easy plug-and-play expansion for new sources and tools.
- **Scalability:** Ensure the system can scale horizontally to handle massive metadata volumes.
- **Observability:** Incorporate robust logging, monitoring, and alerting capabilities for real-time monitoring.

---

## Scope

The architecture is designed around the **Atlan platform** as the core metadata hub, with integration layers for near-real-time data ingestion, event-based metadata updates, and downstream propagation.

| **Category**                          | **Description**                                                                                                                                 |
|-----------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| **Metadata Sources**                    | Ingest metadata from internal (Atlan platform) and external sources (e.g., Monte Carlo, SaaS tools like Slack, MS Teams). The data type can include tables, columns, dashaboard etc.|
| **Real-Time Requirements**              | Sschema, lineage, are event-driven and needs to be captured near-real-time.  |
| **Metadata Storage**                    | Scalable, distributed metadata store with eventual consistency for non-critical data.       |
| **Data Transformations**                | Apply pre-ingest and post-consume transformations for enrichment, validation, and compliance (including GDPR). |
**Authentication & Authorization**      | RBAC/ABAC for metadata access and OAuth2.0 for authentication.|
| **Multi-Tenancy**                        | Support multi-tenant with logical isolation ensuring data privacy, compliance, and security with robust access control, partitioning and encryption. |
| **SaaS Integrations**                   | API-driven integrations with third-party tools. Webhooks or polling mechanisms, supporting real-time metadata propagation
| **Scalability**                          | A horizontally scalable platform to handle large metadata volumes (up to 1B assets) |
| **Observability**                       | Built-in monitoring and logging for metadata flow and system health. Custom metrics and dashboards for KPIs(Key Performance Indicators). Can leverage Atlan's native observability tools for real-time insights |

---

## Architecture Overview


![Atlan Lily Architecture Diagram](lily-overview.drawio.png)


1. **Metadata Ingestion Layer**: Real-time ingestion of metadata using webhooks, APIs, and custom connectors.
2. **Event Stream Layer**: Stream processing to ensure metadata is captured and propagated in real-time across systems.
3. **Metadata Enrichment & Transformation**: Pre and post-processing to apply transformations, data validation, and compliance checks.
4. **Atlan Platform**: The core system that handles metadata storage, querying, and visualization.
5. **Outbound Dispatcher**: For real-time communication of metadata changes to downstream systems (e.g., dbt, Snowflake).
6. **Observability**: Metrics and logs for platform health, metadata ingestion times, and API performance.

---