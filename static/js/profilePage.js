
document.addEventListener('DOMContentLoaded', function() {
    fetchAndDisplayProfile();
});

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
    const userId = getCurrentUserId();
    const profileData = {
        fullName: document.getElementById('fullName').value,
        address1: document.getElementById('address1').value,
        address2: document.getElementById('address2').value,
        city: document.getElementById('city').value,
        state: document.getElementById('state').value,
        zipcode: document.getElementById('zipcode').value,
    };
    const url = `http://localhost:5000/profile/${userId}`;

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(profileData),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        // Handle success, such as updating UI or showing a success message
    })
    .catch(error => {
        console.error('Error:', error);
        // Handle error, such as showing an error message to the user
    }); //store this in a text file

    // document.getElementById('displayName').textContent = document.getElementById('fullName').value;
    // document.getElementById('displayAddress1').textContent = document.getElementById('address1').value;
    // document.getElementById('displayAddress2').textContent = document.getElementById('address2').value;
    // document.getElementById('displayCity').textContent = document.getElementById('city').value;
    // document.getElementById('displayState').textContent = document.getElementById('state').value;
    // document.getElementById('displayZipcode').textContent = document.getElementById('zipcode').value;

    // hideEditForm(); // Hide the form after saving
}

function fetchAndDisplayProfile() {
    const userId = getCurrentUserId(); // Assume this function gets the current user's ID
    const url = `http://localhost:5000/profile/${userId}`;

    fetch(url)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Profile Data:', data);
        // Update the UI elements with the fetched profile data
        document.getElementById('displayName').textContent = data.fullName || '';
        document.getElementById('displayAddress1').textContent = data.address1 || '';
        document.getElementById('displayAddress2').textContent = data.address2 || '';
        document.getElementById('displayCity').textContent = data.city || '';
        document.getElementById('displayState').textContent = data.state || '';
        document.getElementById('displayZipcode').textContent = data.zipcode || '';
    })
    .catch(error => {
        console.error('Error:', error);
        // Handle error, such as displaying a message to the user
    });
}

function getCurrentUserId() {
    return 1; // Or return null if creating a new profile
    // will implement code of getting the logged-in user session id when implementing database.
    // for right now, just return hardcoded id
}