// Clean portfolio interactions
document.addEventListener('DOMContentLoaded', function() {
    
    // 1. Dynamic greeting based on time of day
    const greetingElement = document.createElement('div');
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
    greetingElement.style.fontSize = "16px";
    greetingElement.style.margin = "20px 0";
    greetingElement.style.color = "#666";
    
    // Insert greeting after the introduction
    const mainContent = document.querySelector('.main-content');
    if (mainContent) {
        mainContent.insertBefore(greetingElement, mainContent.firstChild);
    }
    
    // 2. Add hover effects to social links (without scale transform)
    const links = document.querySelectorAll('.social-link');
    links.forEach(link => {
        link.addEventListener('mouseenter', function() {
            this.style.color = '#000';
        });
        
        link.addEventListener('mouseleave', function() {
            this.style.color = '#555';
        });
        
        // Simple tracking without annoying confirm
        link.addEventListener('click', function(e) {
            console.log(`📤 Clicked: ${this.textContent}`);
        });
    });
    
    // 3. Add a "Back to Top" button
    const backToTopBtn = document.createElement('button');
    backToTopBtn.id = 'backToTop';
    backToTopBtn.textContent = '↑ Back to Top';
    document.body.appendChild(backToTopBtn);
    
    // Show/hide back to top button
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopBtn.style.display = 'block';
        } else {
            backToTopBtn.style.display = 'none';
        }
    });
    
    backToTopBtn.addEventListener('click', function() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
    
    // 4. Remove typing effect (can be annoying, but kept simple)
    // Just ensure heading is visible
    const mainHeading = document.querySelector('h1');
    if (mainHeading && !mainHeading.textContent) {
        mainHeading.textContent = 'Mohammed Sayed';
    }
    
    // 5. Simple click counter (fun, but not intrusive)
    let clickCount = 0;
    const mainContent = document.querySelector('.main-content');
    
    if (mainContent) {
        mainContent.addEventListener('click', function(e) {
            if (e.target.tagName !== 'A' && e.target.tagName !== 'BUTTON') {
                clickCount++;
                
                const clickMessage = document.createElement('div');
                clickMessage.className = 'click-message';
                clickMessage.textContent = `👆 Click ${clickCount}`;
                document.body.appendChild(clickMessage);
                
                setTimeout(() => clickMessage.remove(), 1500);
            }
        });
    }
    
    // 6. Track tool clicks
    const toolLinks = document.querySelectorAll('.tool-link');
    toolLinks.forEach(link => {
        link.addEventListener('click', function() {
            console.log(`🛠️ Tool launched: ${this.textContent}`);
        });
    });
    
    // 7. Console message
    console.log('%c🚀 Mohammed Sayed - Full Stack Developer Portfolio', 'color: #0066cc; font-size: 14px; font-weight: bold;');
    console.log('%cView source on GitHub: https://github.com/mos238/myWebSite', 'color: #666; font-size: 12px;');
    
});
