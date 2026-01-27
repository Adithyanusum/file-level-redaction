async function doSignup(){
  const u = document.getElementById('signupUser').value;
  const p = document.getElementById('signupPass').value;
  if(!u || !p) return alert('enter username and password');
  const res = await fetch('/signup', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({username:u,password:p})});
  if(!res.ok){ const j = await res.json(); return alert('error: '+(j.detail||res.status)); }
  const j = await res.json();
  localStorage.setItem('token', j.token);
  window.location = '/static/index.html';
}

async function doLogin(){
  const u = document.getElementById('loginUser').value;
  const p = document.getElementById('loginPass').value;
  if(!u || !p) return alert('enter username and password');
  const res = await fetch('/login', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({username:u,password:p})});
  if(!res.ok){ const j = await res.json(); return alert('error: '+(j.detail||res.status)); }
  const j = await res.json();
  localStorage.setItem('token', j.token);
  window.location = '/static/index.html';
}

// attach quick logout if on index page
if(window.location.pathname.endsWith('index.html')){
  const btn = document.createElement('button'); btn.style.marginLeft='8px'; btn.textContent='Logout';
  btn.onclick = ()=>{ localStorage.removeItem('token'); window.location='/static/login.html'; };
  document.addEventListener('DOMContentLoaded', ()=>{
    const h = document.querySelector('h1'); if(h) h.appendChild(btn);
  });
}

// Guest signin
async function doGuest(){
  const res = await fetch('/guest', {method:'POST'});
  if(!res.ok) return alert('guest signin failed');
  const j = await res.json();
  localStorage.setItem('token', j.token);
  window.location = '/static/index.html';
}

// Google credential handler
async function handleCredentialResponse(response){
  if(!response || !response.credential) return;
  const id_token = response.credential;
  const res = await fetch('/auth/google', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({id_token})});
  if(!res.ok){ const j = await res.json().catch(()=>({detail:'error'})); return alert('google signin failed: '+(j.detail||res.status)); }
  const j = await res.json();
  localStorage.setItem('token', j.token);
  window.location = '/static/index.html';
}

// Expose handler globally for Google's callback
window.handleCredentialResponse = handleCredentialResponse;
