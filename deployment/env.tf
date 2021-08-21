locals {
  app_name = "simple-websocket-testing"
  env = terraform.workspace

  app_name_full = "${local.app_name}-${local.env}"
}

locals {
  env_config = {
    dev = {
      # For Region Wide API Gateway logging. Solves:
      # https://aws.amazon.com/premiumsupport/knowledge-center/api-gateway-cloudwatch-logs/
      init_api_gw_logging_role = true
    }
  }
  config = local.env_config[local.env]
}
