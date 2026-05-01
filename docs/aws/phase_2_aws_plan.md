# AWS Deployment Plan

Phase 1 runs locally with Docker and GitHub Actions. Phase 2 adds AWS readiness in small, controlled steps. No AWS resources are created by this repository unless a guarded manual workflow is explicitly enabled.

## Target AWS Architecture

```text
GitHub Actions
  -> run tests
  -> build Docker image
  -> optionally push image to an existing Amazon ECR repository

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

1. Keep the manual workflow in no-cost dry-run mode.
2. Create AWS Budget and billing alerts before any deployment.
3. Create an ECR repository only when ready.
4. Add GitHub Actions OIDC role for ECR push only.
5. Push one image to ECR manually, then confirm billing remains quiet.
6. Deploy container to ECS Fargate or SageMaker only after adding shutdown steps.
