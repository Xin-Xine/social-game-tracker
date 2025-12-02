async function loadUpdates() {
  const list = document.getElementById("list");

  try {
    const res = await fetch("./data/result.json");
    const data = await res.json();

    if (!data || data.length === 0) {
      list.innerHTML = "データがありません";
      return;
    }

    list.innerHTML = data.map(item => `
      <div class="update-item">
        <h3>${item.title}</h3>
        <p>ゲーム名：${item.game}</p>
        <p>更新日：${item.date}</p>
        <p>${item.description}</p>
        <a href="${item.link}" target="_blank">公式サイト</a>
      </div>
    `).join("");

  } catch (e) {
    list.innerHTML = "読み込みに失敗しました";
  }
}

loadUpdates();
