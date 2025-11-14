# Adding annotations to keep PVCs even if the ArgoCD application is deleted
c.KubeSpawner.storage_extra_annotations = {
    "argocd.argoproj.io/compare-options": "IgnoreExtraneous",
    "argocd.argoproj.io/sync-options": "Prune=false,Delete=false",
    "helm.sh/resource-policy": "keep",
}
