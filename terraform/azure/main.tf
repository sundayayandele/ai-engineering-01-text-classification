provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "app" {
  name     = "${var.project}-rg"
  location = var.location
}

resource "azurerm_container_registry" "app" {
  name                = substr(replace(var.project, "-", ""), 0, 50)
  resource_group_name = azurerm_resource_group.app.name
  location            = azurerm_resource_group.app.location
  sku                 = "Basic"
  admin_enabled       = false
}

output "registry_login_server" {
  value = azurerm_container_registry.app.login_server
}
