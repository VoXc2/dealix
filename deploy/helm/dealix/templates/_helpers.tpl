{{/* Common labels + selector helpers. */}}
{{- define "dealix.labels" -}}
app.kubernetes.io/name: dealix
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end -}}

{{- define "dealix.api.selectorLabels" -}}
app.kubernetes.io/name: dealix
app.kubernetes.io/component: api
{{- end -}}

{{- define "dealix.web.selectorLabels" -}}
app.kubernetes.io/name: dealix
app.kubernetes.io/component: web
{{- end -}}
