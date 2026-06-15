// Wait for the HTML to fully load before running the script
document.addEventListener('DOMContentLoaded', function() {
    
    // 1. Dynamic greeting based on time of day
    const greetingElement = document.createElement('p');
    const currentHour = new Date().getHours();
    let greeting;
    
    if (currentHour < 12) {
        greeting = "🌅 Good morning!";
    } else if (currentHour < 18) {
        greeting = "☀️ Good afternoon!";
    } else {
        greeting = "🌙 Good evening!";
    }
    
    greetingElement.textContent = greeting;
    greetingElement.style.fontWeight = "bold";
    greetingElement.style.fontSize = "18px";
    greetingElement.style.margin = "20px";
    
    // Insert greeting after the introduction
    const introductionDiv = document.querySelector('.introduction');
    if (introductionDiv) {
        introductionDiv.insertAdjacentElement('afterend', greetingElement);
    }
    
    // 2. Add hover effects to social links with animation
    const links = document.querySelectorAll('a');
    links.forEach(link => {
        link.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.1)';
            this.style.transition = 'transform 0.3s ease';
            this.style.display = 'inline-block';
        });
        
        link.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
        
        // Add click confirmation for external links
        link.addEventListener('click', function(e) {
            const confirmed = confirm(`You're about to visit ${this.textContent}. Continue?`);
            if (!confirmed) {
                e.preventDefault();
            }
        });
    });
    
    // 3. Add a "Last Updated" timestamp
    const lastUpdated = document.createElement('p');
    const lastModified = new Date(document.lastModified);
    lastUpdated.textContent = `📅 Last updated: ${lastModified.toLocaleDateString()} at ${lastModified.toLocaleTimeString()}`;
    lastUpdated.style.fontSize = "12px";
    lastUpdated.style.textAlign = "center";
    lastUpdated.style.marginTop = "40px";
    lastUpdated.style.opacity = "0.7";
    document.body.appendChild(lastUpdated);
    
    // 4. Add a "Back to Top" button that appears when scrolling
    const backToTopBtn = document.createElement('button');
    backToTopBtn.textContent = '↑ Back to Top';
    backToTopBtn.style.position = 'fixed';
    backToTopBtn.style.bottom = '20px';
    backToTopBtn.style.right = '20px';
    backToTopBtn.style.padding = '10px 15px';
    backToTopBtn.style.backgroundColor = '#b4ff33';
    backToTopBtn.style.color = '#333';
    backToTopBtn.style.border = 'none';
    backToTopBtn.style.borderRadius = '5px';
    backToTopBtn.style.cursor = 'pointer';
    backToTopBtn.style.display = 'none';
    backToTopBtn.style.zIndex = '1000';
    backToTopBtn.style.fontWeight = 'bold';
    
    document.body.appendChild(backToTopBtn);
    
    // Show/hide back to top button based on scroll position
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopBtn.style.display = 'block';
        } else {
            backToTopBtn.style.display = 'none';
        }
    });
    
    // Scroll to top when button is clicked
    backToTopBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    // 5. Add a subtle typing effect to the main heading
    const mainHeading = document.querySelector('h1');
    if (mainHeading) {
        const originalText = mainHeading.textContent;
        mainHeading.textContent = '';
        let i = 0;
        
        function typeWriter() {
            if (i < originalText.length) {
                mainHeading.textContent += originalText.charAt(i);
                i++;
                setTimeout(typeWriter, 100);
            }
        }
        
        // Start typing effect when page loads
        typeWriter();
    }
    
    // 6. Add a click counter for fun
    let clickCount = 0;
    const profileSection = document.querySelector('.profile');
    
    if (profileSection) {
        profileSection.addEventListener('click', function(e) {
            // Don't count clicks on links
            if (e.target.tagName !== 'A') {
                clickCount++;
                
                // Create temporary message
                const clickMessage = document.createElement('div');
                clickMessage.textContent = `👆 You've clicked this section ${clickCount} time${clickCount !== 1 ? 's' : ''}!`;
                clickMessage.style.position = 'fixed';
                clickMessage.style.bottom = '80px';
                clickMessage.style.right = '20px';
                clickMessage.style.backgroundColor = '#333';
                clickMessage.style.color = '#b4ff33';
                clickMessage.style.padding = '10px';
                clickMessage.style.borderRadius = '5px';
                clickMessage.style.fontSize = '12px';
                clickMessage.style.zIndex = '1000';
                
                document.body.appendChild(clickMessage);
                
                // Remove message after 2 seconds
                setTimeout(() => {
                    clickMessage.remove();
                }, 2000);
            }
        });
    }
    
    // 7. Console message for developers
    console.log('%c🚀 Welcome to Mohammed Sayed\'s Portfolio Website!', 'color: #b4ff33; font-size: 16px; font-weight: bold;');
    console.log('%cFeel free to explore the code!', 'color: #ffffff; font-size: 12px;');
    
});