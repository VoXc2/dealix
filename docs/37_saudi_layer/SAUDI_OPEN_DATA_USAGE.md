# Saudi Open Data Usage — استخدام البيانات المفتوحة السعودية

## Available Sources

### 1. Ministry of Commerce (وزارة التجارة)
- **API**: `https://api.mc.gov.sa/v1`
- **Data Available**: Commercial Registration lookup, company name search
- **Auth**: API key required (free for basic access)
- **Rate Limit**: 100 req/min (basic)
- **Python Module**: `integrations/mc.py`

### 2. GASTAT — General Authority for Statistics (الهيئة العامة للإحصاء)
- **Portal**: `https://www.stats.gov.sa/en/850`
- **Data Available**:
  - Population statistics by region, age, gender, nationality
  - Economic indicators (GDP, inflation, employment)
  - Establishment statistics by sector and size
  - Wholesale/retail trade indices
- **Format**: CSV, XLSX, PDF
- **Update Frequency**: Quarterly / Annually
- **Open Data Portal**: `https://open.data.gov.sa`

### 3. SDAIA — Saudi Data and AI Authority (سدايا)
- **Open Data Portal**: `https://open.data.gov.sa`
- **National Data Bank**: Centralized government data repository
- **Data Available**:
  - Government service quality indicators
  - Digital transformation metrics
  - AI adoption statistics
- **AI Models**: Access to Saudi AI models via SDAIA platform
- **Auth**: Open access for most datasets, registration for some

### 4. Ministry of Human Resources (وزارة الموارد البشرية)
- **Platform**: Qiwa (قوى) — `https://qiwa.sa`
- **Data Available**:
  - Nitaqat levels by sector/region (aggregate)
  - Saudization rates by activity
  - Wage protection statistics
- **Python Module**: `integrations/qiwa.py`
- **Auth**: API key required

### 5. ZATCA — Zakat, Tax and Customs Authority
- **Portal**: `https://zatca.gov.sa`
- **Data Available**:
  - VAT registration lookup
  - Customs tariff schedules
  - Zakat calculation guidance
- **Python Module**: `integrations/zatca.py` (Fatoorah API)
- **Auth**: Certificate-based for Fatoorah API

### 6. Ministry of Investment (MISA — وزارة الاستثمار)
- **Portal**: `https://misa.gov.sa`
- **Data Available**:
  - Investment license validation
  - Investment opportunities catalog
  - Sector-specific incentives
- **Python Module**: `integrations/misa.py`

### 7. Saudi Central Bank (SAMA — البنك المركزي)
- **Portal**: `https://sama.gov.sa`
- **Data Available**:
  - Interest rates, money supply
  - Banking sector indicators
  - Payment statistics (MADA, SADAD)
  - Fintech licensing

### 8. Capital Market Authority (CMA — هيئة السوق المالية)
- **Portal**: `https://cma.org.sa`
- **Data Available**:
  - Listed company data (Tadawul)
  - Capital market statistics
  - Corporate disclosures
  - Investor protection data

### 9. Saudi Post (البريد السعودي)
- **API**: `https://api.address.gov.sa/v1`
- **Data Available**:
  - National address validation
  - Building number lookup
  - Address geocoding
- **Python Module**: `integrations/saudi_post.py`

### 10. Ministry of Tourism (وزارة السياحة)
- **Portal**: `https://mt.gov.sa`
- **Data Available**:
  - Tourism licenses
  - Visitor statistics
  - Licensed tour operators

## Data Processing Workflows

### CR Validation Pipeline
```
input CR number → MCClient.validate_cr() → CRValidation
                  ↓ (if valid)
              QiwaClient.check_nitaqat() → NitaqatStatus
              QiwaClient.check_saudization() → SaudizationRate
                  ↓ (if applicable)
              GOSIClient.verify_employer() → EmployerStatus
                  ↓ (if applicable)
              MudadClient.verify_wps() → WPSStatus
```

### Address Normalization
```
input address → SaudiPostClient.validate_address() → AddressValidation
                ↓
            City/Region Normalizer → normalized city/region
                ↓
            SAUDI_REGIONS lookup → region info
```

## Rate Limiting & Caching

- **MC API**: 100 req/min — cache CR validations for 24h
- **Qiwa**: 60 req/min — cache Nitaqat for 6h
- **Saudi Post**: 200 req/min — cache address lookups for 30 days
- **GOSI**: 60 req/min — cache for 24h
- **Mudad**: 60 req/min — cache for 6h

## Data Quality Notes

1. CR data from MC may be up to 24h delayed from actual registry
2. Nitaqat data is live through Qiwa
3. Saudi Post address data is 95%+ accurate for major cities
4. GOSI employer data reflects contributions, not employment (may differ from Qiwa)
5. GASTAT economic data is typically published 2-3 months after period end

## Code Reference

- **All API clients**: `integrations/` package
- **Sector mapping**: `auto_client_acquisition/saudi_layer/saudi_sector_taxonomy.py`
- **City/region mapping**: `auto_client_acquisition/saudi_layer/city_region_normalizer.py`
- **ZATCA e-invoicing**: `integrations/zatca.py`
