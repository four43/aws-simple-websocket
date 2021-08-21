data "aws_iam_policy_document" "lambda_fn_assume_role" {
  statement {
    actions = [
      "sts:AssumeRole",
    ]
    effect = "Allow"

    principals {
      type = "Service"
      identifiers = [
        "lambda.amazonaws.com"
      ]
    }
  }
}

resource "aws_iam_role" "lambda_main" {
  name = local.app_name_full
  assume_role_policy = data.aws_iam_policy_document.lambda_fn_assume_role.json
}

resource "aws_iam_role_policy_attachment" "lambda_main" {
  role = aws_iam_role.lambda_main.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "main" {
  function_name = local.app_name_full
  handler = "aws_simple_websocket.handler.handler"
  role = aws_iam_role.lambda_main.arn
  runtime = "python3.8"

  filename = "./empty.zip"

  lifecycle {
    ignore_changes = [filename]
  }
}


