// Variables globales
let projects = [];
let devices = [];

// Colores para los proyectos (se asignan cíclicamente)
const projectColors = [
  '#eef5fb',
  '#f9eef6',
  '#fdefe3',
  '#e9f7ec',
  '#fef3c7',
  '#ede9fe',
  '#f0f9ff',
  '#fdf2f8'
];

// Elementos del DOM
const loadingElement = document.getElementById('loading');
const errorElement = document.getElementById('error');
const cardsContainer = document.getElementById('cards-container');
const emptyStateElement = document.getElementById('empty-state');

// Función para mostrar/ocultar elementos
function showElement(element) {
  element.classList.remove('hidden');
}

function hideElement(element) {
  element.classList.add('hidden');
}

// Función para obtener proyectos desde la API
async function fetchProjects() {
  try {
    const response = await fetch('http://localhost:8000/api/projects');
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching projects:', error);
    throw error;
  }
}

// Función para obtener dispositivos desde la API
async function fetchDevices() {
  try {
    const response = await fetch('http://localhost:8000/api/devices');
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching devices:', error);
    throw error;
  }
}

// Función para contar dispositivos por proyecto
function countDevicesByProject(projectId) {
  return devices.filter(device => device.project_id === projectId).length;
}

// Función para obtener estadísticas de dispositivos por proyecto
function getDeviceStats(projectId) {
  const projectDevices = devices.filter(device => device.project_id === projectId);
  
  if (projectDevices.length === 0) {
    return { mean: 0, std: 0, variance: 0 };
  }

  // Calcular promedios
  const avgMean = projectDevices.reduce((sum, device) => sum + device.mean_delta, 0) / projectDevices.length;
  const avgStd = projectDevices.reduce((sum, device) => sum + device.std_delta, 0) / projectDevices.length;
  const avgVar = projectDevices.reduce((sum, device) => sum + device.var_delta, 0) / projectDevices.length;

  return {
    mean: avgMean.toFixed(2),
    std: avgStd.toFixed(2),
    variance: avgVar.toFixed(2)
  };
}

// Función para crear una tarjeta de proyecto
function createProjectCard(project, index) {
  const deviceCount = countDevicesByProject(project.id);
  const stats = getDeviceStats(project.id);
  const backgroundColor = projectColors[index % projectColors.length];
  
  return `
    <div class="card" data-project-id="${project.id}">
      <div class="card-header" style="--label-bg: ${backgroundColor};">
        <div class="project-info">
          <h2 class="project-name">${project.name}</h2>
          <p class="project-id">ID: ${project.id}</p>
        </div>
        <div class="device-count">
          <div class="device-number">${deviceCount}</div>
          <div class="device-label">Dispositivos</div>
        </div>
      </div>
      <div class="card-content">
        <div class="card-actions">
          <button class="btn primary" onclick="viewDashboard(${project.id})">
            Ver Dashboard
          </button>
        <div class="device-stats">
            <div class="stat-item">
              <div class="stat-value">${stats.mean}</div>
              <div class="stat-label">Media</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">${stats.std}</div>
              <div class="stat-label">Desv. Est.</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">${stats.variance}</div>
              <div class="stat-label">Varianza</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `;
}

// Función para renderizar las tarjetas de proyectos
function renderProjects() {
  if (projects.length === 0) {
    hideElement(cardsContainer);
    showElement(emptyStateElement);
    return;
  }

  hideElement(emptyStateElement);
  
  const cardsHTML = projects.map((project, index) => createProjectCard(project, index)).join('');
  cardsContainer.innerHTML = cardsHTML;
  
  showElement(cardsContainer);
}

// Función para cargar todos los datos
async function loadProjects() {
  try {
    // Mostrar loading
    showElement(loadingElement);
    hideElement(errorElement);
    hideElement(cardsContainer);
    hideElement(emptyStateElement);

    // Cargar proyectos y dispositivos en paralelo
    const [projectsData, devicesData] = await Promise.all([
      fetchProjects(),
      fetchDevices()
    ]);

    // Actualizar variables globales
    projects = projectsData;
    devices = devicesData;

    // Ocultar loading
    hideElement(loadingElement);

    // Renderizar proyectos
    renderProjects();

    console.log('Datos cargados exitosamente:', {
      projects: projects.length,
      devices: devices.length
    });

  } catch (error) {
    console.error('Error loading data:', error);
    
    // Ocultar loading
    hideElement(loadingElement);
    hideElement(cardsContainer);
    hideElement(emptyStateElement);
    
    // Mostrar error
    showElement(errorElement);
  }
}

// Funciones para manejar acciones de botones
function viewDashboard(projectId) {
    window.location.href = `/projects/${projectId}`;
}

// Función para actualizar los datos (útil para refresh)
function refreshData() {
  loadProjects();
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
  // Cargar datos al iniciar la página
  loadProjects();
  
  // Opcional: Actualizar datos cada 30 segundos
  // setInterval(refreshData, 30000);
});

// Hacer disponibles las funciones globalmente
window.loadProjects = loadProjects;
window.viewDashboard = viewDashboard;
window.refreshData = refreshData;


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
