# Set custom GID support for singleserver user (not supported by Z2JHK8S HelmChart)

# Defining custom UID for singleserver user
user_id = {{ .Values.configuration.jupyterhub.singleuser.ownership.uidOverride | default 1000 }}

# Defining custom GID for singleserver user 
extra_gids = []

{{- range $groups := .Values.configuration.jupyterhub.singleuser.ownership.addToGroups }}
extra_gids.append({{ $groups.gid }})
{{- end }}

c.KubeSpawner.uid = user_id
c.KubeSpawner.supplemental_gids = extra_gids