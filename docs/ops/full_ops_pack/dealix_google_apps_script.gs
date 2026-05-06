/**
 * Dealix Level 1 — Google Apps Script template
 * Copy into: Extensions → Apps Script (bound to the same Spreadsheet as the Form).
 * Do NOT put API keys, Moyasar secrets, or PATs in this file. Use Script Properties for production email overrides if needed.
 */

/************************************
 * CONFIG
 ************************************/
const OWNER_EMAIL = "your@email.com";
const WHATSAPP_LINK = "https://wa.me/9665XXXXXXXX?text=Diagnostic";
const OPERATING_BOARD_SHEET = "02_Operating_Board";
const FORM_RESPONSES_SHEET = "Form Responses 1";

/**
 * Row 1 on 02_Operating_Board must use these exact headers in this order.
 * See GOOGLE_SHEET_MODEL_AR.md
 */
const BOARD_COLUMN_ORDER = [
  "submitted_at",
  "lead_name",
  "company",
  "website",
  "sector",
  "city",
  "goal",
  "ideal_customer",
  "offer",
  "contact_method",
  "whatsapp_or_email",
  "has_list",
  "business_type",
  "source",
  "consent",
  "consent_source",
  "meeting_status",
  "diagnostic_status",
  "pilot_status",
  "proof_pack_status",
  "recommended_service",
  "next_step",
  "diagnostic_card",
  "owner",
  "invoice_link",
  "last_touch_at",
  "notes",
];

/************************************
 * SETUP
 ************************************/
function setupDealixTrigger() {
  const ss = SpreadsheetApp.getActive();
  ScriptApp.newTrigger("onDealixFormSubmit")
    .forSpreadsheet(ss)
    .onFormSubmit()
    .create();
}

/************************************
 * MAIN FORM HANDLER
 ************************************/
function onDealixFormSubmit(e) {
  if (!e || !e.range) {
    return;
  }
  const sh = e.range.getSheet();
  if (sh.getName() !== FORM_RESPONSES_SHEET) {
    return;
  }
  const rowIndex = e.range.getRow();
  const lastCol = sh.getLastColumn();
  const headers = sh.getRange(1, 1, 1, lastCol).getValues()[0];
  const rowVals = sh.getRange(rowIndex, 1, rowIndex, lastCol).getValues()[0];
  const row = {};
  for (var i = 0; i < headers.length; i++) {
    row[String(headers[i]).trim()] = rowVals[i];
  }

  row._source_sheet = "form";
  var payload = buildOperatingPayload_(row);
  appendToOperatingBoard_(payload);
  sendOwnerAlert_(payload);
}

/************************************
 * TEST
 ************************************/
function testInsertRow() {
  var fake = {
    Timestamp: new Date(),
    "الاسم الكامل": "Sami Test",
    "اسم الشركة": "وكالة تجربة",
    "رابط الموقع": "",
    القطاع: "وكالة/مسوق",
    المدينة: "الرياض",
    "ما هدفك الآن؟": "أبغى عملاء",
    "وصف العميل المثالي": "شركات B2B",
    "ماذا تقدّم للسوق اليوم؟": "تسويق أداء",
    "أفضل طريقة للتواصل": "WhatsApp",
    "رقم الواتساب أو الإيميل": "966500000000",
    "هل عندك قائمة عملاء محتملين؟": "لا",
    "نوع النشاط": "Agency",
    "الموافقة": "نعم",
  };
  fake._source_sheet = "test";
  var payload = buildOperatingPayload_(fake);
  appendToOperatingBoard_(payload);
  sendOwnerAlert_(payload);
}

/************************************
 * MAPPING
 ************************************/
function mapRecommendedService_(row) {
  var goal = normalizeArabic_(safeString_(row["ما هدفك الآن؟"] || row.goal || ""));
  var sector = normalizeArabic_(safeString_(row["القطاع"] || row.sector || ""));
  var hasList = normalizeArabic_(safeString_(row["هل عندك قائمة عملاء محتملين؟"] || row.has_list || ""));

  if (goal.indexOf("اجتماع") !== -1) {
    return "Meeting Sprint";
  }
  if (goal.indexOf("شراك") !== -1) {
    return "Partnership Growth";
  }
  if (hasList.indexOf("نعم") !== -1 || hasList === "yes" || hasList === "true") {
    return "Data to Revenue";
  }
  if (sector.indexOf("وكال") !== -1 || sector.indexOf("مسوق") !== -1) {
    return "Agency Partner Pilot";
  }
  if (goal.indexOf("عملاء") !== -1 || goal.indexOf("عميل") !== -1) {
    return "Growth Starter";
  }
  return "Growth Starter";
}

function buildNextStep_(row, service) {
  if (service === "Meeting Sprint") {
    return "جهّز رسائل تأهيل + متابعة 24h + جدولة اجتماع";
  }
  if (service === "Partnership Growth") {
    return "حدد 5 شركاء محتملين + رسائل عربية قصيرة";
  }
  if (service === "Data to Revenue") {
    return "صنّف القائمة + رسائل حسب الشريحة";
  }
  if (service === "Agency Partner Pilot") {
    return "جهّز Mini Diagnostic لعميل واحد للوكالة";
  }
  return "جهّز Mini Diagnostic خلال 24 ساعة ثم عرض Pilot 499";
}

function buildRiskNote_(row) {
  var consent = normalizeArabic_(safeString_(row["الموافقة"] || row.consent || ""));
  if (consent.indexOf("نعم") === -1 && consent.indexOf("yes") === -1) {
    return "لا تواصل تسويقي بدون موافقة صريحة.";
  }
  return "لا واتساب بارد؛ قنوات inbound أو opt-in فقط.";
}

function buildRecommendedChannel_(row) {
  var method = safeString_(row["أفضل طريقة للتواصل"] || row.contact_method || "");
  if (/whatsapp|واتس/i.test(method)) {
    return "WhatsApp (بعد أن يبدأ العميل أو يوافق)";
  }
  return "Email / رد يدوي بعد التأهيل";
}

/************************************
 * CARD GENERATION
 ************************************/
function buildDiagnosticCard_(row) {
  var name = safeString_(row["الاسم الكامل"] || row.lead_name || "العميل");
  var company = safeString_(row["اسم الشركة"] || row.company || "—");
  var sector = safeString_(row["القطاع"] || row.sector || "—");
  var goal = safeString_(row["ما هدفك الآن؟"] || row.goal || "—");
  var offer = safeString_(row["ماذا تقدّم للسوق اليوم؟"] || row.offer || "—");
  var ideal = safeString_(row["وصف العميل المثالي"] || row.ideal_customer || "—");
  var service = mapRecommendedService_(row);
  var channel = buildRecommendedChannel_(row);
  var risk = buildRiskNote_(row);

  var lines = [
    "📊 Dealix Mini Diagnostic",
    "",
    "الشركة: " + company,
    "القطاع: " + sector,
    "الهدف: " + goal,
    "",
    "1. أفضل شريحة تبدأ بها:",
    "[" + ideal + "]",
    "",
    "2. لماذا هذه الشريحة:",
    "- تطابق الهدف: " + goal,
    "- تطابق العرض: " + offer,
    "- الخدمة المقترحة: " + service,
    "",
    "3. 3 فرص مناسبة:",
    "- [opportunity_1] راجع يدوياً حسب القطاع",
    "- [opportunity_2]",
    "- [opportunity_3]",
    "",
    "4. رسالة عربية جاهزة:",
    "السلام عليكم " + name + "،",
    "[draft_message — خصص قبل الإرسال]",
    "",
    "5. القناة المقترحة:",
    channel,
    "",
    "6. مخاطرة يجب تجنبها:",
    risk,
    "",
    "7. الخطوة القادمة:",
    "Pilot 499 لمدة 7 أيام.",
  ];
  return lines.join("\n");
}

/************************************
 * WRITE TO BOARD
 ************************************/
function appendToOperatingBoard_(payload) {
  var ss = SpreadsheetApp.getActive();
  var board = ss.getSheetByName(OPERATING_BOARD_SHEET);
  if (!board) {
    throw new Error("Missing sheet: " + OPERATING_BOARD_SHEET);
  }
  var newRow = BOARD_COLUMN_ORDER.map(function (key) {
    var v = payload[key];
    return v === undefined || v === null ? "" : v;
  });
  board.appendRow(newRow);
}

/************************************
 * NOTIFICATIONS
 ************************************/
function sendOwnerAlert_(payload) {
  if (!OWNER_EMAIL || OWNER_EMAIL.indexOf("@") === -1) {
    return;
  }
  var subject = "[Dealix] Lead جديد — " + safeString_(payload.company);
  var body =
    "شركة: " +
    payload.company +
    "\nاسم: " +
    payload.lead_name +
    "\nالهدف: " +
    payload.goal +
    "\nالخدمة المقترحة: " +
    payload.recommended_service +
    "\nالخطوة: " +
    payload.next_step +
    "\n\n" +
    "رابط واتساب (تذكير): " +
    WHATSAPP_LINK;
  MailApp.sendEmail({
    to: OWNER_EMAIL,
    subject: subject,
    body: body,
  });
}

/************************************
 * HELPERS
 ************************************/
function normalizeArabic_(value) {
  return safeString_(value)
    .replace(/[\u064B-\u065F\u0670]/g, "")
    .replace(/\s+/g, " ")
    .trim()
    .toLowerCase();
}

function safeString_(value) {
  if (value === null || value === undefined) {
    return "";
  }
  if (value instanceof Date) {
    return value.toISOString();
  }
  return String(value).trim();
}

function now_() {
  return new Date();
}

/**
 * Builds the flat payload used by append + email.
 * Adjust keys here if your Form column titles differ from the Arabic defaults in testInsertRow.
 */
function buildOperatingPayload_(row) {
  var consentRaw = safeString_(row["الموافقة"] || row.consent || "");
  var consentOk = /نعم|yes|true|1/i.test(consentRaw);
  var source = row._source_sheet === "test" ? "manual_test" : "google_form";
  var consentSource = consentOk ? "form_opt_in" : "form_no_consent";

  var company = safeString_(row["اسم الشركة"] || row.company);
  var goal = safeString_(row["ما هدفك الآن؟"] || row.goal);
  var service = mapRecommendedService_(row);

  return {
    submitted_at: row.Timestamp || row.submitted_at || now_(),
    lead_name: safeString_(row["الاسم الكامل"] || row.lead_name),
    company: company,
    website: safeString_(row["رابط الموقع"] || row.website),
    sector: safeString_(row["القطاع"] || row.sector),
    city: safeString_(row["المدينة"] || row.city),
    goal: goal,
    ideal_customer: safeString_(row["وصف العميل المثالي"] || row.ideal_customer),
    offer: safeString_(row["ماذا تقدّم للسوق اليوم؟"] || row.offer),
    contact_method: safeString_(row["أفضل طريقة للتواصل"] || row.contact_method),
    whatsapp_or_email: safeString_(row["رقم الواتساب أو الإيميل"] || row.whatsapp_or_email),
    has_list: safeString_(row["هل عندك قائمة عملاء محتملين؟"] || row.has_list),
    business_type: safeString_(row["نوع النشاط"] || row.business_type),
    source: source,
    consent: consentOk ? "نعم" : "لا",
    consent_source: consentSource,
    meeting_status: "not_booked",
    diagnostic_status: consentOk ? "new" : "waiting_data",
    pilot_status: "not_offered",
    proof_pack_status: "not_started",
    recommended_service: service,
    next_step: buildNextStep_(row, service),
    diagnostic_card: buildDiagnosticCard_(row),
    owner: OWNER_EMAIL,
    invoice_link: "",
    last_touch_at: now_(),
    notes: row._source_sheet === "test" ? "testInsertRow" : "",
  };
}
