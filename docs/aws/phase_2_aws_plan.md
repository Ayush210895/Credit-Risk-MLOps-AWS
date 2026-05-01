# AWS Deployment Plan

Phase 1 runs locally with Docker and GitHub Actions. Phase 2 will add AWS deployment in small steps.

## Target AWS Architecture

```text
GitHub Actions
  -> run tests
  -> build Docker image
  -> push image to Amazon ECR

S3
  -> raw credit data
  -> model artifacts
  -> monitoring reports

ECS Fargate or SageMaker Endpoint
  -> FastAPI inference service
  -> /health
  -> /predict

CloudWatch
  -> API logs
  -> prediction latency metrics
  -> error alarms
```

## IAM Policy Scope

The deployment role should use least privilege:

- read/write only the project S3 bucket prefixes
- push/pull only this project ECR repository
- update only this project ECS/SageMaker resources
- write logs only to this project CloudWatch log group
- read only required secrets from AWS Secrets Manager

## Future Steps

1. Create S3 bucket for raw data and model artifacts.
2. Create ECR repository for the inference image.
3. Add GitHub Actions OIDC role for AWS deploys.
4. Deploy container to ECS Fargate or SageMaker.
5. Add CloudWatch dashboards and alarms.
6. Add scheduled drift report job.
