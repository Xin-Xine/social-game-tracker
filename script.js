async function loadUpdates() {
  const container = document.getElementById("calendar");
  container.innerHTML = "読み込み中…";

  try {
    const res = await fetch("./data/result.json");
    const data = await res.json();

    // 日付ごとにグループ化
    const grouped = {};
    data.forEach(item => {
      if (!grouped[item.date]) grouped[item.date] = [];
      grouped[item.date].push(item);
    });

    // カレンダー形式で表示
    container.innerHTML = Object.keys(grouped).sort().map(date => {
      return `
        <div class="day">
          <h3>${date}</h3>
          ${grouped[date].map(u => `
            <div class="update-item">
              <h4>${u.title}</h4>
              <p>ゲーム名：${u.game}</p>
              <p>${u.description}</p>
              <a href="${u.link}" target="_blank">公式サイト</a>
            </div>
          `).join("")}
        </div>
      `;
    }).join("");

  } catch(e) {
    container.innerHTML = "読み込み失敗";
  }
}

// ボタンで手動更新（ローカルテスト用）
document.getElementById("refresh").addEventListener("click", async () => {
  alert("ローカルでは Python を実行してください。\nGitHub上では Actions の手動実行で更新されます。");
});

loadUpdates();
