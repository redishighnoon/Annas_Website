// Defines a function named toggleFeedbackForm. This function is responsible for toggling
// the visibility of the feedback form on the webpage.
function toggleFeedbackForm() {
    // Attempts to find an element with 
    var form = document.getElementById('feedbackForm');
    
    // Checks if the form variable is not null (i.e. the element with the ID 'feedbackForm' exists).
    if (form) {
        // Toggles the visibility of the form element. If the form is currently hidden, it will be shown.
        form.style.display = form.style.display === 'none' ? 'block' : 'none';
    }
}
