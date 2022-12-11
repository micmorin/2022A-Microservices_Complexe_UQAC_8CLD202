az login -u adavy@et.esiea.fr -p Jo3M2qRze
az account set --subscription a75d99f4-a240-4c29-a2f3-57fc5ea29163
az aks get-credentials --resource-group k8s --name k8s
az aks start --resource-group k8s --name k8s