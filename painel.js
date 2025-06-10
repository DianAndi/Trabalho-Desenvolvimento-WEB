<script>
  document.getElementById('uploadForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const titulo = document.getElementById('titulo').value;
    const descricao = document.getElementById('descricao').value;
    const categoria = document.getElementById('categoria').value;
    const linha = document.getElementById('linha').value;
    const imagem = document.getElementById('imagem').files[0];

    if (!titulo || !descricao || !categoria || !linha || !imagem) {
      alert('Preencha todos os campos obrigatórios.');
      return;
    }

    const formData = new FormData();
    formData.append('titulo', titulo);
    formData.append('descricao', descricao);
    formData.append('categoria', categoria);
    formData.append('linha', linha);
    formData.append('imagem', imagem);

    try {
      const response = await fetch('http://localhost:8000/api/produtos', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        throw new Error('Erro ao cadastrar o produto.');
      }

      const produto = await response.json();

      //galeria
      const galeria = document.getElementById('galeria');
      const item = document.createElement('div');
      item.className = 'item';
      item.innerHTML = `
        <img src="${produto.imagem_url}" alt="${produto.titulo}" />
        <p><strong>${produto.titulo}</strong></p>
        <p>${produto.descricao}</p>
        <p><em>${produto.categoria}</em> - ${produto.linha}</p>
      `;
      galeria.appendChild(item);

      // Limpa o form
      document.getElementById('uploadForm').reset();

    } catch (error) {
      console.error(error);
      alert('Erro ao enviar os dados.');
    }
  });
</script>
