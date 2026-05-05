c.KubeSpawner.pod_security_context.update({{- if .Values.configuration.jupyterhub.singleuser.securityContext.seccompProfile.type == "Localhost" }} 
{
    'runAsNonRoot': True,
    'seccompProfile': {
        'type': 'localhost', 
        'localhostProfile': '{{- .Values.configuration.jupyterhub.singleuser.securityContext.seccompProfile.localhostProfile | default "" }}',
    },
})
{{- else }}
{
    'runAsNonRoot': True,
    'seccompProfile': {
        'type': 'RuntimeDefault', 
    },
})
{{- end }}

c.KubeSpawner.container_security_context.update({
    'allowPrivilegeEscalation': False,
    'capabilities': {
        'drop': ['ALL'],
    },
})