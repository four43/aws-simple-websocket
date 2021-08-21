resource "aws_cloudwatch_log_group" "api_gw" {
  name              = "/aws/apigateway/${aws_apigatewayv2_api.main.name}"
  retention_in_days = 7
}

# Create log group here so we can set retention and can clean it up.
resource "aws_cloudwatch_log_group" "mangum_logs" {
  name              = "/aws/lambda/${local.app_name_full}"
  retention_in_days = 7
}
