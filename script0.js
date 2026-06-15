// Simple JavaScript for beginners

// 1. Change background color when clicking a button
function changeColor() {
    const colors = ['#ef9191', '#6c91b2', '#6cb27c', '#b27a6c', '#a86cb2'];
    const randomColor = colors[Math.floor(Math.random() * colors.length)];
    document.body.style.backgroundColor = randomColor;
}

// Create a color change button
const colorButton = document.createElement('button');
colorButton.textContent = 'Change Background Color';
colorButton.style.display = 'block';
colorButton.style.margin = '20px auto';
colorButton.style.padding = '10px 20px';
colorButton.style.backgroundColor = '#b4ff33';
colorButton.style.border = 'none';
colorButton.style.borderRadius = '5px';
colorButton.style.cursor = 'pointer';
colorButton.onclick = changeColor;

// Add button to the page
document.body.appendChild(colorButton);

// 2. Show an alert when clicking on social links
const allLinks = document.querySelectorAll('a');

for (let i = 0; i < allLinks.length; i++) {
    allLinks[i].onclick = function() {
        alert('You are leaving this website to visit: ' + this.textContent);
    };
}

// 3. Display current date and time
const dateParagraph = document.createElement('p');
const now = new Date();
const dateString = now.toLocaleDateString() + ' - ' + now.toLocaleTimeString();
dateParagraph.textContent = '📅 Current Date & Time: ' + dateString;
dateParagraph.style.textAlign = 'center';
dateParagraph.style.marginTop = '30px';
dateParagraph.style.fontSize = '14px';
document.body.appendChild(dateParagraph);

// 4. Simple welcome message in console
console.log('Welcome to Mohammed\'s website!');