output "ws_url" {
  value = aws_apigatewayv2_stage.lambda.invoke_url
}

output "input_sns_topic_arn" {
  value = aws_sns_topic.input.arn
}

output "lambda_log_group" {
  value = aws_cloudwatch_log_group.lambda_main.name
}

output "api_gw_log_group" {
  value = aws_cloudwatch_log_group.api_gw.name
}

