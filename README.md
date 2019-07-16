# Terraform Filter

The purpose of this program is to filter out sensitive information
from `terraform plan` and `terraform apply` output. 

The program accepts the output of terraform on `stdin` along with a
file of the key names of sensitive information in terraform state. The
program will output the terraform output with the sensitive
information replaced with `*`s. 

For example, if the output of terraform plan looked like:

``` shell
An execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
+ create
- destroy

Terraform will perform the following actions:

  # module.radar-retail-dashboard.azurerm_app_service.radar-retail-dashboard will be destroyed
- resource "azurerm_app_service" "radar-retail-dashboard" {
      - app_service_plan_id            = "/subscriptions/ad956a0c-8145-4373-8540-4d68fcce5080/resourceGroups/radar-retail-dashboard/providers/Microsoft.Web/serverfarms/radar-retail-dashboard-plan" -> null
      - app_settings                   = {
          - "DOCKER_REGISTRY_SERVER_PASSWORD"     = "<some secret here>"
          - "DOCKER_REGISTRY_SERVER_URL"          = "https://automatonregistry.azurecr.io"
          - "DOCKER_REGISTRY_SERVER_USERNAME"     = "automatonregistry"
          - "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = "false"
        } -> null
```

and a file named `sensitive_keys.txt` looked like 

``` shell
password
username
```

the output of `terraform plan | ./terraform_filter.py
sensitive_keys.txt` would be

``` shell
An execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
+ create
- destroy

Terraform will perform the following actions:

  # module.radar-retail-dashboard.azurerm_app_service.radar-retail-dashboard will be destroyed
- resource "azurerm_app_service" "radar-retail-dashboard" {
      - app_service_plan_id            = "/subscriptions/ad956a0c-8145-4373-8540-4d68fcce5080/resourceGroups/radar-retail-dashboard/providers/Microsoft.Web/serverfarms/radar-retail-dashboard-plan" -> null
      - app_settings                   = {
          - "DOCKER_REGISTRY_SERVER_PASSWORD"     = **********************************
          - "DOCKER_REGISTRY_SERVER_URL"          = "https://automatonregistry.azurecr.io"
          - "DOCKER_REGISTRY_SERVER_USERNAME"     = "automatonregistry"
          - "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = "false"
        } -> null

```

## Usage

``` shell
./terraform_filter.py --help
usage: terraform_filter.py [-h] [tf_output] sensitive_keys_input

positional arguments:
  tf_output
  sensitive_keys_input

optional arguments:
  -h, --help            show this help message and exit
```

Note - you may either pass in `tf_output` via `stdin` or a file.

