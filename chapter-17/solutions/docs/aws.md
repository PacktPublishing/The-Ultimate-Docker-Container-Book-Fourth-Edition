# Preparing an AWS Account for the exercise
## Account creation
* Create a free account here: https://aws.amazon.com/free/
Make sure you have AMI configured correctly and added at least one user with 
## Create permission set
Go to the IAM Identity Center console
	•	In the AWS console search bar, type “IAM Identity Center” → open it.
	•	In the left sidebar, click Permission sets under Multi-account permissions.

---

2️⃣ Click Create permission set

You’ll see two options:

* Predefined permission set (recommended)
* Custom permission set

Choose Predefined permission set — it’s faster and safe.

---

3️⃣ Select the predefined policy

You’ll see a list like:

*	AdministratorAccess
*	PowerUserAccess
*	ReadOnlyAccess

✅ Select AdministratorAccess
Then click Next.

---



 
4️⃣ Leave default settings
 
You can leave everything as default:
* Session duration: 1 hour (or 4 hours if you prefer)
* Relay state: blank
* Tags: optional

Then click Create.

You’ll now see AdministratorAccess listed in your Permission sets table.

---

## Create User

1️⃣ Confirm there’s at least one user

Go to the left menu → Users
➡️ You should see your email listed (e.g., yourname@gmail.com).
If not, click Add user, then fill in your name and email.

---

2️⃣ Assign the user to your AWS account
1. Left menu → AWS accounts
1. You should see your account (e.g., ending with 6546-...).
1. Click it → go to the Assigned users tab.
1. If empty, click Assign users or groups → pick your user → choose AdministratorAccess as the Permission set.

✅ This step is crucial — without it, SSO login will fail (“no accounts available”).

---

3️⃣ Optional: Confirm MFA (multi-factor authentication)

Still on the dashboard, you can click Configure MFA if you want to enforce MFA for your users — not mandatory, but highly recommended.

## Install AWS CLI:
```
brew update
brew install awscli
aws --version
```
Configure:
```
aws configure sso
# Answer prompts:
# SSO session name (Recommended): eks-lab
# SSO start URL [None]: https://<your-app>.awsapps.com/start
# SSO region [None]: eu-central-1
# Then choose your account (it should show your AWS account)
# Then choose a permission set (AdministratorAccess)
# CLI default client Region [None]: eu-central-1
# CLI default output format [None]: json
# CLI profile name [None]: eks-lab
```
NOTE: The SSO start URL you can find on the dashboard of the AIM Identity Center in AWS

Then test:
```
aws sso login --profile eks-lab
aws sts get-caller-identity --profile eks-lab
```
---

## Install eksctl
```
brew install eksctl
eksctl version
```
eksctl reads your AWS CLI profile & default region, so you must login to your AWS account first. Creating clusters later will use that region by default.  

---

## Quick sanity check
```
aws sts get-caller-identity --profile <your-sso-profile>
```
eksctl wired to your profile & region:
```
# should return "clusters: []" if you have none (that’s fine)
aws eks list-clusters --region eu-central-1 --profile eks-lab
eksctl version
```

That’s it 🎉