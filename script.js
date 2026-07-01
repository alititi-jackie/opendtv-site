/**
 * OpenDTV — script.js
 * Static data & UI rendering. Ready for Supabase migration.
 */

// =============================================
//  MOCK DATA  (migrate to /data/opendtv.js or Supabase later)
// =============================================

const featuredItems = [
  {
    name: "Netflix",
    emoji: "🎬",
    category: "影视平台",
    categorySlug: "streaming",
    description: "全球最大流媒体平台，海量英美剧与电影",
    url: "https://www.netflix.com",
  },
  {
    name: "Disney+",
    emoji: "🏰",
    category: "影视平台",
    categorySlug: "streaming",
    description: "Marvel、星球大战、迪士尼经典动画全收录",
    url: "https://www.disneyplus.com",
  },
  {
    name: "IPTV Smarters",
    emoji: "📡",
    category: "TV 应用",
    categorySlug: "apps",
    description: "最流行的 IPTV 播放器，支持 M3U 与 Xtream",
    url: "/apps.html",
  },
  {
    name: "Kodi",
    emoji: "🎮",
    category: "TV 应用",
    categorySlug: "apps",
    description: "开源多媒体中心，插件生态丰富可高度自定义",
    url: "/apps.html",
  },
  {
    name: "Fire TV Stick",
    emoji: "🔥",
    category: "电视设备",
    categorySlug: "devices",
    description: "亚马逊出品，价格亲民，支持4K HDR播放",
    url: "/devices.html",
  },
  {
    name: "Apple TV 4K",
    emoji: "🍎",
    category: "电视设备",
    categorySlug: "devices",
    description: "苹果生态最佳选择，性能强劲画质顶级",
    url: "/devices.html",
  },
];

// =============================================
//  RENDER FEATURED CARDS
// =============================================
function renderFeatured() {
  const grid = document.getElementById("featured-grid");
  if (!grid) return;

  grid.innerHTML = featuredItems
    .map(
      (item) => `
      <a href="${item.url}" class="featured-card" ${item.url.startsWith('http') ? 'target="_blank" rel="noopener noreferrer"' : ''}>
        <span class="featured-card-emoji">${item.emoji}</span>
        <span class="featured-card-name">${item.name}</span>
        <span class="featured-card-category">${item.category}</span>
        <p class="featured-card-desc">${item.description}</p>
      </a>
    `
    )
    .join("");
}

// =============================================
//  SEARCH HANDLER  (UI only, no backend)
// =============================================
function handleSearch(event) {
  event.preventDefault();
  const query = document
    .getElementById("search-input")
    .value.trim()
    .toLowerCase();
  if (!query) return;

  const grid = document.getElementById("featured-grid");
  if (!grid) return;

  const filtered = featuredItems.filter(
    (item) =>
      item.name.toLowerCase().includes(query) ||
      item.category.toLowerCase().includes(query) ||
      item.description.toLowerCase().includes(query)
  );

  if (filtered.length === 0) {
    grid.innerHTML = `<p style="color:var(--text-muted);grid-column:1/-1;padding:24px 0">没有找到"${escapeHtml(query)}"相关内容</p>`;
    return;
  }

  grid.innerHTML = filtered
    .map(
      (item) => `
      <a href="${item.url}" class="featured-card" ${item.url.startsWith('http') ? 'target="_blank" rel="noopener noreferrer"' : ''}>
        <span class="featured-card-emoji">${item.emoji}</span>
        <span class="featured-card-name">${item.name}</span>
        <span class="featured-card-category">${item.category}</span>
        <p class="featured-card-desc">${item.description}</p>
      </a>
    `
    )
    .join("");

  // Scroll to results
  document.querySelector(".section--alt")?.scrollIntoView({ behavior: "smooth", block: "start" });
}

function escapeHtml(str) {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

// =============================================
//  INIT
// =============================================
document.addEventListener("DOMContentLoaded", () => {
  renderFeatured();
});
