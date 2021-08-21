output "ws_url" {
  value = aws_apigatewayv2_stage.lambda.invoke_url
}

output "input_sns_topic_arn" {
  value = aws_sns_topic.input.arn
}
