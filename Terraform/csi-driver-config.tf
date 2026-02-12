data "aws_iam_policy_document" "secrets_csi_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]
    effect  = "Allow"

    condition {
      test     = "StringEquals"
      variable = "${replace(aws_iam_openid_connect_provider.eks.url, "https://", "")}:sub"
      values   = ["system:serviceaccount:default:backend-sa"]
    }

    principals {
      identifiers = [aws_iam_openid_connect_provider.eks.arn]
      type        = "Federated"
    }
  }
}


# Role
resource "aws_iam_role" "backend_secrets" {
  assume_role_policy = data.aws_iam_policy_document.secrets_csi_assume_role_policy.json
  name               = "${var.prefix}-secrets-csi-role"
}


# Policy
resource "aws_iam_policy" "secrets_csi" {
  name = "${var.prefix}-secrets-csi-policy"

  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [{
      Effect = "Allow"
      Action = [
        "secretsmanager:GetSecretValue",
        "secretsmanager:DescribeSecret"
      ]
      Resource = "${module.secret_store.secretmanager_arn}"
    }]
  })
}


# Policy Attachment
resource "aws_iam_role_policy_attachment" "secrets_csi" {
  policy_arn = aws_iam_policy.secrets_csi.arn
  role       = aws_iam_role.backend_secrets.name
}


output "backend_secrets_role_arn" {
  value = aws_iam_role.backend_secrets.arn
}
