# Store basic config, use just a dev environment for now
locals {
  app_name = "simple-websocket-testing"
  env      = terraform.workspace

  app_name_full = "${local.app_name}-${local.env}"
  unique_prefix = "four43"
}

locals {
  env_config = {
    dev = {
      # For Region Wide API Gateway logging. Solves:
      # https://aws.amazon.com/premiumsupport/knowledge-center/api-gateway-cloudwatch-logs/
      init_api_gw_logging_role     = true
      connection_store_bucket_name = "${local.unique_prefix}-${local.app_name_full}"
      connection_store_prefix      = "active-connections"
    }
  }
  config = local.env_config[local.env]
}
