-- This SQL script creates a schema for managing assets
CREATE DATABASE IF NOT EXISTS atlan_lily_metadata;
-- Create table for assets
CREATE TABLE assets (
    asset_id SERIAL PRIMARY KEY,
    tenant_id INT NOT NULL,  
    asset_name VARCHAR(255) NOT NULL,
    asset_type VARCHAR(100) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id) ON DELETE CASCADE
);

-- Separate out asset metadata into its own table (for flexibility and normalization)
CREATE TABLE asset_metadata (
    metadata_id SERIAL PRIMARY KEY,
    asset_id INT NOT NULL,
    metadata_key VARCHAR(100),
    metadata_value TEXT,
    metadata_source VARCHAR(255), -- Adding a field for source
    metadata_type VARCHAR(100),   -- Adding a field for type
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (asset_id) REFERENCES assets(asset_id) ON DELETE CASCADE
);


-- Create table for asset lineage (normalized for upstream and downstream relationships)
CREATE TABLE asset_lineage (
    lineage_id SERIAL PRIMARY KEY,
    asset_id INT NOT NULL,
    upstream_asset_id INT,
    downstream_asset_id INT,
    FOREIGN KEY (asset_id) REFERENCES assets(asset_id) ON DELETE CASCADE,
    FOREIGN KEY (upstream_asset_id) REFERENCES assets(asset_id) ON DELETE CASCADE,
    FOREIGN KEY (downstream_asset_id) REFERENCES assets(asset_id) ON DELETE CASCADE
);

-- Create table for asset audits (split out user information for audit records)
CREATE TABLE asset_audits (
    audit_id SERIAL PRIMARY KEY,
    asset_id INT NOT NULL,
    action_type VARCHAR(50),
    user_id INT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    details TEXT,
    FOREIGN KEY (asset_id) REFERENCES assets(asset_id) ON DELETE CASCADE
);

-- Normalize asset access control (separate access control rules)
CREATE TABLE user_roles (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(100)
);

CREATE TABLE asset_access_control (
    asset_id INT NOT NULL,
    tenant_id INT NOT NULL,
    user_id INT NOT NULL,
    role_id INT,
    read_permission BOOLEAN DEFAULT FALSE,
    write_permission BOOLEAN DEFAULT FALSE,
    delete_permission BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (asset_id, user_id),
    FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES user_roles(role_id) ON DELETE CASCADE,
    FOREIGN KEY (asset_id) REFERENCES assets(asset_id) ON DELETE CASCADE
);

-- Asset tags normalized (tags table moved out for many-to-many relationships)
CREATE TABLE tags (
    tag_id SERIAL PRIMARY KEY,
    tag_name VARCHAR(100)
);

CREATE TABLE asset_tags (
    asset_id INT NOT NULL,
    tag_id INT NOT NULL,
    tenant_id INT NOT NULL,
    PRIMARY KEY (asset_id, tag_id),
    FOREIGN KEY (asset_id) REFERENCES assets(asset_id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id) ON DELETE CASCADE,
    FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id) ON DELETE CASCADE
);

-- Separate asset changes into its own table (for tracking history)
CREATE TABLE asset_changes (
    change_id SERIAL PRIMARY KEY,
    asset_id INT NOT NULL,
    change_type VARCHAR(100),
    change_description TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (asset_id) REFERENCES assets(asset_id) ON DELETE CASCADE
);

-- Asset versions normalized (keep track of different asset versions in a separate table)
CREATE TABLE asset_versions (
    version_id SERIAL PRIMARY KEY,
    asset_id INT NOT NULL,
    version_number VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (asset_id) REFERENCES assets(asset_id) ON DELETE CASCADE
);

-- Separate asset search indexes into its own table
CREATE TABLE asset_search_indexes (
    index_id SERIAL PRIMARY KEY,
    asset_id INT NOT NULL,
    index_name VARCHAR(100),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (asset_id) REFERENCES assets(asset_id) ON DELETE CASCADE
);

-- Asset comments normalized (comments separated from core asset table)
CREATE TABLE asset_comments (
    comment_id SERIAL PRIMARY KEY,
    asset_id INT NOT NULL,
    user_id INT NOT NULL,
    comment_text TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (asset_id) REFERENCES assets(asset_id) ON DELETE CASCADE
);

-- Asset labels normalized (separate from core asset table for better scalability)
CREATE TABLE asset_labels (
    asset_id INT NOT NULL,
    label_name VARCHAR(100),
    tenant_id INT NOT NULL,
    PRIMARY KEY (asset_id, label_name),
    FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id) ON DELETE CASCADE,
    FOREIGN KEY (asset_id) REFERENCES assets(asset_id) ON DELETE CASCADE
);

-- Create table for asset metadata connections (normalize metadata systems)
CREATE TABLE metadata_systems (
    system_id SERIAL PRIMARY KEY,
    system_name VARCHAR(100),
    metadata_type VARCHAR(100)
);

CREATE TABLE asset_metadata_connections (
    asset_id INT NOT NULL,
    system_id INT NOT NULL,
    PRIMARY KEY (asset_id, system_id),
    FOREIGN KEY (asset_id) REFERENCES assets(asset_id) ON DELETE CASCADE,
    FOREIGN KEY (system_id) REFERENCES metadata_systems(system_id) ON DELETE CASCADE
);

