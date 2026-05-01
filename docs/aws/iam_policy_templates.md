# IAM Policy Templates

These are templates only. They are not applied by this repository.

## GitHub Actions OIDC Trust Policy

Replace:

- `AWS_ACCOUNT_ID`
- `Ayush210895`
- `Credit-Risk-MLOps-AWS`

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::AWS_ACCOUNT_ID:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:Ayush210895/Credit-Risk-MLOps-AWS:ref:refs/heads/main"
        }
      }
    }
  ]
}
```

## Minimal ECR Push Policy

Replace:

- `AWS_ACCOUNT_ID`
- `AWS_REGION`
- `credit-risk-mlops-aws`

This policy allows pushing only to one existing ECR repository. It does not allow creating infrastructure.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "GetEcrAuthorizationToken",
      "Effect": "Allow",
      "Action": "ecr:GetAuthorizationToken",
      "Resource": "*"
    },
    {
      "Sid": "PushOnlyOneRepository",
      "Effect": "Allow",
      "Action": [
        "ecr:BatchCheckLayerAvailability",
        "ecr:CompleteLayerUpload",
        "ecr:DescribeRepositories",
        "ecr:InitiateLayerUpload",
        "ecr:PutImage",
        "ecr:UploadLayerPart"
      ],
      "Resource": "arn:aws:ecr:AWS_REGION:AWS_ACCOUNT_ID:repository/credit-risk-mlops-aws"
    }
  ]
}
```

## GitHub Secret Needed Later

Only add this secret after the AWS role exists:

```text
AWS_GITHUB_ACTIONS_ROLE_ARN=arn:aws:iam::AWS_ACCOUNT_ID:role/github-actions-credit-risk-mlops
```
