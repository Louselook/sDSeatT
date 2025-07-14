let allData = [];
let filteredData = [];
let deltaChart = null;
let accumulatedChart = null;
let showOnlyValid = false;

// Elementos del DOM
const elements = {
    dayFilter: document.getElementById('day-filter'),
    hourFilter: document.getElementById('hour-filter'),
    btnData: document.getElementById('btn-data'),
    btnCharts: document.getElementById('btn-charts'),
    dataView: document.getElementById('data-view'),
    chartsView: document.getElementById('charts-view'),
    dataTable: document.getElementById('data-table'),
    recordCount: document.getElementById('record-count'),
    totalRecords: document.getElementById('total-records'),
    validRecords: document.getElementById('valid-records'),
    avgDelta: document.getElementById('avg-delta'),
    lastAccumulated: document.getElementById('last-accumulated'),
    firstRecord: document.getElementById('first-record'),
    lastRecord: document.getElementById('last-record'),
    daysWithData: document.getElementById('days-with-data'),
    btnAllRecords: document.getElementById('btn-all-records'),
    btnValidRecords: document.getElementById('btn-valid-records'),

};

// Event listeners
elements.btnData.addEventListener('click', () => switchView('data'));
elements.btnCharts.addEventListener('click', () => switchView('charts'));
elements.dayFilter.addEventListener('change', filterData);
elements.hourFilter.addEventListener('change', filterData);
elements.btnAllRecords.addEventListener('click', () => {
  showOnlyValid = false;
  updateToggleButtons();
  filterData();
  if (!elements.dataView.classList.contains('hidden')) {
    // Estamos viendo datos → no hacer nada extra
  } else {
    initializeCharts(); // actualiza si estamos en modo gráfico
  }
});

elements.btnValidRecords.addEventListener('click', () => {
  showOnlyValid = true;
  updateToggleButtons();
  filterData();
  if (!elements.dataView.classList.contains('hidden')) {
    // Estamos viendo datos → no hacer nada extra
  } else {
    initializeCharts(); // actualiza si estamos en modo gráfico
  }
});



function goBack() {
    window.history.back();
}

function updateToggleButtons() {
  if (showOnlyValid) {
    elements.btnValidRecords.classList.add('active');
    elements.btnAllRecords.classList.remove('active');
  } else {
    elements.btnAllRecords.classList.add('active');
    elements.btnValidRecords.classList.remove('active');
  }
}


function formatTimestamp(timestamp) {
    return new Date(timestamp).toLocaleString('es-ES', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
    });
}

function formatNumber(num) {
    if (num === null || num === undefined) return '--';
    return typeof num === 'number' ? num.toFixed(2) : num;
}

function switchView(view) {
    if (view === 'data') {
    elements.btnData.classList.add('active');
    elements.btnCharts.classList.remove('active');
    elements.dataView.classList.remove('hidden');
    elements.chartsView.classList.add('hidden');
    } else {
    elements.btnCharts.classList.add('active');
    elements.btnData.classList.remove('active');
    elements.dataView.classList.add('hidden');
    elements.chartsView.classList.remove('hidden');
    initializeCharts();
    }
}

function setupFilters() {
    // Filtrar datos entre 6am y 6pm
    const workingHoursData = allData.filter(item => {
    const hour = new Date(item.timestamp).getHours();
    return hour >= 6 && hour <= 18;
    });

    // Obtener días únicos
    const uniqueDays = [...new Set(workingHoursData.map(item => 
    new Date(item.timestamp).toISOString().split('T')[0]
    ))].sort();

    // Poblar filtro de días
    elements.dayFilter.innerHTML = '<option value="">Todos los días</option>';
    uniqueDays.forEach(day => {
    const option = document.createElement('option');
    option.value = day;
    option.textContent = new Date(day).toLocaleDateString('es-ES');
    elements.dayFilter.appendChild(option);
    });

    // Poblar filtro de horas (6am - 6pm)
    elements.hourFilter.innerHTML = '<option value="">Todas las horas</option>';
    for (let hour = 6; hour <= 18; hour++) {
    const option = document.createElement('option');
    option.value = hour;
    option.textContent = `${hour}:00`;
    elements.hourFilter.appendChild(option);
    }
}

function filterData() {
  const selectedDay = elements.dayFilter.value;
  const selectedHour = elements.hourFilter.value;

  const baseData = showOnlyValid ? allData.filter(item => item.clasificacion === 'valido') : allData;

  filteredData = baseData.filter(item => {
    const itemDate = new Date(item.timestamp);
    const itemDay = itemDate.toISOString().split('T')[0];
    const itemHour = itemDate.getHours();

    if (itemHour < 6 || itemHour > 18) return false;
    if (selectedDay && itemDay !== selectedDay) return false;
    if (selectedHour && itemHour !== parseInt(selectedHour)) return false;

    return true;
  });

  renderDataTable();
  updateStats();

  // Si estamos en vista de gráficos, actualiza las gráficas también
  if (isChartsViewActive()) {
    initializeCharts();
  }
}

function isChartsViewActive() {
  return !elements.chartsView.classList.contains('hidden');
}


function renderDataTable() {
    const data = filteredData.length > 0 ? filteredData : allData.filter(item => {
    const hour = new Date(item.timestamp).getHours();
    return hour >= 6 && hour <= 18;
    });

    elements.recordCount.textContent = `${data.length} registros`;

    if (data.length === 0) {
    elements.dataTable.innerHTML = '<div class="loading">No hay datos disponibles</div>';
    return;
    }

    const rows = data.map(item => `
    <div class="data-row">
        <div class="data-cell id">${item.id}</div>
        <div class="data-cell delta">${formatNumber(item.delta_value)}</div>
        <div class="data-cell accumulated">${formatNumber(item.accumulated_value)}</div>
        <div class="data-cell timestamp">${formatTimestamp(item.timestamp)}</div>
        <div class="data-cell">
        ${item.clasificacion ? `<span class="badge badge-${item.clasificacion.toLowerCase()}">${item.clasificacion}</span>` : ''}
        </div>
    </div>
    `).join('');

    elements.dataTable.innerHTML = rows;
}

function updateStats() {
    const workingData = allData.filter(item => {
    const hour = new Date(item.timestamp).getHours();
    return hour >= 6 && hour <= 18;
    });

    const validData = workingData.filter(item => item.clasificacion === 'valido');
    const totalRecords = workingData.length;
    const validRecords = validData.length;
    
    const avgDelta = totalRecords > 0 ? 
    workingData.reduce((sum, item) => sum + (item.delta_value || 0), 0) / totalRecords : 0;
    
    const lastAccumulated = workingData.length > 0 ? 
    workingData[workingData.length - 1].accumulated_value : 0;

    const timestamps = workingData.map(item => new Date(item.timestamp)).sort((a, b) => a - b);
    const firstTimestamp = timestamps[0];
    const lastTimestamp = timestamps[timestamps.length - 1];

    const uniqueDays = new Set(workingData.map(item => 
    new Date(item.timestamp).toISOString().split('T')[0]
    )).size;

    elements.totalRecords.textContent = totalRecords;
    elements.validRecords.textContent = validRecords;
    elements.avgDelta.textContent = formatNumber(avgDelta);
    elements.lastAccumulated.textContent = formatNumber(lastAccumulated);
    elements.firstRecord.textContent = firstTimestamp ? formatTimestamp(firstTimestamp) : '--';
    elements.lastRecord.textContent = lastTimestamp ? formatTimestamp(lastTimestamp) : '--';
    elements.daysWithData.textContent = uniqueDays;
}

function initializeCharts() {
    const workingData = filteredData.length > 0 ? filteredData : allData.filter(item => {
    const hour = new Date(item.timestamp).getHours();
    return hour >= 6 && hour <= 18;
    });

    // Gráfico de dispersión delta
    const deltaCtx = document.getElementById('delta-chart').getContext('2d');
    if (deltaChart) deltaChart.destroy();
    
    deltaChart = new Chart(deltaCtx, {
    type: 'scatter',
    data: {
        datasets: [{
        label: 'Delta Values',
        data: workingData.map((item, index) => ({
            x: index,
            y: item.delta_value || 0
        })),
        backgroundColor: 'rgba(59, 130, 246, 0.6)',
        borderColor: 'rgb(59, 130, 246)',
        pointRadius: 4
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
        legend: {
            display: false
        }
        },
        scales: {
        x: {
            title: {
            display: true,
            text: 'Registro'
            }
        },
        y: {
            title: {
            display: true,
            text: 'Delta'
            }
        }
        }
    }
    });

    // Gráfico de barras acumuladas
    const accCtx = document.getElementById('accumulated-chart').getContext('2d');
    if (accumulatedChart) accumulatedChart.destroy();
    
    accumulatedChart = new Chart(accCtx, {
    type: 'bar',
    data: {
        labels: workingData.map((item, index) => `#${index + 1}`),
        datasets: [{
        label: 'Valor Acumulado',
        data: workingData.map(item => item.accumulated_value || 0),
        backgroundColor: 'rgba(16, 185, 129, 0.6)',
        borderColor: 'rgb(16, 185, 129)',
        borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
        legend: {
            display: false
        }
        },
        scales: {
        y: {
            title: {
            display: true,
            text: 'Valor Acumulado'
            }
        }
        }
    }
    });
}

async function loadData() {
    try {
    const response = await fetch(`/api/audit_data?device_id=${DEVICE_ID}`);
    if (!response.ok) throw new Error('Error al cargar datos');
    
    allData = await response.json();
    
    setupFilters();
    filterData();
    
    } catch (error) {
    console.error('Error:', error);
    elements.dataTable.innerHTML = '<div class="loading">Error al cargar datos</div>';
    }
}

// Inicializar
document.addEventListener('DOMContentLoaded', loadData);

// ws-client.js
const socket = new WebSocket(`ws://${location.host}/ws/updates`);

// Icono flotante
const notif = document.createElement('div');
notif.id = 'notif-icon';
document.body.appendChild(notif);

socket.onmessage = ({ data }) => {
  const msg = JSON.parse(data);

  if (msg.type === 'new_record' && msg.device_id === DEVICE_ID) {
    // Solo recarga si es el mismo dispositivo
    loadData();  // vuelve a cargar todo (datos, filtros, stats y tablas)
  }

  else if (msg.type === 'alert') {
    const badge = document.createElement('div');
    badge.className = 'toast';
    badge.textContent = msg.message;
    notif.appendChild(badge);
    setTimeout(() => badge.remove(), 5000);
  }
};
