<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Currency Converter</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 text-gray-900 flex flex-col items-center p-6">

  <h1 class="text-2xl font-bold mb-6">Currency Converter</h1>

  <!-- Conversor principal -->
  <div class="bg-white shadow-md rounded-2xl p-6 w-full max-w-2xl">
    <div class="grid grid-cols-2 gap-4">
      
      <!-- From -->
      <div>
        <label for="fromCurrency" class="block text-sm font-medium text-gray-700">From</label>
        <select id="fromCurrency" class="mt-1 block w-full p-3 border border-gray-300 rounded-lg">
          <option value="USD">USD</option>
          <option value="ARS">ARS</option>
          <option value="EUR">EUR</option>
          <option value="BRL">BRL</option>
        </select>
        <input type="number" id="fromAmount" placeholder="Enter amount" class="mt-2 block w-full p-3 border border-gray-300 rounded-lg">
      </div>

      <!-- To -->
      <div>
        <label for="toCurrency" class="block text-sm font-medium text-gray-700">To</label>
        <select id="toCurrency" class="mt-1 block w-full p-3 border border-gray-300 rounded-lg">
          <option value="ARS">ARS</option>
          <option value="USD">USD</option>
          <option value="EUR">EUR</option>
          <option value="BRL">BRL</option>
        </select>
        <input type="text" id="toAmount" disabled class="mt-2 block w-full p-3 border border-gray-300 rounded-lg bg-gray-100 font-semibold">
      </div>
    </div>
  </div>

  <!-- Tablas de referencia -->
  <div id="referenceTables" class="mt-8 w-full max-w-4xl grid grid-cols-1 md:grid-cols-2 gap-6"></div>

  <script>
    const fromCurrency = document.getElementById("fromCurrency");
    const toCurrency = document.getElementById("toCurrency");
    const fromAmount = document.getElementById("fromAmount");
    const toAmount = document.getElementById("toAmount");
    const referenceTables = document.getElementById("referenceTables");

    async function convertCurrency() {
      const from = fromCurrency.value;
      const to = toCurrency.value;
      const amount = parseFloat(fromAmount.value) || 0;

      const res = await fetch(`https://api.exchangerate.host/latest?base=${from}&symbols=${to}`);
      const data = await res.json();
      const rate = data.rates[to];

      toAmount.value = (amount * rate).toFixed(2);

      updateTables(from, to, rate);
    }

    function updateTables(from, to, rate) {
      const steps = [1, 5, 10, 25, 50, 100, 500, 1000, 5000, 10000];

      let leftTable = `
        <div class="bg-white shadow rounded-2xl p-4">
          <h2 class="text-lg font-bold mb-3">${from} → ${to}</h2>
          <table class="w-full text-sm">
            <tbody>
              ${steps.map(val => `
                <tr class="border-b">
                  <td class="py-2 font-semibold">${val} ${from}</td>
                  <td class="py-2">${(val * rate).toFixed(2)} ${to}</td>
                </tr>
              `).join("")}
            </tbody>
          </table>
        </div>`;

      let rightTable = `
        <div class="bg-white shadow rounded-2xl p-4">
          <h2 class="text-lg font-bold mb-3">${to} → ${from}</h2>
          <table class="w-full text-sm">
            <tbody>
              ${steps.map(val => `
                <tr class="border-b">
                  <td class="py-2 font-semibold">${val} ${to}</td>
                  <td class="py-2">${(val / rate).toFixed(2)} ${from}</td>
                </tr>
              `).join("")}
            </tbody>
          </table>
        </div>`;

      referenceTables.innerHTML = leftTable + rightTable;
    }

    fromCurrency.addEventListener("change", convertCurrency);
    toCurrency.addEventListener("change", convertCurrency);
    fromAmount.addEventListener("input", convertCurrency);

    // Init
    convertCurrency();
  </script>
</body>
</html>


