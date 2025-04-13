/*
  --------------------------------------------------------------------------------------
  Função para obter a lista existente do servidor via requisição GET
  --------------------------------------------------------------------------------------
*/
const getList = async () => {
  let url = 'http://127.0.0.1:5000/produtos';
  fetch(url, {
    method: 'get',
  })
    .then((response) => response.json())
    .then((data) => {
      data.produtos.forEach(item => insertList(item.nome, item.quantidade, item.valor))
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  --------------------------------------------------------------------------------------
  Chamada da função para carregamento inicial dos dados
  --------------------------------------------------------------------------------------
*/
getList()


/*
  --------------------------------------------------------------------------------------
  Função para colocar um item na lista do servidor via requisição POST
  --------------------------------------------------------------------------------------
*/
const postItem = async (inputProduct, inputQuantity, inputPrice) => {
  const formData = new FormData();
  formData.append('nome', inputProduct);
  formData.append('quantidade', inputQuantity);
  formData.append('valor', inputPrice);

  let url = 'http://127.0.0.1:5000/produto';
  fetch(url, {
    method: 'post',
    body: formData
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}


/*
  --------------------------------------------------------------------------------------
  Função para criar um botão close para cada item da lista
  --------------------------------------------------------------------------------------
*/
const insertButton = (parent) => {
  let span = document.createElement("span");
  let txt = document.createTextNode("\u00D7");
  span.className = "close";
  span.appendChild(txt);
  parent.appendChild(span);
}


/*
  --------------------------------------------------------------------------------------
  Função para remover um item da lista de acordo com o click no botão close
  --------------------------------------------------------------------------------------
*/
const removeElement = () => {
  let close = document.getElementsByClassName("close");
  // var table = document.getElementById('myTable');
  let i;
  for (i = 0; i < close.length; i++) {
    close[i].onclick = function () {
      let div = this.parentElement.parentElement;
      const nomeItem = div.getElementsByTagName('td')[0].innerHTML
      if (confirm("Você tem certeza?")) {
        div.remove()
        deleteItem(nomeItem)
        alert("Removido!")
      }
    }
  }
}

/*
  --------------------------------------------------------------------------------------
  Função para deletar um item da lista do servidor via requisição DELETE
  --------------------------------------------------------------------------------------
*/
const deleteItem = (item) => {
  console.log(item)
  let url = 'http://127.0.0.1:5000/produto?nome=' + item;
  fetch(url, {
    method: 'delete'
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  --------------------------------------------------------------------------------------
  Função para adicionar um novo item com nome, quantidade e valor 
  --------------------------------------------------------------------------------------
*/
const newItem = () => {
  let inputProduct = document.getElementById("newInput").value;
  let inputQuantity = document.getElementById("newQuantity").value;
  let inputPrice = document.getElementById("newPrice").value;

  if (inputProduct === '') {
    alert("Escreva o nome de um item!");
  } else if (isNaN(inputQuantity) || isNaN(inputPrice)) {
    alert("Quantidade e valor precisam ser números!");
  } else {
    insertList(inputProduct, inputQuantity, inputPrice)
    postItem(inputProduct, inputQuantity, inputPrice)
    alert("Item adicionado!")
  }
}

/*
  --------------------------------------------------------------------------------------
  Função para inserir items na lista apresentada
  --------------------------------------------------------------------------------------
*/
const insertList = (nameProduct, quantity, price) => {
  var item = [nameProduct, quantity, price]
  var table = document.getElementById('myTable');
  var row = table.insertRow();

  for (var i = 0; i < item.length; i++) {
    var cel = row.insertCell(i);
    cel.textContent = item[i];
  }
  insertButton(row.insertCell(-1))
  document.getElementById("newInput").value = "";
  document.getElementById("newQuantity").value = "";
  document.getElementById("newPrice").value = "";

  removeElement()
}

// Portfolio data structure
let portfolio = [];

// DOM Elements
const stockForm = document.getElementById('stockForm');
const portfolioTable = document.getElementById('portfolioTable');
const totalAssetsElement = document.getElementById('totalAssets');
const totalStocksElement = document.getElementById('totalStocks');

// Event Listeners
stockForm.addEventListener('submit', handleAddStock);

// Functions
function handleAddStock(e) {
    e.preventDefault();
    
    const symbol = document.getElementById('symbol').value.toUpperCase();
    const quantity = parseInt(document.getElementById('quantity').value);
    const price = parseFloat(document.getElementById('price').value);
    
    // Check if stock already exists
    const existingStockIndex = portfolio.findIndex(stock => stock.symbol === symbol);
    
    if (existingStockIndex !== -1) {
        // Update existing stock
        portfolio[existingStockIndex] = {
            symbol,
            quantity,
            price,
            totalValue: quantity * price
        };
    } else {
        // Add new stock
        portfolio.push({
            symbol,
            quantity,
            price,
            totalValue: quantity * price
        });
    }
    
    updatePortfolioDisplay();
    stockForm.reset();
}

function updatePortfolioDisplay() {
    // Clear table
    portfolioTable.innerHTML = '';
    
    // Calculate totals
    const totalAssets = portfolio.reduce((sum, stock) => sum + stock.totalValue, 0);
    const totalStocks = portfolio.length;
    
    // Update summary
    totalAssetsElement.textContent = `$${totalAssets.toFixed(2)}`;
    totalStocksElement.textContent = totalStocks;
    
    // Add stocks to table
    portfolio.forEach((stock, index) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${stock.symbol}</td>
            <td>${stock.quantity}</td>
            <td>$${stock.price.toFixed(2)}</td>
            <td>$${stock.totalValue.toFixed(2)}</td>
            <td class="action-buttons">
                <button class="btn btn-sm btn-primary" onclick="editStock(${index})">
                    <i class="bi bi-pencil"></i>
                </button>
                <button class="btn btn-sm btn-danger" onclick="removeStock(${index})">
                    <i class="bi bi-trash"></i>
                </button>
            </td>
        `;
        portfolioTable.appendChild(row);
    });
}

function removeStock(index) {
    if (confirm('Are you sure you want to remove this stock?')) {
        portfolio.splice(index, 1);
        updatePortfolioDisplay();
    }
}

function editStock(index) {
    const stock = portfolio[index];
    document.getElementById('symbol').value = stock.symbol;
    document.getElementById('quantity').value = stock.quantity;
    document.getElementById('price').value = stock.price;
    
    // Remove the stock being edited
    portfolio.splice(index, 1);
    updatePortfolioDisplay();
}

// Initialize display
updatePortfolioDisplay();