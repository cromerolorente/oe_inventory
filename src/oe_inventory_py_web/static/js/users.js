// Form logic for the Users screen (frmUser.html).

function desactivarFormulario() {
    document.getElementById('input-is-new').value = "0";
    document.getElementById('input-nombre').value = "";
    document.getElementById('input-email').value = "";
    document.getElementById('input-password').value = "";
    document.getElementById('textarea-notes').value = "";

    document.getElementById('input-nombre').disabled = true;
    document.getElementById('input-email').disabled = true;
    document.getElementById('input-password').disabled = true;

    // Turn off all permission checkboxes.
    document.querySelectorAll('.chk-permiso').forEach(chk => {
        chk.checked = false;
        chk.disabled = true;
    });

    // Clear and disable the grid checkboxes.
    document.querySelectorAll('.grid-chk').forEach(chk => {
        chk.checked = false;
        chk.disabled = true;
    });

    document.getElementById('btn-save').disabled = true;
    document.getElementById('btn-clear').disabled = true;
}

function activarFormulario() {
    document.getElementById('input-nombre').disabled = false;
    document.getElementById('input-email').disabled = false;

    document.querySelectorAll('.chk-permiso').forEach(chk => chk.disabled = false);
    document.querySelectorAll('.grid-chk').forEach(chk => chk.disabled = false);

    document.getElementById('btn-save').disabled = false;
    document.getElementById('btn-clear').disabled = false;
}

// Password is editable only for new users or accounts without a usable password.
// For accounts that already have one, it stays masked and locked (changed via
// 'Password Change' or the 'Forgot my password' email flow).
function setPasswordEditable(editable) {
    const pw = document.getElementById('input-password');
    if (editable) {
        pw.value = '';
        pw.disabled = false;
        pw.readOnly = false;
    } else {
        pw.value = '********';
        pw.disabled = true;
        pw.readOnly = true;
    }
}

function buscarUsuarioAjax() {
    const loginInput = document.getElementById('input-login');
    if (!loginInput || !loginInput.value.trim()) return;
    const login = loginInput.value.trim();

    desactivarFormulario();

    fetch(`/api/get-user/?login=${encodeURIComponent(login)}`)
        .then(res => res.json())
        .then(res => {
            if (res.success) {
                activarFormulario();
                if (res.exists) {
                    // UPDATE MODE
                    document.getElementById('input-is-new').value = "0";
                    const user = res.data;

                    document.getElementById('input-nombre').value = user.nombre || '';
                    document.getElementById('input-email').value = user.email || '';
                    setPasswordEditable(!user.has_password);  // editable only if no password yet
                    document.getElementById('textarea-notes').value = user.notes || '';

                    // Dynamically set the permission checkboxes.
                    document.querySelectorAll('.chk-permiso').forEach(chk => {
                        const fieldName = chk.id.replace('permiso-', '');
                        chk.checked = (user[fieldName] === 1 || user[fieldName] === true);
                    });

                    // Check the grid rows by parsing the comma-separated strings.
                    marcarCheckboxesGrid('companies_selected', user.companies);
                    marcarCheckboxesGrid('delegations_selected', user.delegations);
                    marcarCheckboxesGrid('departments_selected', user.departments);
                } else {
                    // NEW USER MODE (INSERT)
                    if (confirm(`User [${res.login}] does not exist. Do you want to create a new user?`)) {
                        document.getElementById('input-is-new').value = "1";
                        setPasswordEditable(true);  // new user: allow setting an initial password
                        document.getElementById('input-nombre').focus();
                    } else {
                        loginInput.value = "";
                        desactivarFormulario();
                    }
                }
            }
        })
        .catch(err => console.error("Error fetching user data:", err));
}

function marcarCheckboxesGrid(nameAttr, listStr) {
    if (!listStr) return;
    const targetElements = listStr.split(',').map(el => el.trim());
    document.querySelectorAll(`input[name="${nameAttr}"]`).forEach(chk => {
        const val = chk.getAttribute('data-raw').toString();
        if (targetElements.includes(val)) {
            chk.checked = true;
        }
    });
}
