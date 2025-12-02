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

    // 日付順にソートして HTML を生成
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

  } catch (e) {
    container.innerHTML = "更新情報の読み込みに失敗しました";
    console.error(e);
  }
}

// ページ読み込み時に更新情報を表示
window.addEventListener("DOMContentLoaded", loadUpdates);
