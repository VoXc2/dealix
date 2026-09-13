export const serviceCatalogSnapshot = {
  "generated_from": "scripts/dealix_export_service_catalog_json.py",
  "public_only": true,
  "schema_version": "2.0-public",
  "public_commercial_truth": "one_governed_path",
  "generated_for": "public_static_surface",
  "offerings": [
    {
      "id": "free_mini_diagnostic",
      "name_en": "Free Mini Diagnostic",
      "name_ar": "التشخيص المجاني المختصر",
      "pricing": "free",
      "commercial_status": "public_entry",
      "next_step": "qualified_discovery"
    },
    {
      "id": "revenue_command_pilot_30d",
      "name_en": "30-Day Revenue Command Pilot",
      "name_ar": "تجربة مركز قيادة الإيرادات — 30 يومًا",
      "pricing": "customer_specific_quote_after_qualified_discovery",
      "commercial_status": "quote_only",
      "public_checkout": false,
      "customer_result_guarantee": false,
      "next_step": "governed_delivery_and_proof"
    }
  ],
  "claim_policy": {
    "synthetic_or_demo_is_customer_proof": false,
    "revenue_requires_payment_evidence": true,
    "testimonial_requires_publication_approval": true,
    "unsupported_certification_or_residency_claims": false
  }
} as const;
