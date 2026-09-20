---
title: Azure Services - Deployment Template
source_url: https://github.com/swisskyrepo/InternalAllTheThings/blob/203bb0c0b290bf7c9158c32d43523b8d66f292c1/docs/cloud/azure/azure-services-deployment-template.md
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: cloud
---

* List the deployments

    ```powershell
    PS Az> Get-AzResourceGroup
    PS Az> Get-AzResourceGroupDeployment -ResourceGroupName SAP
    ```

* Export the deployment template

    ```ps1
    PS Az> Save-AzResourceGroupDeploymentTemplate -ResourceGroupName <RESOURCE GROUP> -DeploymentName <DEPLOYMENT NAME>

    # search for hardcoded password
    cat <DEPLOYMENT NAME>.json
    cat <PATH TO .json FILE> | Select-String password
    ```

## References

* [Training - Attacking and Defending Azure Lab - Altered Security](https://www.alteredsecurity.com/azureadlab)
