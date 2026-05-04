/* =============================================================
   Dealix Frontend — onboarding-wizard.js
   4-step public wizard:
     1. Company basics
     2. Bundle intake (loaded from /api/v1/services/{id}/intake-questions)
     3. Contact email + send magic-link
     4. Confirmation + ETA

   Submits to: POST /api/v1/onboarding/submit
   Magic-link send: POST /api/v1/auth/magic-link/send (silent failure ok)
   ETA hook:        GET  /api/v1/onboarding/eta

   Failure mode: any network error keeps the user on the current step
   with a visible error banner — the wizard never breaks the page.
   ============================================================= */
(function () {
  'use strict';

  var api = window.DealixAPI;
  if (!api) {
    console.warn('[wizard] DealixAPI not loaded — wizard disabled');
    return;
  }

  var BUNDLE_ID = 'free_diagnostic';
  var STATE = {
    step: 1,
    answers: {},
  };

  function $(id) { return document.getElementById(id); }
  function setError(msg) {
    var e = $('dx-wizard-error');
    if (!e) return;
    if (!msg) { e.classList.remove('is-shown'); e.textContent = ''; return; }
    e.textContent = msg;
    e.classList.add('is-shown');
  }

  function showStep(n) {
    STATE.step = n;
    var steps = document.querySelectorAll('[data-step]');
    Array.prototype.forEach.call(steps, function (el) {
      var s = parseInt(el.getAttribute('data-step'), 10);
      if (s === n) {
        el.removeAttribute('hidden');
        el.classList.add('is-active');
      } else {
        el.setAttribute('hidden', '');
        el.classList.remove('is-active');
      }
    });
    var inds = document.querySelectorAll('[data-step-indicator]');
    Array.prototype.forEach.call(inds, function (el) {
      var s = parseInt(el.getAttribute('data-step-indicator'), 10);
      el.classList.remove('dx-wizard__step--active', 'dx-wizard__step--done');
      if (s < n) el.classList.add('dx-wizard__step--done');
      else if (s === n) el.classList.add('dx-wizard__step--active');
    });
    $('dx-btn-back').hidden = n === 1 || n === 4;
    $('dx-btn-next').hidden = n === 4 || n === 3;
    $('dx-btn-submit').hidden = n !== 3;
    setError('');
    track('wizard_step_view', { step: n });
  }

  function track(name, props) {
    try {
      if (window.posthog && typeof window.posthog.capture === 'function') {
        window.posthog.capture(name, props || {});
      }
    } catch (_) { /* swallow */ }
  }

  async function loadIntake() {
    var holder = $('dx-intake-questions');
    if (!holder) return;
    var r = await api.get('/api/v1/services/' + encodeURIComponent(BUNDLE_ID) + '/intake-questions');
    var qs = (r && r.ok && r.data && Array.isArray(r.data.questions)) ? r.data.questions : [];
    if (!qs.length) {
      holder.innerHTML = '<p style="color:var(--dx-muted)">لا توجد أسئلة لهذا الـ bundle — تخطّى للخطوة التالية.</p>';
      return;
    }
    holder.innerHTML = '';
    qs.slice(0, 6).forEach(function (q) {
      var wrap = document.createElement('div');
      wrap.className = 'dx-form-group';
      var label = document.createElement('label');
      label.htmlFor = 'dx-q-' + q.key;
      label.textContent = q.label_ar + (q.required === 'true' || q.required === true ? ' *' : '');
      wrap.appendChild(label);
      var input;
      if (q.type === 'textarea') {
        input = document.createElement('textarea');
        input.rows = 3;
      } else if (q.type === 'select') {
        input = document.createElement('select');
        var opts = ['—', 'نعم', 'لا', 'لست متأكداً'];
        opts.forEach(function (o) {
          var op = document.createElement('option');
          op.value = o === '—' ? '' : o;
          op.textContent = o;
          input.appendChild(op);
        });
      } else {
        input = document.createElement('input');
        input.type = (q.type === 'number') ? 'number' : (q.type === 'email' ? 'email' : 'text');
      }
      input.id = 'dx-q-' + q.key;
      input.dataset.qkey = q.key;
      input.dataset.required = q.required === 'true' || q.required === true ? '1' : '0';
      wrap.appendChild(input);
      holder.appendChild(wrap);
    });
  }

  function collectIntake() {
    var inputs = document.querySelectorAll('#dx-intake-questions [data-qkey]');
    var out = {};
    var missing = [];
    Array.prototype.forEach.call(inputs, function (el) {
      var k = el.dataset.qkey;
      var v = (el.value || '').trim();
      out[k] = v;
      if (el.dataset.required === '1' && !v) missing.push(k);
    });
    return { answers: out, missing: missing };
  }

  function validateStep1() {
    var company = ($('dx-company-name').value || '').trim();
    if (!company) { setError('يرجى إدخال اسم الشركة.'); return false; }
    STATE.answers.company_name = company;
    STATE.answers.sector = ($('dx-sector').value || '').trim();
    STATE.answers.monthly_revenue_band = $('dx-revenue-band').value;
    return true;
  }

  function validateStep2() {
    var c = collectIntake();
    if (c.missing.length) {
      setError('يرجى إكمال الحقول المطلوبة: ' + c.missing.join('، '));
      return false;
    }
    STATE.answers.intake_answers = c.answers;
    return true;
  }

  function validateStep3() {
    var email = ($('dx-contact-email').value || '').trim().toLowerCase();
    var emailRe = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
    if (!emailRe.test(email)) { setError('بريد إلكتروني غير صالح.'); return false; }
    STATE.answers.contact_email = email;
    STATE.answers.contact_name = ($('dx-contact-name').value || '').trim();
    return true;
  }

  async function submit() {
    if (!validateStep3()) return;
    var btn = $('dx-btn-submit');
    btn.disabled = true;
    btn.textContent = 'جاري الإرسال…';
    track('wizard_submit_start', {});

    var payload = {
      company_name: STATE.answers.company_name,
      sector: STATE.answers.sector,
      monthly_revenue_band: STATE.answers.monthly_revenue_band,
      contact_name: STATE.answers.contact_name,
      contact_email: STATE.answers.contact_email,
      bundle_id: BUNDLE_ID,
      intake_answers: STATE.answers.intake_answers || {},
      locale: 'ar',
    };

    var r = await api.post('/api/v1/onboarding/submit', payload);
    if (!r.ok) {
      btn.disabled = false;
      btn.textContent = 'إرسال';
      setError('حصل خطأ في الإرسال — حاول مجدداً أو راسلنا على support.');
      track('wizard_submit_error', { status: r.status, error: r.error });
      return;
    }

    // Fire-and-forget magic-link (silent fail ok — gate may be False)
    api.post('/api/v1/auth/magic-link/send', { email: STATE.answers.contact_email }).catch(function () {});

    // Show confirmation
    showStep(4);
    var nameEl = $('dx-confirmed-name');
    if (nameEl) nameEl.textContent = STATE.answers.contact_name || '';
    var leadLine = $('dx-lead-id-line');
    if (leadLine && r.data && r.data.lead_id) {
      leadLine.textContent = 'مرجع داخلي: ' + r.data.lead_id;
    }
    track('wizard_submit_success', { lead_id: (r.data && r.data.lead_id) || null });

    // Refresh ETA copy
    var eta = await api.get('/api/v1/onboarding/eta');
    var promiseEl = $('dx-eta-promise');
    if (promiseEl && eta && eta.ok && eta.data && eta.data.promise_ar) {
      promiseEl.textContent = eta.data.promise_ar;
    }
  }

  function bind() {
    $('dx-btn-next').addEventListener('click', function () {
      if (STATE.step === 1) {
        if (!validateStep1()) return;
        showStep(2);
        loadIntake();
      } else if (STATE.step === 2) {
        if (!validateStep2()) return;
        showStep(3);
      }
    });
    $('dx-btn-back').addEventListener('click', function () {
      if (STATE.step > 1) showStep(STATE.step - 1);
    });
    $('dx-btn-submit').addEventListener('click', function () {
      submit();
    });
  }

  function init() {
    bind();
    showStep(1);
    track('wizard_start', {});
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
}());
