// Generic finder modal controller, shared by the forms that include finder_modal.html.
// Becomes globally available (window.FrmFinder) as soon as this script loads.
const FrmFinder = {
  targetInputId: null,
  callbackFunctionName: null,
  searchField: 'device_name',
  option: null,

  open: function (targetInputId, callbackFunctionName, field = 'device_name', option = null) {
    this.targetInputId = targetInputId;
    this.callbackFunctionName = callbackFunctionName;
    this.searchField = field;
    this.option = option;

    document.getElementById('finderSearchInput').value = '';
    document.getElementById('finderResultsBody').innerHTML = '<tr><td colspan="2" class="text-center text-muted">Press SEARCH button to load data.</td></tr>';

    const modal = new bootstrap.Modal(document.getElementById('finderModal'));
    modal.show();

    document.getElementById('finderModal').addEventListener('shown.bs.modal', function () {
      document.getElementById('finderSearchInput').focus();
    }, { once: true });
  },

  loadData: function () {
    const term = document.getElementById('finderSearchInput').value;
    const url = `/api/finder/?term=${encodeURIComponent(term)}&field=${this.searchField}&option=${this.option || ''}`;

    fetch(url)
      .then(response => response.json())
      .then(response => {
        const tbody = document.getElementById('finderResultsBody');
        tbody.innerHTML = '';

        if (response.data && response.data.length > 0) {
          response.data.forEach(item => {
            const row = document.createElement('tr');
            row.style.cursor = 'pointer';
            row.innerHTML = `<td><strong>${item.code}</strong></td><td>${item.description}</td>`;

            row.addEventListener('dblclick', () => {
              this.selectItem(item.code);
            });

            tbody.appendChild(row);
          });
        } else {
          tbody.innerHTML = '<tr><td colspan="2" class="text-center text-danger">No data found with the specified criteria.</td></tr>';
        }
      })
      .catch(error => console.error('Error fetching finder data:', error));
  },

  selectItem: function (code) {
    const targetInput = document.getElementById(this.targetInputId);
    if (targetInput) {
      targetInput.value = code;
    }

    const modalElement = document.getElementById('finderModal');
    const modal = bootstrap.Modal.getInstance(modalElement);
    if (modal) modal.hide();

    // Automatically runs the parent form's callback (e.g. buscarDispositivoAjax()).
    if (this.callbackFunctionName && typeof window[this.callbackFunctionName] === 'function') {
      window[this.callbackFunctionName]();
    }
  }
};

document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('btnFinderSearch').addEventListener('click', () => FrmFinder.loadData());
  document.getElementById('finderSearchInput').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') FrmFinder.loadData();
  });
});
