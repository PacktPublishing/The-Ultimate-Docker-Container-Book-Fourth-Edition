# Preparing an Azure Account for the exercise
## Account creation
* Create a free account here: https://azure.microsoft.com/en-us/pricing/purchase-options/azure-account

## Install Azure CLI
```
brew update
brew install azure-cli
az version
```

## Login to the correct tenant/subscription
```
az login --tenant f7f84bff-f18b-44e5-8f26-5a08518baadf
```
Select the subscription when asked, in my case "The Ultimate Docker Container Book v4"

List your accounts:
```
az account list --output table
```
Set your subscription:
```
az account set --subscription "<YOUR_SUBSCRIPTION_NAME_OR_ID>"
```
When I tried to create the ASK cluster I got an error message with this text snippet: "...(MissingSubscriptionRegistration) The subscription is not registered to use namespace 'Microsoft.ContainerService'..."
This is how I needed to register `ContainerService` in my subscription:
```
az provider register --namespace Microsoft.ContainerService --wait
az provider show --namespace Microsoft.ContainerService --query "registrationState" -o tsv
```
The second command should show "Registered"

As the creation of the ACR failed, I also had to register the `ContainerRegistry` first:
```
az provider register --namespace Microsoft.ContainerRegistry --wait
az provider show --namespace Microsoft.ContainerRegistry --query "registrationState" -o tsv
```
The resulting acr registry name is in the author's case: `taskboardacr8716`

