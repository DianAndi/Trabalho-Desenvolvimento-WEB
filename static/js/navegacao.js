document.addEventListener('DOMContentLoaded', () => {

    const mainContent = document.getElementById('main-content');

    const navButtons = document.querySelectorAll('nav button, [data-route]');


    const btnLojista = document.getElementById('btnLojista');

  
    async function loadPageContent(partialUrl, isInitialLoad = false) {
        try {
            const response = await fetch(partialUrl);
            if (!response.ok) {
                console.error(`HTTP error! Status: ${response.status} for ${partialUrl}`);
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
            
                window.scrollTo(0, 0);

              
                const scripts = newMainContent.querySelectorAll('script');
                scripts.forEach(oldScript => {
                    const newScript = document.createElement('script');
                    // Copia todos os atributos (como 'defer')
                    Array.from(oldScript.attributes).forEach(attr => newScript.setAttribute(attr.name, attr.value));
                    newScript.textContent = oldScript.textContent;
                    mainContent.appendChild(newScript);
                });

                
                const visibleUrl = partialUrl.replace('_partial', '');
                if (!isInitialLoad) {
                    window.history.pushState({ path: partialUrl }, '', visibleUrl);
                }

            } else {
                console.warn('Tag <main> não encontrada no conteúdo parcial:', partialUrl);
                mainContent.innerHTML = '<p>Conteúdo da página não pôde ser processado corretamente.</p>';
            }

        } catch (error) {
            console.error('Erro ao carregar o conteúdo da página:', error);
            mainContent.innerHTML = '<p>Ocorreu um erro ao carregar a página. Tente novamente mais tarde.</p>';
        }
    }

    // Event listeners para os botões de navegação SPA
    navButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault(); // Impede o comportamento padrão do botão/link
            const partialRoute = event.target.dataset.route; // Pega a URL da rota parcial do atributo data-route
            if (partialRoute) {
                loadPageContent(partialRoute);
            }
        });
    });

   
    if (btnLojista) {
        btnLojista.addEventListener('click', () => {
           
            window.location.href = btnLojista.dataset.route;
        });
    }

   
    window.addEventListener('popstate', (event) => {
       
        if (event.state && event.state.path) {
            loadPageContent(event.state.path);
        } else {
            
            const currentPathname = window.location.pathname; 
            let partialLoadUrl;

            if (currentPathname === '/') {
                partialLoadUrl = '{{ url_for("index_partial") }}';
            } else {
    
                partialLoadUrl = currentPathname + '_partial';
            }
            loadPageContent(partialLoadUrl);
        }
    });

    
    const initialPathname = window.location.pathname;
    let initialLoadUrl;

    if (initialPathname === '/') {
        initialLoadUrl = '{{ url_for("index_partial") }}';
    } else {
        
        initialLoadUrl = initialPathname + '_partial';
    }
    loadPageContent(initialLoadUrl, true);
});
