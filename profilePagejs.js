function toggleEdit(showEdit) {
    var displaySection = document.getElementById('profileDisplay');
    var editSection = document.getElementById('profileEdit');
    if (showEdit) {
        displaySection.style.display = 'none';
        editSection.style.display = 'block';
    } else {
        displaySection.style.display = 'block';
        editSection.style.display = 'none';
    }
}
function showEditForm() {
    document.getElementById('profileDisplay').style.display = 'none';
    document.getElementById('profileEdit').style.display = 'block';
}

function hideEditForm() {
    document.getElementById('profileEdit').style.display = 'none';
    document.getElementById('profileDisplay').style.display = 'block';
}

function saveProfile() {
    // Example of saving form data to display elements
    document.getElementById('displayName').textContent = document.getElementById('fullName').value;
    document.getElementById('displayAddress1').textContent = document.getElementById('address1').value;
    document.getElementById('displayAddress2').textContent = document.getElementById('address2').value;
    document.getElementById('displayCity').textContent = document.getElementById('city').value;
    document.getElementById('displayState').textContent = document.getElementById('state').value;
    document.getElementById('displayZipcode').textContent = document.getElementById('zipcode').value;

    hideEditForm(); // Hide the form after saving
}