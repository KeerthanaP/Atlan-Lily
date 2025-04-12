-- Create database for Atlan Lily metadata management
CREATE DATABASE IF NOT EXISTS atlan_lily_metadata;

-- Create table for tenants
CREATE TABLE tenants (
    tenant_id SERIAL PRIMARY KEY,          -- Unique identifier for each tenant
    tenant_name VARCHAR(255) NOT NULL,     -- Name of the tenant (customer or user group)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp when the tenant was created
);

-- Create table for assets (metadata assets like databases, tables, views)
CREATE TABLE assets (
    asset_id SERIAL PRIMARY KEY,           -- Unique identifier for each asset (table, column, etc.)
    tenant_id INT NOT NULL,                -- Tenant ID for multi-tenancy support
    asset_name VARCHAR(255) NOT NULL,      -- Name of the asset (e.g., table name)
    asset_type VARCHAR(100) NOT NULL,      -- Type of asset (Table, View, Column, etc.)
    description TEXT,                      -- Description of the asset
    status VARCHAR(50) DEFAULT 'active',   -- Status of the asset (active, archived, etc.)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Creation timestamp for asset
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp when the asset was last updated
    FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id) ON DELETE CASCADE -- Foreign key to tenant table
);

-- Table for metadata sources (where the metadata comes from, e.g., Monte Carlo)
CREATE TABLE metadata_sources (
    source_id SERIAL PRIMARY KEY,          -- Unique identifier for the metadata source
    source_name VARCHAR(255) NOT NULL,     -- Name of the metadata source (e.g., 'Monte Carlo')
    description TEXT,                      -- Description of the metadata source
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp when the source was created
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp of the last update
);

-- Table for metadata types (e.g., 'data quality', 'lineage')
CREATE TABLE metadata_types (
    type_id SERIAL PRIMARY KEY,            -- Unique identifier for metadata type
    type_name VARCHAR(255) NOT NULL,       -- Type of metadata (e.g., 'data quality', 'freshness')
    description TEXT,                      -- Description of the metadata type
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Creation timestamp for the metadata type
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Last update timestamp for the metadata type
);

-- Create table for metadata records (core table for holding metadata info)
CREATE TABLE metadata (
    metadata_id SERIAL PRIMARY KEY,        -- Unique identifier for each metadata record
    asset_id INT NOT NULL REFERENCES assets(asset_id) ON DELETE CASCADE, -- Link to asset
    metadata_source_id INT REFERENCES metadata_sources(source_id) ON DELETE SET NULL, -- Link to metadata source
    metadata_type_id INT REFERENCES metadata_types(type_id) ON DELETE SET NULL, -- Link to metadata type
    status VARCHAR(50) DEFAULT 'active',   -- Status of metadata (active, archived, etc.)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp when metadata was created
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp of last metadata update
    retention_policy JSONB,                -- JSON field to hold retention policy details
    downstream_status VARCHAR(50) DEFAULT 'pending', -- Status for downstream systems (e.g., pending, completed)
    issue BOOLEAN DEFAULT FALSE,           -- Flag to indicate if there is an issue with this metadata
    FOREIGN KEY (asset_id) REFERENCES assets(asset_id) ON DELETE CASCADE -- Link to asset
);

-- Table for metadata lineage (to track upstream and downstream relationships)
CREATE TABLE metadata_lineage (
    lineage_id SERIAL PRIMARY KEY,         -- Unique identifier for lineage record
    metadata_id INT NOT NULL REFERENCES metadata(metadata_id) ON DELETE CASCADE, -- Link to metadata record
    upstream_metadata_id INT REFERENCES metadata(metadata_id) ON DELETE CASCADE, -- Link to upstream metadata
    downstream_metadata_id INT REFERENCES metadata(metadata_id) ON DELETE CASCADE, -- Link to downstream metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp of lineage creation
);

-- Table for metadata quality rules (to manage data quality checks)
CREATE TABLE metadata_quality_rules (
    rule_id SERIAL PRIMARY KEY,            -- Unique identifier for each quality rule
    metadata_id INT REFERENCES metadata(metadata_id) ON DELETE CASCADE, -- Link to metadata
    rule_type VARCHAR(100),                -- Type of quality rule (e.g., "score", "threshold")
    threshold INT,                         -- Threshold value for quality checks
    last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Last checked timestamp for quality rule
);

-- Table for metadata access control (for controlling who can access metadata)
CREATE TABLE metadata_access_control (
    metadata_id INT REFERENCES metadata(metadata_id) ON DELETE CASCADE, -- Link to metadata
    user_id VARCHAR(100),               -- User identifier for access control
    read_permission BOOLEAN DEFAULT FALSE, -- Read permission for user
    write_permission BOOLEAN DEFAULT FALSE, -- Write permission for user
    delete_permission BOOLEAN DEFAULT FALSE, -- Delete permission for user
    PRIMARY KEY (metadata_id, user_id)   -- Primary key for user and metadata pair
);

-- Table for metadata tags (tags for categorizing metadata)
CREATE TABLE metadata_tags (
    metadata_id INT REFERENCES metadata(metadata_id) ON DELETE CASCADE, -- Link to metadata
    tag_name VARCHAR(100),               -- Tag name for categorization
    PRIMARY KEY (metadata_id, tag_name)  -- Primary key for metadata and tag pair
);

-- Table for metadata changes (to track any modifications in metadata)
CREATE TABLE metadata_changes (
    change_id SERIAL PRIMARY KEY,         -- Unique identifier for each change record
    metadata_id INT REFERENCES metadata(metadata_id) ON DELETE CASCADE, -- Link to metadata
    change_type VARCHAR(100),             -- Type of change (e.g., update, delete)
    change_description TEXT,              -- Description of the change
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp of the change
);

-- Table for metadata notifications (for alerting downstream systems)
CREATE TABLE metadata_notifications (
    notification_id SERIAL PRIMARY KEY,   -- Unique identifier for the notification
    metadata_id INT REFERENCES metadata(metadata_id) ON DELETE CASCADE, -- Link to metadata
    event_type VARCHAR(100),              -- Type of event that triggers the notification (e.g., "metadata_update")
    notification_channel VARCHAR(50),     -- Channel for the notification (e.g., "email", "slack")
    notification_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Time when the notification was triggered
);

-- Table for metadata retention policies (to manage retention of metadata)
CREATE TABLE metadata_retention_policies (
    policy_id SERIAL PRIMARY KEY,         -- Unique identifier for retention policy
    metadata_id INT REFERENCES metadata(metadata_id) ON DELETE CASCADE, -- Link to metadata
    retention_period INT,                 -- Retention period in days
    retention_type VARCHAR(50),           -- Retention strategy (e.g., "delete", "archive", etc.)
    action_after_expiry VARCHAR(100)      -- Action to take after retention expiry (e.g., "archive", "delete")
);

-- Table for metadata versions (to track different versions of metadata)
CREATE TABLE metadata_versions (
    version_id SERIAL PRIMARY KEY,        -- Unique identifier for each version
    metadata_id INT REFERENCES metadata(metadata_id) ON DELETE CASCADE, -- Link to metadata
    version_number VARCHAR(50),           -- Version number (e.g., "v1.0")
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp of version creation
);

-- Table for metadata search indexes (to speed up metadata searches)
CREATE TABLE metadata_search_indexes (
    index_id SERIAL PRIMARY KEY,          -- Unique identifier for the search index
    metadata_id INT REFERENCES metadata(metadata_id) ON DELETE CASCADE, -- Link to metadata
    index_name VARCHAR(100),              -- Name of the search index (e.g., "metadata_name")
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp when the index was last updated
);

-- Table for metadata comments (to allow users to comment on metadata)
CREATE TABLE metadata_comments (
    comment_id SERIAL PRIMARY KEY,        -- Unique identifier for each comment
    metadata_id INT REFERENCES metadata(metadata_id) ON DELETE CASCADE, -- Link to metadata
    user_id VARCHAR(100),                 -- User who made the comment
    comment_text TEXT,                    -- Content of the comment
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp when the comment was made
);

-- Table for metadata labels (to categorize metadata by labels)
CREATE TABLE metadata_labels (
    metadata_id INT REFERENCES metadata(metadata_id) ON DELETE CASCADE, -- Link to metadata
    label_name VARCHAR(100),            -- Label for categorization (e.g., "PII", "Sensitive")
    PRIMARY KEY (metadata_id, label_name) -- Primary key for metadata and label pair
);
