resource "aws_lambda_function" "main" {
  function_name = local.app_name_full
  handler       = "aws_simple_websocket.handler.handler"
  role          = aws_iam_role.lambda_main.arn
  runtime       = "python3.8"

  timeout = 10

  filename = "./empty.zip"

  environment {
    variables = {
      CONNECTION_STORE_BUCKET_NAME = aws_s3_bucket.connection_store.bucket
      CONNECTION_STORE_PREFIX      = local.connection_store_prefix
      EXECUTE_API_ENDPOINT         = replace(aws_apigatewayv2_stage.lambda.invoke_url, "wss://", "https://")
    }
  }

  lifecycle {
    ignore_changes = [filename]
  }
}


