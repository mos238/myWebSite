// SUPER SIMPLE - Just shows an alert when page loads
alert('Welcome to my website!');

// Changes heading color when you click on it
const heading = document.querySelector('h1');

heading.onclick = function() {
    heading.style.color = '#ff5733';
    heading.style.fontSize = '40px';
};