c.KubeSpawner.pod_security_context.update({
    'runAsNonRoot': True,
    'seccompProfile': {
        'type': '{{- .Values.configuration.jupyterhub.singleuser.securityContext.seccompProfile.type | default "RuntimeDefault" }}', 
        {{- if .Values.configuration.jupyterhub.singleuser.securityContext.seccompProfile.type == "Localhost" }} 'localhostProfile': '{{- .Values.configuration.jupyterhub.singleuser.securityContext.seccompProfile.localhostProfile | default "" }}', {{- end }}
    },
})

c.KubeSpawner.container_security_context.update({
    'allowPrivilegeEscalation': False,
    'capabilities': {
        'drop': ['ALL'],
    },
})