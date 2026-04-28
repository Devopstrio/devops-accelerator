provider "azurerm" {
  features {}
}

provider "aws" {
  region = var.aws_region
}

resource "azurerm_resource_group" "accelerator" {
  name     = "rg-${var.project_name}-accelerator-${var.environment}"
  location = var.location
}

# --- DevOps Transformation Hub (AKS) ---

resource "azurerm_kubernetes_cluster" "accelerator_k8s" {
  name                = "aks-devops-iq-${var.environment}"
  location            = azurerm_resource_group.accelerator.location
  resource_group_name = azurerm_resource_group.accelerator.name
  dns_prefix          = "devops-k8s"

  default_node_pool {
    name       = "default"
    node_count = 3
    vm_size    = "Standard_D2s_v3"
  }

  identity {
    type = "SystemAssigned"
  }
}

# --- Delivery Metadata Store (Postgres) ---

resource "azurerm_postgresql_flexible_server" "metadata" {
  name                   = "psql-devops-metadata-${var.environment}"
  resource_group_name    = azurerm_resource_group.accelerator.name
  location               = azurerm_resource_group.accelerator.location
  version                = "13"
  administrator_login    = "devopsadmin"
  administrator_password = var.db_password
  storage_mb             = 32768
  sku_name               = "GP_Standard_D2ds_v4"
}

# --- Multi-Cloud Landing Zone Foundation (AWS VPC) ---

resource "aws_vpc" "landing_zone" {
  cidr_block = "10.0.0.0/16"
  
  tags = {
    Name = "vpc-devops-foundation-${var.environment}"
    ManagedBy = "DevOps-Accelerator"
  }
}

# --- Global Artifact Repository (Azure Container Registry) ---

resource "azurerm_container_registry" "acr" {
  name                = "acrdevopsiq${var.environment}"
  resource_group_name = azurerm_resource_group.accelerator.name
  location            = azurerm_resource_group.accelerator.location
  sku                 = "Premium"
  admin_enabled       = true
}
