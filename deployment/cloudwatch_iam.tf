# For API Gateway Logging: https://aws.amazon.com/premiumsupport/knowledge-center/api-gateway-cloudwatch-logs/
# This is only required once per region
data "aws_iam_policy_document" "cloudwatch_logging" {
  statement {
    actions = [
      "sts:AssumeRole",
    ]
    effect = "Allow"

    principals {
      type = "Service"
      identifiers = [
        "apigateway.amazonaws.com"
      ]
    }
  }
}

resource "aws_iam_role" "cloudwatch_log_role" {
  count              = local.init_api_gw_logging_role ? 1 : 0
  name               = "${local.app_name}-logging-${local.env}"
  assume_role_policy = data.aws_iam_policy_document.cloudwatch_logging.json
}

resource "aws_iam_role_policy_attachment" "cloudwatch_log_role" {
  count = local.init_api_gw_logging_role ? 1 : 0

  role       = aws_iam_role.cloudwatch_log_role[0].name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonAPIGatewayPushToCloudWatchLogs"
}

resource "aws_api_gateway_account" "main_config" {
  count               = local.init_api_gw_logging_role ? 1 : 0
  cloudwatch_role_arn = aws_iam_role.cloudwatch_log_role[0].arn
}
