resource "aws_s3_bucket" "connection_store" {
  bucket = local.config.connection_store_bucket_name
}