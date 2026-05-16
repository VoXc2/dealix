# Governance Core

## خط التنفيذ الإلزامي
`risk score -> policy check -> approval check -> execution -> audit`

## قواعد v1
- تحديث CRM يتطلب gate
- إذا لم توجد موافقة عند المخاطر المرتفعة: block
- كل قرار يُكتب في audit log

## نقطة ربط
- `GovernanceEngine` في `auto_client_acquisition/foundation_core/enterprise_loop.py`
