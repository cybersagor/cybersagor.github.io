// Change the title of the page
document.title = 'New Title of the Page';

// Change text content
document.getElementById('header').innerText = 'Welcome to the New Site';
document.getElementById('paragraph').innerText = 'This is a dynamically modified paragraph!';

// Change styles
document.getElementById('header').style.color = 'blue';
document.getElementById('header').style.fontSize = '40px';

// Change an image source
document.getElementById('logo').src = 'new-logo.png';

// Add a new element
const newDiv = document.createElement('div');
newDiv.innerHTML = '<h2>This is a new section!</h2><p>Added dynamically with JavaScript.</p>';
document.body.appendChild(newDiv);

// Remove an element
const elementToRemove = document.getElementById('footer');
elementToRemove.remove();
