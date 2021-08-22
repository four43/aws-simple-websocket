data "aws_iam_policy_document" "lambda_fn_assume_role" {
  statement {
    actions = [
      "sts:AssumeRole",
    ]
    effect  = "Allow"

    principals {
      type        = "Service"
      identifiers = [
        "lambda.amazonaws.com"
      ]
    }
  }
}

resource "aws_iam_role" "lambda_main" {
  name               = local.app_name_full
  assume_role_policy = data.aws_iam_policy_document.lambda_fn_assume_role.json
}

resource "aws_iam_role_policy_attachment" "lambda_main" {
  role       = aws_iam_role.lambda_main.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

data "aws_iam_policy_document" "lambda_rw_connection_store" {
  statement {
    effect    = "Allow"
    actions   = [
      "s3:GetObject",
      "s3:PutObject",
      "s3:DeleteObject"
    ]
    resources = [
      "arn:aws:s3:::${local.config.connection_store_bucket_name}/${local.config.connection_store_prefix}/*",
    ]
  }
  statement {
    effect    = "Allow"
    actions   = [
      "s3:ListBucket",
    ]
    resources = [
      "arn:aws:s3:::${local.config.connection_store_bucket_name}",
    ]
  }

  statement {
    effect    = "Allow"
    actions   = [
      "execute-api:ManageConnections"
    ]
    resources = [
      "${aws_apigatewayv2_api.main.execution_arn}/*"
    ]
  }
}

resource "aws_iam_policy" "lambda_rw_connection_store" {
  name   = local.app_name_full
  policy = data.aws_iam_policy_document.lambda_rw_connection_store.json
}

resource "aws_iam_role_policy_attachment" "lambda_rw_connection_store" {
  policy_arn = aws_iam_policy.lambda_rw_connection_store.arn
  role       = aws_iam_role.lambda_main.name
}

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
      CONNECTION_STORE_PREFIX      = local.config.connection_store_prefix
      EXECUTE_API_ENDPOINT         = replace(aws_apigatewayv2_stage.lambda.invoke_url, "wss://", "https://")
    }
  }

  lifecycle {
    ignore_changes = [filename]
  }
}


