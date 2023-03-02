// Modal window
document.addEventListener('DOMContentLoaded', function () {
    // Your code here
    const modal = document.querySelector(".making-appointment");

// Get the button that opens the modal
    const openModal = document.querySelector(".make-appointment");

// Get the <button> element that closes the modal
    const cancelBtn = document.querySelector('.close-appointment');

// When the user clicks on the button, open the modal
    if (openModal !== null) {
        openModal.addEventListener('click', function () {
            modal.classList.toggle('open-modal');
        });
    }

// When the user clicks on Cancel, close the modal
    cancelBtn.addEventListener('click', function () {
        modal.classList.toggle('open-modal');
    });

// // When the user clicks anywhere outside of the modal, close it
//     window.onclick = function (event) {
//         if (event.target === modal) {
//             modal.classList.toggle('open-modal');
//         }
//     }
});


// for appointment(modal)
function clearSelect() {
    var select = document.getElementById('doctor_id');
    select.innerHTML = '';
}