// static/js/project.js

async function fetchJSON(path) {
  const res = await fetch(path);
  if (!res.ok) throw new Error(res.statusText);
  return res.json();
}

// DOM
const loadingEl    = document.getElementById('loading');
const errorEl      = document.getElementById('error');
const emptyStateEl = document.getElementById('empty-state');
const devicesGrid  = document.getElementById('devices-container');
const projectNameEl= document.getElementById('project-name');
const deviceCountEl= document.getElementById('device-count');
const avgMeanEl    = document.getElementById('avg-mean');
const avgStdEl     = document.getElementById('avg-std');
const avgVarEl     = document.getElementById('avg-var');

function show(el)    { el.classList.remove('hidden'); }
function hide(el)    { el.classList.add('hidden'); }
function goBack()    { window.history.back(); }

function renderProjectHeader(project, devices) {
  projectNameEl.textContent = project.name;
  deviceCountEl.textContent = devices.length;
  if (!devices.length) {
    avgMeanEl.textContent = avgStdEl.textContent = avgVarEl.textContent = '0.00';
    return;
  }
  const sumMean = devices.reduce((s,d)=>s+d.mean_delta,0);
  const sumStd  = devices.reduce((s,d)=>s+d.std_delta,0);
  const sumVar  = devices.reduce((s,d)=>s+d.var_delta,0);
  avgMeanEl.textContent = (sumMean/devices.length).toFixed(2);
  avgStdEl.textContent  = (sumStd/devices.length).toFixed(2);
  avgVarEl.textContent  = (sumVar/devices.length).toFixed(2);
}

// Función global para navegar al detalle de un dispositivo
function viewDevice(deviceId) {
  window.location.href = `/dispositivo/${deviceId}`;
}

function renderDevices(devices) {
  if (!devices.length) {
    hide(devicesGrid);
    show(emptyStateEl);
    return;
  }
  hide(emptyStateEl);
  devicesGrid.innerHTML = devices.map(d=>`
    <div class="device-card" onclick="viewDevice(${d.id})">
      <p class="device-id">Dispositivo ${d.id}</p>
      <div class="device-stats">
        <div class="device-stat-item">
          <div class="device-stat-value">${d.mean_delta.toFixed(2)}</div>
          <div class="device-stat-label">Media Δ</div>
        </div>
        <div class="device-stat-item">
          <div class="device-stat-value">${d.std_delta.toFixed(2)}</div>
          <div class="device-stat-label">Desv. Est. Δ</div>
        </div>
        <div class="device-stat-item">
          <div class="device-stat-value">${d.var_delta.toFixed(2)}</div>
          <div class="device-stat-label">Varianza Δ</div>
        </div>
      </div>
    </div>
  `).join('');
  show(devicesGrid);
}

document.addEventListener('DOMContentLoaded', async () => {
  try {
    show(loadingEl);
    hide(errorEl);
    hide(devicesGrid);
    hide(emptyStateEl);

    // Llamadas a la API bajo /api
    const project = await fetchJSON(`/api/projects/${PROJECT_ID}`);
    const devices = await fetchJSON(`/api/devices?project_id=${PROJECT_ID}`);

    renderProjectHeader(project, devices);
    renderDevices(devices);
  } catch (e) {
    console.error(e);
    hide(devicesGrid);
    hide(emptyStateEl);
    show(errorEl);
  } finally {
    hide(loadingEl);
  }
});

// ws-client.js
const socket = new WebSocket(`ws://${location.host}/ws/updates`);

// Icono flotante
const notif = document.createElement('div');
notif.id = 'notif-icon';
document.body.appendChild(notif);

socket.onmessage = ({ data }) => {
  const msg = JSON.parse(data);
  if (msg.type === 'new_record') {
    // actualizas tu tabla (p.ej. refetch de /audit_data)
  }
  else if (msg.type === 'alert') {
    const badge = document.createElement('div');
    badge.className = 'toast';
    badge.textContent = msg.message;
    notif.appendChild(badge);
    setTimeout(() => badge.remove(), 5000);
  }
};
