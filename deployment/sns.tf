# An SNS topic we can invoke to send messages to our API Gateway connections/Websocket clients
resource "aws_sns_topic" "input" {
  name = local.app_name_full
}

resource "aws_sns_topic_subscription" "input_to_lambda" {
  topic_arn = aws_sns_topic.input.arn
  protocol  = "lambda"
  endpoint  = aws_lambda_function.main.arn
}

resource "aws_lambda_permission" "with_sns" {
  statement_id  = "AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.main.function_name
  principal     = "sns.amazonaws.com"
  source_arn    = aws_sns_topic.input.arn
}
