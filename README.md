# HELIX

TODO 

How to install :  

```sh
helm repo add aphp-helix https://aphp.github.io/HELIX
helm repo update
helm upgrade helix aphp-helix/helix \
  --namespace <namespace> \
  --install \
  -f <values-file> \
  --wait
```