// gate.js - Password gate for restricted LA pages
// Password: 'pratt', cookie: tbc_la_auth, 30-day expiry
(function() {
  var PASS = 'pratt';
  var COOKIE = 'tbc_la_auth';
  var DAYS = 30;

  function getCookie(name) {
    var match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? match[2] : null;
  }

  function setCookie(name, val, days) {
    var d = new Date();
    d.setTime(d.getTime() + days * 86400000);
    document.cookie = name + '=' + val + ';expires=' + d.toUTCString() + ';path=/la/';
  }

  if (getCookie(COOKIE) === '1') {
    document.documentElement.classList.add('gate-unlocked');
    return;
  }

  var overlay = document.createElement('div');
  overlay.id = 'gate-overlay';
  overlay.innerHTML =
    '<div id="gate-modal">' +
      '<p style="font-family:Georgia,serif;font-size:14px;color:#111;margin:0 0 16px;font-weight:700;letter-spacing:1px;">THIS SECTION IS RESTRICTED</p>' +
      '<input type="password" id="gate-input" placeholder="Password" style="font-family:Georgia,serif;font-size:14px;padding:6px 10px;border:1px solid #ccc;width:200px;display:block;margin:0 0 12px;">' +
      '<button id="gate-submit" style="font-family:Georgia,serif;font-size:11px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:#fff;background:#1e3a5f;border:none;padding:6px 20px;cursor:pointer;">Enter</button>' +
      '<p id="gate-error" style="font-family:Georgia,serif;font-size:12px;color:#c00;margin:8px 0 0;display:none;">Incorrect password.</p>' +
    '</div>';

  var style = document.createElement('style');
  style.textContent =
    '#gate-overlay{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(255,255,255,0.97);z-index:9999;display:flex;align-items:center;justify-content:center;}' +
    '#gate-modal{text-align:center;}' +
    '#gate-input:focus{outline:none;border-color:#1e3a5f;}' +
    '#gate-submit:hover{background:#2a4a73;}' +
    '@keyframes shake{0%,100%{transform:translateX(0)}25%{transform:translateX(-6px)}75%{transform:translateX(6px)}}' +
    '.shake{animation:shake 0.3s ease-in-out;}';

  document.head.appendChild(style);
  document.body.appendChild(overlay);

  function tryPassword() {
    var input = document.getElementById('gate-input');
    if (input.value === PASS) {
      setCookie(COOKIE, '1', DAYS);
      overlay.remove();
      document.documentElement.classList.add('gate-unlocked');
    } else {
      var modal = document.getElementById('gate-modal');
      modal.classList.remove('shake');
      void modal.offsetWidth;
      modal.classList.add('shake');
      document.getElementById('gate-error').style.display = 'block';
      input.value = '';
      input.focus();
    }
  }

  document.getElementById('gate-submit').addEventListener('click', tryPassword);
  document.getElementById('gate-input').addEventListener('keydown', function(e) {
    if (e.key === 'Enter') tryPassword();
  });

  setTimeout(function() { document.getElementById('gate-input').focus(); }, 100);
})();
