/* ========== Dealix WebSocket ==========
 * Auto-reconnect with backoff, event dispatch to window.
 */

const WS = {
  conn: null,
  backoff: 1000,
  maxBackoff: 30000,
  connected: false,
  closing: false,
  heartbeat: null,

  connect() {
    if (!window.Auth || !Auth.token) return;
    if (this.conn && this.conn.readyState < 2) return;
    this.closing = false;

    let url;
    try { url = window.apiClient.wsUrl(); } catch { return; }

    try {
      this.conn = new WebSocket(url);
    } catch (err) {
      console.warn('[WS] connect failed', err);
      this._scheduleReconnect();
      return;
    }

    this.conn.addEventListener('open', () => {
      this.connected = true;
      this.backoff = 1000;
      window.dispatchEvent(new CustomEvent('dealix:ws-status', { detail: { connected: true } }));
      // heartbeat ping
      this.heartbeat = setInterval(() => {
        try { this.conn && this.conn.readyState === 1 && this.conn.send(JSON.stringify({ type: 'ping' })); } catch {}
      }, 25000);
    });

    this.conn.addEventListener('message', (ev) => {
      let data;
      try { data = JSON.parse(ev.data); } catch { return; }
      if (!data || !data.type) return;
      window.dispatchEvent(new CustomEvent('dealix:ws:' + data.type, { detail: data.payload || {} }));
      window.dispatchEvent(new CustomEvent('dealix:ws-any', { detail: data }));
    });

    this.conn.addEventListener('close', () => {
      this.connected = false;
      if (this.heartbeat) { clearInterval(this.heartbeat); this.heartbeat = null; }
      window.dispatchEvent(new CustomEvent('dealix:ws-status', { detail: { connected: false } }));
      if (!this.closing) this._scheduleReconnect();
    });

    this.conn.addEventListener('error', () => {
      try { this.conn.close(); } catch {}
    });
  },

  _scheduleReconnect() {
    const delay = Math.min(this.backoff, this.maxBackoff);
    setTimeout(() => this.connect(), delay);
    this.backoff = Math.min(this.backoff * 1.7, this.maxBackoff);
  },

  disconnect() {
    this.closing = true;
    if (this.heartbeat) clearInterval(this.heartbeat);
    try { this.conn && this.conn.close(); } catch {}
    this.conn = null;
    this.connected = false;
  }
};

window.WS = WS;
