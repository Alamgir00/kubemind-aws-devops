terraform {
  backend "s3" {
    bucket       = "kubemind-terraform-state-650694421089-ap-south-1"
    key          = "env/dev/terraform.tfstate"
    region       = "ap-south-1"
    encrypt      = true
    use_lockfile = true
  }
}
