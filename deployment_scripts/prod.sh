echo "Beginning Deployment..."

# These are set for when running locally as these values will be empty
if [ -z "$ROLE" ]; then
  ROLE="arn:aws:iam::467911368405:role/SAF-ECS-Task"
fi
if [ -z "$CI_PIPELINE_ID" ]; then
  CI_PIPELINE_ID=3864898
fi
if [ -z "$CI_PROJECT_NAME" ]; then
  CI_PROJECT_NAME=django-dashboard
fi

# Set AWS creds
response=$(aws sts assume-role --role-arn ${ROLE} --role-session-name ${CI_PIPELINE_ID}@${CI_PROJECT_NAME})
export AWS_SECRET_ACCESS_KEY=$(echo $response | jq -r ".Credentials.SecretAccessKey")
export AWS_SESSION_TOKEN=$(echo $response | jq -r ".Credentials.SessionToken")
export AWS_ACCESS_KEY_ID=$(echo $response | jq -r ".Credentials.AccessKeyId")
export AWS_DEFAULT_REGION=us-east-1

echo "[default]" > credentials
echo "aws_access_key_id = $AWS_ACCESS_KEY_ID" >> credentials
echo "aws_secret_access_key = $AWS_SECRET_ACCESS_KEY" >> credentials
echo "aws_session_token = \"$AWS_SESSION_TOKEN\"" >> credentials

echo "Deploying to prod"
make deploy_to_prod
