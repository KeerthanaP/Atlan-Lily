# Atlan-Lily: Real-Time Metadata Platform using Atlan
## Table of Contents
- [Summary](#context--summary)
- [Design Goals & Principles](#design-goals--principles)
- [Requirements](#requirements)
- [Architecture Overview](#architecture-overview)
- [Use Cases](#use-cases)
- [Architecture Diagram](#architecture-diagram)

---


# Summary

Atlan Lily delivers a comprehensive event-driven, modular system design pattern built on real-time metadata flow between internal and external systems, providing a dynamic metadata plane within the data stack, powering data observability, governance, and automation requirements.

This system will be built for scale, and modularity, with authentication, authorization, extensibility, and operational observability. By leveraging an event-driven approach and supporting pre-ingest/post-consume transformation hooks, Atlan Lily ensures seamless metadata flow across diverse data ecosystems, including SaaS tools like Monte Carlo.

---
# Requirements & Assumptions

| **Category**                   | **Details**                                                                 |
|---------------------------------|-----------------------------------------------------------------------------|
| **Functional Requirements**     | 1. Real-time metadata ingestion and consumption of issues. <br> 2. Support for multiple ingestion methods (CDC, API Polling, Webhooks). <br> 3. Integration with diverse external/internal tools like JIRA, Slack, Okta, and Monte Carlo. <br> 4. Ensure tenant isolation for metadata and secure data segregation. <br> 5. Allow enrichment of metadata with additional attributes. <br> 6. Lineage tracking by capturing and visualizing the flow of data across systems. <br> 7. Implement granular RBAC for metadata management. <br> 8. Maintain audit trails and trigger alerts in case of data quality issues, failures, and changes. |
| **Non-Functional Requirements** | 1. Scalability to handle 1B+ metadata assets. <br> 2. Allow ease of new data source integration.<br> 3. Low latency in metadata ingestion and updates.<br> 4. System should be fault-tolerant - achieved through retries and dead-letter queues to handle failures gracefully. <br> 5. Multi-tenant isolation and compliance support. |
| **Assumptions**                 | 1. The system operates purely through APIs, with no direct user interface. <br> 2. APIs will handle all interactions with external systems, including metadata ingestion, lineage, and notifications. <br> 3. All API endpoints will support RESTful principles with JSON as the standard data format for requests and responses. <br> 4. Authentication and authorization for all API interactions will be handled via JWT and RBAC. <br> 5. External systems will interact with the platform via APIs (e.g., for metadata ingestion, error reporting, notifications). <br> 6. All external communication protocols (such as Webhooks, CDC, etc.) will be facilitated through API endpoints. <br> 7. Future UI can be built on top of the existing API layer to expose functionalities if needed. <br> 8. The system will be able to scale and handle varying API loads with distributed architecture and load balancing. <br> 9. All API interactions will be logged for auditing purposes and potential error debugging. <br> 10. API endpoints should support high availability and fault tolerance mechanisms. <br> 11. Customers/tenants are managed and billed by the Accounts system. |
| **Limitations**                 | 1. Real-time ingestion may be limited by the capabilities of external systems, such as data source latency or rate limits on external APIs. <br> 2. The system is dependent on external data sources' ability to provide consistent, accurate, and timely metadata; inconsistent metadata may result in inaccurate insights. <br> 3. Metadata storage may be constrained by storage limits, affecting the ability to retain historical data over extended periods. |
| **Scope**                       | 1. Ingest metadata from external/internal systems. <br> 2. Real-time and batch processing of metadata. <br> 3. Provide API endpoints for metadata ingestion, lineage tracking, and notifications. <br> 4. Ensure system scalability to handle large volumes of metadata and API requests. |
| **Out-of-Scope**                | 1. User interface development is out-of-scope for this phase. <br> 2. Direct integration with proprietary or unsupported external systems is not part of the current scope. <br> 3. Heavy-duty analytics, ML models, or complex processing for metadata enrichment is outside the scope at this stage. |



---
# Atlan Lily: Phases & Prioritization

| **Priority**  | **Focus**                                                                | **Description**                                                                |
|---------------|--------------------------------------------------------------------------|--------------------------------------------------------------------------------|
| **High**      | Core System Foundation                                                   | Establish real-time metadata ingestion, event-driven architecture, and core integrations with security (PII/GDPR). |
| **High**      | SaaS Integrations                                                        | Integrate with external tools like JIRA, Slack, Okta, Monte Carlo for seamless metadata flow. |
| **High**      | Performance & Scalability                                                 | Optimize for large-scale metadata estates (1B+ assets) and ensure low-latency, high-throughput performance. |
| **High**      | Extensibility & Future Use-Cases                                         | Create a modular framework for new integrations and evolving metadata use-cases. |
| **High**      | Observability & Monitoring                                               | Build monitoring tools (logs, metrics, alerts) for proactive system health checks. |
| **High**      | Compliance & Governance                                                  | Implement GDPR/PII tagging, role-based access control (RBAC), and compliance checks. |
| **Long-term** | AI & Automation                                                           | Integrate AI for smarter metadata quality checks and automate data governance workflows. |

---
# Future UI Roadmap for Atlan Lily

| **Phase**    | **UI Focus**                                                   | **Features**                                                     |
|--------------|----------------------------------------------------------------|------------------------------------------------------------------|
| **Phase 2+** | Enhanced Observability & Monitoring                            | Full dashboards for logs, metrics, and alerting visualization    |
| **Phase 2+** | Data & Metadata Exploration                                    | Interactive views for data lineage, asset health, and quality    |
| **Long-Term**| Analytics                                    | Reporting, and advanced analytics |

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
### **External APIs** (APIs exposed to customers or external systems):

| **HTTP Method** | **Endpoint**                                | **Purpose**                                                                         |
|-----------------|--------------------------------------------|-------------------------------------------------------------------------------------|
| **POST**        | /api/v1/metadata                           | Ingest metadata from external systems or internal sources (bulk/real-time).         |
| **GET**         | /api/v1/metadata/{id}                      | Retrieve metadata details by ID.                                                    |
| **PUT**         | /api/v1/metadata/{id}                      | Update metadata by ID.                                                              |
| **DELETE**      | /api/v1/metadata/{id}                      | Delete metadata by ID.                                                              |
| **POST**        | /api/v1/metadata/lineage                   | Create or update metadata lineage information.                                      |
| **GET**         | /api/v1/metadata/lineage/{id}              | Retrieve the lineage of a specific metadata asset.                                  |
| **GET**         | /api/v1/metadata/search                    | Search for metadata assets based on parameters like tags, asset type, and filters.  |
| **POST**        | /api/v1/metadata/bulk                      | Process bulk metadata ingestion requests.                                           |
| **GET**         | /api/v1/metadata/bulk/status/{job_id}      | Get the status of a bulk metadata ingestion job.                                    |
| **POST**        | /api/v1/metadata/access-control            | Set access control policies for metadata assets (RBAC, masking rules).              |
| **GET**         | /api/v1/metadata/access-control/{asset_id} | Retrieve access control information for a specific metadata asset.                  |
| **POST**        | /api/v1/metadata/data-quality              | Create or update data quality rules for metadata assets.                            |
| **GET**         | /api/v1/metadata/data-quality/{asset_id}   | Retrieve data quality details for a metadata asset.                                 |
| **POST**        | /api/v1/metadata/notifications             | Trigger notifications for metadata-related events (e.g., schema drift).            |

### **Internal APIs** (APIs used internally for system management and processing):

| **HTTP Method** | **Endpoint**                                | **Purpose**                                                                         |
|-----------------|--------------------------------------------|-------------------------------------------------------------------------------------|
| **POST**        | /api/v1/auth/login                         | User login to generate JWT for API access.                                          |
| **POST**        | /api/v1/auth/logout                        | Log out and revoke the user session.                                                |
| **GET**         | /api/v1/auth/validate                      | Validate JWT token.                                                                 |
| **GET**         | /api/v1/metadata/audit/{asset_id}          | Retrieve audit trail for a specific metadata asset.                                 |
| **POST**        | /api/v1/metadata/external/{system_name}    | Push metadata changes or updates to external systems (e.g., BI tools, other systems). |


---
## Architecture Overview

![Atlan Lily Architecture Diagram](lily-overview.drawio.png)
## Use Cases
![Atlan Lily Architecture Diagram](lily-use-case-v2.png)

---

## Architecture Diagram
![Atlan Lily Architecture Diagram](lily-arch-v2.png)

---
# Entity Relation for Metadata Store
![Entity Relationship](lily-er.png) 

# Sequence of Interaction
## Metadata Ingestion
![Metadata Ingestion](<metadata-ingestion-seq.png>) 
## Bulk Metadata Ingestion
![Bulk Metadata Ingestion](inbound-internal-seq-v2.png)
## Metadata Transformation Service
![Metadata Transformation Service](metadata-transformation-service.png) 


## **Atlan Lily Metadata Management API**

This API provides a mechanism to manage metadata assets, notifications, and support for retry and bulk operations. It allows customers to interact with metadata, such as creating, updating, and importing metadata for multiple assets. It also supports the management of notification retries and provides the ability to handle metadata lineage, retention, and notification settings.

### **Base URL**

```
https://api.atlan.com/lily/v1
```

### **Security**

This API requires **JWT** authentication for access.

```json
{
  "security": [
    {
      "BearerAuth": []
    }
  ]
}
```

---

### **Endpoints**

#### **1. POST /metadata**

**Summary:**  
Creates or updates metadata for one or more assets, with support for retry and bulk operations.

**Request Body:**

```json
{
  "metadata": {
    "asset": {
      "asset_name": "string",
      "asset_type": "string",
      "description": "string",
      "tenant_id": "integer",
      "created_at": "string",
      "updated_at": "string"
    },
    "metadata_details": {
      "metadata_key": "string",
      "metadata_value": "string",
      "metadata_source": "string",
      "metadata_type": "string",
      "status": "string",
      "retention_policy": {
        "enabled": "boolean",
        "retention_period_days": "integer",
        "action_after_expiry": "string"
      },
      "downstream_status": "string",
      "downstream_notifications": [
        {
          "system_name": "string",
          "notification_status": "string",
          "attempts": "integer",
          "last_attempted_at": "string",
          "next_attempt_at": "string",
          "notification_type": "string",
          "notification_method": "string",
          "recipient": "string",
          "notification_payload": {
            "ticket_title": "string",
            "ticket_description": "string",
            "ticket_priority": "string",
            "ticket_labels": ["string"],
            "message": "string"
          },
          "status_message": "string"
        }
      ]
    }
  }
}
```

**Responses:**

- `200`: Metadata successfully created or updated.
  
  ```json
  {
    "status": "success",
    "message": "Metadata processed successfully."
  }
  ```

- `400`: Invalid input or missing required fields.
  
- `500`: Internal server error.

---

#### **2. POST /notifications/retry**

**Summary:**  
Retrieves a failed notification and retries sending it.

**Request Body:**

```json
{
  "notification_id": "string",
  "retry_count": 1,
  "reason": "string"
}
```

**Responses:**

- `200`: Notification retry successful.

- `400`: Invalid notification ID or retry data.

- `500`: Failed to retry notification.

---

#### **3. POST /metadata/bulk**

**Summary:**  
Bulk import metadata for one or more assets, supporting retry and bulk operations.

**Request Body:**

```json
{
  "metadata": [
    {
      "asset": {
        "asset_name": "string",
        "asset_type": "string",
        "description": "string",
        "tenant_id": "integer",
        "created_at": "string",
        "updated_at": "string"
      },
      "metadata_details": {
        "metadata_key": "string",
        "metadata_value": "string",
        "metadata_source": "string",
        "metadata_type": "string",
        "status": "string",
        "retention_policy": {
          "enabled": "boolean",
          "retention_period_days": "integer",
          "action_after_expiry": "string"
        },
        "downstream_status": "string",
        "downstream_notifications": [
          {
            "system_name": "string",
            "notification_status": "string",
            "attempts": "integer",
            "last_attempted_at": "string",
            "next_attempt_at": "string",
            "notification_type": "string",
            "notification_method": "string",
            "recipient": "string",
            "notification_payload": {
              "ticket_title": "string",
              "ticket_description": "string",
              "ticket_priority": "string",
              "ticket_labels": ["string"],
              "message": "string"
            },
            "status_message": "string"
          }
        ]
      }
    }
  ]
}
```

**Responses:**

- `200`: Bulk metadata successfully created or updated.

  ```json
  {
    "status": "success",
    "message": "Bulk metadata processed successfully."
  }
  ```

- `400`: Invalid input or missing required fields.

- `500`: Internal server error.

---

### **Security Scheme**

The API uses **Bearer Authentication**. All endpoints require a valid JWT token.

```yaml
securitySchemes:
  BearerAuth:
    type: http
    scheme: bearer
    bearerFormat: JWT
```

---