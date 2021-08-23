# A bucket to store our Connection IDs
resource "aws_s3_bucket" "connection_store" {
  bucket_prefix = "${local.app_name_full}-"
}
