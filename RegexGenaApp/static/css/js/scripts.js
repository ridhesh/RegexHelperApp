// scripts.js

document.addEventListener("DOMContentLoaded", function() {
    // Example: Alert when a link is clicked
    const links = document.querySelectorAll('a');
    links.forEach(link => {
        link.addEventListener('click', function(event) {
            alert('You are about to visit: ' + this.href);
        });
    });
 });