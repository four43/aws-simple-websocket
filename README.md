# aws-simple-websocket

Using AWS's API Gateway + Lambda + Python to run a simple websocket application. For learning/testing. The AWS Resources
seemed overly complex and were missing some critical gotchas in setting up a system like this.

Using the following for guidance:

* [AWS Blog: Announcing WebSocket APIs in Amazon API Gateway](https://aws.amazon.com/blogs/compute/announcing-websocket-apis-in-amazon-api-gateway/)
* [GitHub: aws-samples/simple-websockets-chat-app (Node.JS + SAM)](https://github.com/aws-samples/simple-websockets-chat-app)

## Architecture

To keep things as basic as possible we're using a bare minimum of resources and CLI helpers where possible.

A **client** makes a connection via Websocket to an **API Gateway V2**. That gateway maintains a socket connection for
us, and sends events to some sort of "integration" or handler. In our case, this will be a **Lambda** function that will
handle the incoming socket events (**$connect**/**$disconnect**). It will handle messages sent from websocket clients,
and to further expand this example, an outside data source via **SNS** topic. The API Gateway requires us to keep track
of Connection IDs, so we can programmatically and precisely send messages to specific clients.

Using Terraform (in `./deployment`) the following are created:

![Architecture Diagram](./docs/architecture.svg)

1. **API Gateway V2 (Websocket)** - The primary Websocket management service which holds sockets for connections and can
   hit a variety of AWS integrations

1. **Lambda** - The main executor of business logic - where all our code will live

1. **S3** - A basic Key/Value store for our connections

1. **SNS** - To demonstrate an external publisher, our Lambda function is also listening to an SNS Topic

Some additional resources are needed:

1. **CloudWatch** - Logging for API Gateway and Lambda function with retention periods set by default

1. **IAM** - Permissions to glue everything together

## Deployment

This demo repo uses Terraform to manage cloud resources. These are all stored in the `./deployment` repository.
**NOTE:** Creating resources in AWS may incur charges to your account. Ensure you have billing alarms setup and
understand AWS costs. This demo repo should cost almost nothing, however.

1. [Install Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli)
1. Change to `./deployment` directory
1. Init Terraform (`terraform init`)
1. It's best practice to use "Workspaces" to namespace resources in terraform for different environments, so create
   a `dev` workspace (`terraform workspace new dev`)
1. Check if you need to
   enable [API Gateway Logging](https://aws.amazon.com/premiumsupport/knowledge-center/api-gateway-cloudwatch-logs/) in
   your current region. Feel free to set `./deployment/enf.tf:init_api_gw_logging_role` to false if your account already
   has this setup
1. Create the resources `terraform apply`

## Improvements

1. Move from `print()` to `logging` module, for the sake of keeping this really simple, I left print in there
