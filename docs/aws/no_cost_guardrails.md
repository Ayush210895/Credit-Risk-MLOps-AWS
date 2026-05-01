# No-Cost AWS Guardrails

This repository is AWS-ready, but it does not create AWS resources by default.

## Current No-Cost Mode

The default workflow is local-only:

- no AWS authentication
- no AWS resource creation
- no ECR image push
- no ECS, SageMaker, RDS, S3, or CloudWatch resources

The manual workflow `.github/workflows/aws-ecr-manual.yml` always runs a local dry run first. The ECR publish job is skipped unless both are true:

1. `enable_aws_push` is set to `true`
2. `cost_confirmation` is exactly `I_UNDERSTAND_AWS_COSTS`

## Before Enabling Any AWS Step

Do these first in the AWS console:

1. Create an AWS Budget with a very small monthly threshold.
2. Add billing email alerts.
3. Confirm there is no NAT Gateway in the design.
4. Confirm there is no always-on RDS database.
5. Confirm there is no SageMaker endpoint left running.
6. Confirm CloudWatch log retention is short.
7. Confirm the ECR repository already exists.

## Services To Avoid Until Needed

These are common sources of accidental charges:

| Service | Why to avoid early |
| --- | --- |
| NAT Gateway | Can cost money while idle |
| RDS | Usually bills while provisioned |
| SageMaker Endpoint | Bills while endpoint is running |
| ECS Fargate Service | Bills while tasks are running |
| CloudWatch Logs | Can grow quietly if retention is unlimited |

## Safe Learning Path

1. Keep running local CI, Docker, MLflow, and registry approval.
2. Use the manual workflow in no-cost dry-run mode.
3. Add AWS Budget and billing alerts.
4. Create only an ECR repo when ready.
5. Push one image manually, then delete old images.
6. Deploy runtime services only when you are ready to monitor and shut them down.
