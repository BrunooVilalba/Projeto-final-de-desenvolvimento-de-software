variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "container_image" {
  description = "Docker image for EstudaAI"
  type        = string
  default     = "estudaai:latest"
}

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}

variable "secret_key" {
  description = "Django secret key"
  type        = string
  sensitive   = true
}

variable "openai_api_key" {
  description = "OpenAI API key"
  type        = string
  sensitive   = true
  default     = ""
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "estudaai"
}

variable "tags" {
  description = "Common tags"
  type        = map(string)
  default = {
    Project     = "estudaai"
    Environment = "production"
    ManagedBy   = "terraform"
  }
}
