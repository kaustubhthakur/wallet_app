document.addEventListener("DOMContentLoaded", () => {
  const token = localStorage.getItem("token");
  if (!token) {
    window.location.href = "login.html";
    return;
  }

  const balanceSpan = document.getElementById("balance");
  const transactionsList = document.getElementById("transactions");

  async function fetchBalance() {
    const res = await apiRequest("/wallet/balance/");
    balanceSpan.textContent = res.balance;
  }

  async function fetchTransactions() {
    const res = await apiRequest("/wallet/transactions/");
    transactionsList.innerHTML = "";
    res.transactions.forEach(tx => {
      const li = document.createElement("li");
      li.textContent = `${tx.date} - ₹${tx.amount} (${tx.type})`;
      transactionsList.appendChild(li);
    });
  }

  document.getElementById("refreshBalance").onclick = fetchBalance;

  document.getElementById("enableWallet").onclick = async () => {
    await apiRequest("/wallet/enable/", "POST");
    fetchBalance();
  };

  fetchBalance();
  fetchTransactions();
});
