resource "aws_apigatewayv2_api" "main" {
  name                       = local.app_name_full
  description                = "Websocket on AWS Simple Testing, ${local.env} environment"
  protocol_type              = "WEBSOCKET"
  route_selection_expression = "$request.body.action"
}

# Use our Lambda function to service requests
resource "aws_apigatewayv2_integration" "lambda_main" {
  api_id             = aws_apigatewayv2_api.main.id
  integration_uri    = aws_lambda_function.main.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

# Forward special requests ($connect, $disconnect) to our Lambda function so we can manage their state
resource "aws_apigatewayv2_route" "_connect" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "$connect"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_main.id}"
}

resource "aws_apigatewayv2_route" "_disconnect" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "$disconnect"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_main.id}"
}

resource "aws_apigatewayv2_route" "sub_widget" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "sub-widget"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_main.id}"
}

# A stage is required to actually "deploy" our API Gateway
resource "aws_apigatewayv2_stage" "lambda" {
  api_id      = aws_apigatewayv2_api.main.id
  name        = "primary"
  auto_deploy = true

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gw.arn
    format = jsonencode({
      requestId               = "$context.requestId"
      sourceIp                = "$context.identity.sourceIp"
      requestTime             = "$context.requestTime"
      protocol                = "$context.protocol"
      httpMethod              = "$context.httpMethod"
      resourcePath            = "$context.resourcePath"
      routeKey                = "$context.routeKey"
      status                  = "$context.status"
      responseLength          = "$context.responseLength"
      integrationErrorMessage = "$context.integrationErrorMessage"
    })
  }
}

# Allow the API Gateway to invoke Lambda function
resource "aws_lambda_permission" "api_gw_main_lambda_main" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.main.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.main.execution_arn}/*/*"
}



