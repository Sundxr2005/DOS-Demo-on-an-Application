// small UI behaviors for the demo bank
const pingBtn = document.getElementById('pingBtn');
const pingResult = document.getElementById('pingResult');
const lastAccess = document.getElementById('lastAccess');
const loginBtn = document.getElementById('loginBtn');
const loginModal = document.getElementById('loginModal');
const closeModal = document.getElementById('closeModal');
const loginForm = document.getElementById('loginForm');
const transferForm = document.getElementById('transferForm');
const clearBtn = document.getElementById('clearBtn');

function nowTime() {
  return new Date().toLocaleString();
}
lastAccess.textContent = nowTime();

pingBtn.addEventListener('click', async () => {
  pingResult.textContent = 'Status: pinging...';
  try {
    const r = await fetch('/');
    pingResult.textContent = `Status: ${r.status} (${r.statusText}) — ${nowTime()}`;
  } catch (e) {
    pingResult.textContent = `Error: ${e.message}`;
  }
});

// login modal
loginBtn.addEventListener('click', () => loginModal.classList.remove('hidden'));
closeModal.addEventListener('click', () => loginModal.classList.add('hidden'));
loginForm.addEventListener('submit', (ev) => {
  ev.preventDefault();
  alert('This is a demo login. Do not enter real credentials.');
  loginModal.classList.add('hidden');
});

// transfer demo
transferForm.addEventListener('submit', (ev) => {
  ev.preventDefault();
  alert('Transfer simulated (DEMO). No real money moved.');
});
clearBtn.addEventListener('click', () => transferForm.reset());

// small auto-refresh of last access time
setInterval(()=> lastAccess.textContent = nowTime(), 60*1000);
