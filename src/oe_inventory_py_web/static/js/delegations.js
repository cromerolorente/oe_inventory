// Form logic for the Delegations screen (frmDelegations.html).

function currentCode() {
    return document.getElementById('input-code').value.trim();
}

function syncCode() {
    document.getElementById('input-code-hidden').value = currentCode();
}

function buscarDelegacionAjax() {
    const code = currentCode();
    if (!code) return;
    fetch(`/api/get-delegation/?id=${encodeURIComponent(code)}`)
        .then(r => r.json())
        .then(res => {
            if (!res.success) return;
            if (res.exists) {
                fillDelegation(res.data);
            } else {
                limpiarDelegacion();
                document.getElementById('input-code').value = code;
                Swal.fire({ title: 'OE Inventory', text: 'Delegation not found. Fill the fields and Save to create it.', icon: 'info', confirmButtonColor: '#FF48D8' });
            }
        })
        .catch(err => console.error('Error fetching delegation:', err));
}

function fillDelegation(d) {
    document.getElementById('input-code').value = d.id;
    document.getElementById('input-delegation').value = d.delegation || '';
    document.getElementById('input-direccion').value = d.direccion || '';
    document.getElementById('input-cpostal').value = d.cpostal || '';
    document.getElementById('input-poblacion').value = d.poblacion || '';
    document.getElementById('input-provincia').value = d.provincia || '';
    document.getElementById('textarea-notes').value = d.notes || '';
    syncCode();
}

function limpiarDelegacion() {
    document.getElementById('form-delegation').reset();
    document.getElementById('input-code').value = '';
    document.getElementById('textarea-notes').value = '';
    syncCode();
    document.querySelectorAll('.delegation-row').forEach(r => r.classList.remove('table-primary'));
}

function setDelegationAction(action) {
    document.querySelector('#form-delegation input[name="action"]').value = action;
}

function guardarDelegacion() {
    if (!document.getElementById('input-delegation').value.trim()) {
        Swal.fire({ title: 'OE Inventory', text: 'The Delegation field is required.', icon: 'error', confirmButtonColor: '#FF48D8' });
        return;
    }
    syncCode();
    setDelegationAction('save');
    document.getElementById('form-delegation').submit();
}

function geolocalizarDelegacion() {
    if (!currentCode()) {
        Swal.fire({ title: 'OE Inventory', text: 'Load and save a delegation first, then geolocate it.', icon: 'info', confirmButtonColor: '#FF48D8' });
        return;
    }
    syncCode();
    setDelegationAction('geocode');
    document.getElementById('form-delegation').submit();
}

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('tabla-delegaciones').addEventListener('click', function (e) {
        const row = e.target.closest('tr.delegation-row');
        if (!row) return;
        document.querySelectorAll('.delegation-row').forEach(r => r.classList.remove('table-primary'));
        row.classList.add('table-primary');
        document.getElementById('input-code').value = row.dataset.id;
        buscarDelegacionAjax();
    });

    if (window.jQuery && jQuery.fn.DataTable) {
        jQuery('#tabla-delegaciones').DataTable({ pageLength: 25, ordering: true, autoWidth: false });
    }

    const pre = document.getElementById('preselected-delegation').value;
    if (pre) {
        document.getElementById('input-code').value = pre;
        buscarDelegacionAjax();
    }

    initDelegationsMap();
});

// Leaflet map of Spain with a pin per geocoded delegation.
function initDelegationsMap() {
    const mapEl = document.getElementById('delegations-map');
    if (!mapEl || typeof L === 'undefined') return;

    let points = [];
    const dataEl = document.getElementById('delegations-map-data');
    if (dataEl) {
        try { points = JSON.parse(dataEl.textContent) || []; } catch (e) { points = []; }
    }

    // Center on Spain by default.
    const map = L.map('delegations-map').setView([40.0, -3.7], 6);
    // CARTO Positron basemap: free, no API key, and suitable for app use.
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        maxZoom: 20,
        subdomains: 'abcd',
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
    }).addTo(map);

    // Blue pin for active delegations (activo=1), red for inactive (activo=0).
    const blueIcon = delegationPinIcon('#2A81CB');
    const redIcon = delegationPinIcon('#CB2B3E');

    const markers = [];
    points.forEach(p => {
        if (p.lat == null || p.lng == null) return;
        const icon = (Number(p.activo) === 0) ? redIcon : blueIcon;
        const m = L.marker([p.lat, p.lng], { icon: icon }).addTo(map);
        const addr = p.address ? `<br><span class="text-muted">${p.address}</span>` : '';
        const status = (Number(p.activo) === 0) ? '<br><span style="color:#CB2B3E;">Inactive</span>' : '';
        m.bindPopup(`<strong>${p.name || ''}</strong>${addr}${status}`);
        markers.push(m);
    });

    // Fit the view to the pins (if any).
    if (markers.length === 1) {
        map.setView(markers[0].getLatLng(), 13);
    } else if (markers.length > 1) {
        map.fitBounds(L.featureGroup(markers).getBounds().pad(0.2));
    }

    // Leaflet needs a size recalculation once the container is fully laid out.
    setTimeout(() => map.invalidateSize(), 200);
}

// Build a colored pin marker as an inline SVG (no external image assets needed).
function delegationPinIcon(color) {
    const svg = `<svg width="25" height="41" viewBox="0 0 25 41" xmlns="http://www.w3.org/2000/svg">
        <path d="M12.5 0C5.6 0 0 5.6 0 12.5 0 21.9 12.5 41 12.5 41S25 21.9 25 12.5C25 5.6 19.4 0 12.5 0z"
              fill="${color}" stroke="#ffffff" stroke-width="1.5"/>
        <circle cx="12.5" cy="12.5" r="4.5" fill="#ffffff"/>
    </svg>`;
    return L.divIcon({
        className: 'delegation-pin',
        html: svg,
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [0, -36],
    });
}
