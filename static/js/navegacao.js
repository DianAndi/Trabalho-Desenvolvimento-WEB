document.addEventListener('DOMContentLoaded', () => {
    const mainContent = document.getElementById('main-content');
    
    const navButtons = document.querySelectorAll('nav button'); 
    
    const btnLojista = document.getElementById('btnLojista');

  
    async function loadPageContent(routeUrl) {
        try {
            const response = await fetch(routeUrl);
            if (!response.ok) {
                console.error(`HTTP error! Status: ${response.status} for ${routeUrl}`);
                mainContent.innerHTML = '<p>Erro ao carregar o conteúdo. Por favor, tente novamente.</p>';
                return;
            }
            const htmlContent = await response.text();

          
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = htmlContent;

            const newMainContent = tempDiv.querySelector('main'); 

            if (newMainContent) {
                
                mainContent.innerHTML = newMainContent.innerHTML; 
  
                mainContent.className = newMainContent.className; 
            } else {
               
                mainContent.innerHTML = htmlContent;
            }

          
            window.history.pushState({ path: routeUrl }, '', routeUrl);

            
            const scripts = mainContent.querySelectorAll('script');
            scripts.forEach(script => {
                const newScript = document.createElement('script');
                if (script.src) {
                    newScript.src = script.src;
                } else {
                    newScript.textContent = script.textContent;
                }
                document.body.appendChild(newScript);
                document.body.removeChild(newScript); // previnir duplicidade aqui
            });


        } catch (error) {
            console.error('Fetch error:', error);
            mainContent.innerHTML = '<p>Ocorreu um erro ao carregar a página.</p>';
        }
    }

   
    navButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            const route = event.target.dataset.route; // Flask route
            if (route) {
                loadPageContent(route);
            }
        });
    });

    // Handle the Lojista button (full page reload)
    if (btnLojista) {
        btnLojista.addEventListener('click', () => {
            // For the lojista page, we perform a full page reload as it's an authenticated area.
            window.location.href = "/lojista"; // Updated to Flask route
        });
    }

   

    window.addEventListener('popstate', (event) => {
        // Check if there's a state object with a 'path' (from pushState)
        if (event.state && event.state.path) {
            loadPageContent(event.state.path);
        } else {
            
            const initialPath = window.location.pathname === '/' ? '/' : window.location.pathname; 
            loadPageContent(initialPath);
        }
    });

   
    const initialLoadPath = window.location.pathname === '/' ? '/' : window.location.pathname;
    if (initialLoadPath !== '/') {
       
        loadPageContent(initialLoadPath);
    }
});
