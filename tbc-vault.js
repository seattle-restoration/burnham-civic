// Burnham Civic vault: in-browser decrypt for envelope-encrypted content.
// Payloads are produced by vault-encrypt.mjs. A payload's content is AES-GCM
// encrypted under a random content key; that key is wrapped per passphrase
// (PBKDF2-SHA256 + AES-GCM). Any listed passphrase unlocks the content.
(function(){
  function b64(x){var b=atob(x),a=new Uint8Array(b.length);for(var i=0;i<b.length;i++)a[i]=b.charCodeAt(i);return a.buffer;}
  async function unwrap(payload, pw){
    var enc=new TextEncoder();
    var km=await crypto.subtle.importKey('raw',enc.encode(pw),'PBKDF2',false,['deriveKey']);
    for(var i=0;i<payload.wraps.length;i++){
      var w=payload.wraps[i];
      try{
        var kek=await crypto.subtle.deriveKey({name:'PBKDF2',salt:b64(w.salt),iterations:payload.iter,hash:'SHA-256'},km,{name:'AES-GCM',length:256},false,['decrypt']);
        var raw=await crypto.subtle.decrypt({name:'AES-GCM',iv:b64(w.iv)},kek,b64(w.wk));
        return await crypto.subtle.importKey('raw',raw,{name:'AES-GCM'},false,['decrypt']);
      }catch(e){}
    }
    return null;
  }
  // Decrypt payload with passphrase; resolves to string or null.
  window.tbcVaultOpen=async function(payload, pw){
    var cek=await unwrap(payload, pw);
    if(!cek) return null;
    try{
      var pt=await crypto.subtle.decrypt({name:'AES-GCM',iv:b64(payload.iv)},cek,b64(payload.ct));
      return new TextDecoder().decode(pt);
    }catch(e){return null;}
  };
  // Fetch an .enc payload file and decrypt it; resolves to string or null.
  window.tbcVaultFetch=async function(url, pw){
    var r=await fetch(url,{cache:'force-cache'});
    if(!r.ok) return null;
    return tbcVaultOpen(await r.json(), pw);
  };
  // Standard members-page unlock: decrypt payload, inject into .members-content,
  // remember passphrase in localStorage under lsk, flip body class.
  window.tbcMembersUnlock=async function(payload, pw, lsk){
    var html=await tbcVaultOpen(payload, pw);
    if(html===null) return false;
    document.querySelector('.members-content').innerHTML=html;
    document.body.classList.add('tbc-member');
    try{localStorage.setItem(lsk,pw);}catch(e){}
    return true;
  };
  // Wire the standard lockpanel form: tbcMembersGate(payload, inputId, lsk)
  window.tbcMembersGate=function(payload, inputId, lsk){
    window.tbcTryPw=function(id){
      var inp=document.getElementById(id||inputId);
      tbcMembersUnlock(payload, inp.value, lsk).then(function(ok){
        if(!ok){var e=document.getElementById((id||inputId)+'-err');if(e)e.style.display='block';inp.value='';}
      });
      return false;
    };
    var saved=null;
    try{saved=localStorage.getItem(lsk);}catch(e){}
    if(saved){tbcMembersUnlock(payload, saved, lsk);}
  };
  // Whole-page unlock: decrypt full original HTML and replace the document.
  window.tbcPageUnlock=async function(payload, pw, lsk){
    var html=await tbcVaultOpen(payload, pw);
    if(html===null) return false;
    try{localStorage.setItem(lsk,pw);}catch(e){}
    document.open();document.write(html);document.close();
    return true;
  };
})();
