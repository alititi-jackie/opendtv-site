/**
 * OpenAA 华人导航 - script.js
 * Interactions: banner carousel, category tabs, search filter
 */

// ===================================================
// 广告数据 (修改此处可更换广告图片和链接)
// ===================================================
const ADS = [
  {
    image: 'assets/ads/ad-1.png',
    link: 'https://app.openaa.com/jobs',
    alt: '招聘广告'
  },
  {
    image: 'assets/ads/ad-2.png',
    link: 'https://app.openaa.com/housing',
    alt: '房屋广告'
  },
  {
    image: 'assets/ads/ad-3.png',
    link: 'https://app.openaa.com/dmv/ny/practice',
    alt: 'DMV 广告'
  },
  {
    image: 'assets/ads/ad-4.png',
    link: 'https://openaa.com/nav/',
    alt: '导航广告'
  },
  {
    image: 'assets/ads/ad-5.png',
    link: 'https://openaa.com',
    alt: 'OpenAA 广告'
  }
]

// ===================================================
// BANNER CAROUSEL
// ===================================================
;(function initBanner() {
  const track = document.getElementById('bannerTrack')
  const dotsContainer = document.getElementById('bannerDots')
  if (!track || !dotsContainer) return

  let current = 0
  let total = ADS.length
  let autoplayTimer = null
  let touchStartX = 0
  let touchStartY = 0
  let isDragging = false
  let dragOffsetX = 0

  // Build slides
  function buildSlides() {
    track.innerHTML = ''
    dotsContainer.innerHTML = ''

    ADS.forEach(function(ad, i) {
      const a = document.createElement('a')
      a.href = ad.link
      a.target = '_blank'
      a.rel = 'noopener noreferrer'
      a.className = 'banner-slide'

      const img = new Image()
      img.alt = ad.alt || ''
      img.draggable = false
      img.loading = i === 0 ? 'eager' : 'lazy'

      // On error: show placeholder
      img.onerror = function() {
        const ph = document.createElement('div')
        ph.className = 'banner-placeholder'
        ph.innerHTML = '<span>' + (ad.alt || 'OpenAA') + '</span>'
        a.replaceChild(ph, img)
      }
      img.src = ad.image
      a.appendChild(img)
      track.appendChild(a)

      // Dot
      const dot = document.createElement('button')
      dot.className = 'banner-dot' + (i === 0 ? ' active' : '')
      dot.setAttribute('aria-label', '第' + (i + 1) + '张')
      dot.type = 'button'
      dot.addEventListener('click', function() { goTo(i); resetAutoplay() })
      dotsContainer.appendChild(dot)
    })

    total = ADS.length
  }

  function updateDots() {
    const dots = dotsContainer.querySelectorAll('.banner-dot')
    dots.forEach(function(d, i) {
      d.classList.toggle('active', i === current)
    })
  }

  function goTo(index) {
    if (total === 0) return
    current = ((index % total) + total) % total
    track.style.transform = 'translateX(-' + (current * 100) + '%)'
    updateDots()
  }

  function next() { goTo(current + 1) }
  function prev() { goTo(current - 1) }

  function startAutoplay() {
    autoplayTimer = setInterval(next, 4000)
  }

  function resetAutoplay() {
    clearInterval(autoplayTimer)
    startAutoplay()
  }

  // Touch / swipe support
  const wrapper = track.parentElement
  wrapper.addEventListener('touchstart', function(e) {
    touchStartX = e.touches[0].clientX
    touchStartY = e.touches[0].clientY
    isDragging = false
    dragOffsetX = 0
    clearInterval(autoplayTimer)
  }, { passive: true })

  wrapper.addEventListener('touchmove', function(e) {
    const dx = e.touches[0].clientX - touchStartX
    const dy = e.touches[0].clientY - touchStartY
    if (!isDragging && Math.abs(dy) > Math.abs(dx)) return
    isDragging = true
    dragOffsetX = dx
    // live drag feedback
    const baseOffset = current * 100
    const pixelOffset = (dragOffsetX / wrapper.offsetWidth) * 100
    track.style.transition = 'none'
    track.style.transform = 'translateX(calc(-' + baseOffset + '% + ' + dragOffsetX + 'px))'
  }, { passive: true })

  wrapper.addEventListener('touchend', function() {
    track.style.transition = ''
    if (!isDragging) { startAutoplay(); return }
    const threshold = wrapper.offsetWidth * 0.2
    if (dragOffsetX < -threshold) {
      next()
    } else if (dragOffsetX > threshold) {
      prev()
    } else {
      goTo(current)
    }
    isDragging = false
    startAutoplay()
  })

  // Pause autoplay when tab is hidden
  document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
      clearInterval(autoplayTimer)
    } else {
      startAutoplay()
    }
  })

  buildSlides()
  if (total > 0) {
    goTo(0)
    startAutoplay()
  }
})()

// ===================================================
// CATEGORY TAB SWITCHING
// ===================================================
// Module order in DOM: featured(0), gov(1), bank(2), shop(3), dmv(4), tools(5), ai(6)
// Category "全部" shows all; others show from their start module down

var categoryStartModule = {
  all:  null,          // show all
  gov:  'gov',
  bank: 'bank',
  shop: 'shop',
  dmv:  'dmv'
}

function switchCategory(cat, btn) {
  // Update tab buttons
  document.querySelectorAll('.cat-tab').forEach(function(t) {
    t.classList.remove('active')
    t.setAttribute('aria-selected', 'false')
  })
  if (btn) {
    btn.classList.add('active')
    btn.setAttribute('aria-selected', 'true')
  }

  // Clear any active search when switching tabs
  var searchVal = document.getElementById('searchInput').value.trim()

  var modules = document.querySelectorAll('.nav-module')
  var startModule = categoryStartModule[cat]

  if (cat === 'all') {
    modules.forEach(function(m) {
      m.classList.remove('hidden')
    })
  } else {
    // Hide all modules before the start module, show from start module onward
    var showing = false
    modules.forEach(function(m) {
      if (m.dataset.module === startModule) showing = true
      m.classList.toggle('hidden', !showing)
    })
  }

  // If there's an active search, re-apply filtering on newly visible modules
  if (searchVal) {
    applySearch(searchVal)
  }
}

// ===================================================
// SEARCH FILTER
// ===================================================
function handleSearch(value) {
  var clearBtn = document.getElementById('searchClear')
  if (value.trim()) {
    clearBtn.classList.add('visible')
  } else {
    clearBtn.classList.remove('visible')
  }
  applySearch(value.trim())
}

function clearSearch() {
  var input = document.getElementById('searchInput')
  input.value = ''
  document.getElementById('searchClear').classList.remove('visible')
  applySearch('')
  input.focus()
}

function applySearch(query) {
  var modules = document.querySelectorAll('.nav-module')
  var noResults = document.getElementById('noResults')
  var q = query.toLowerCase()
  var anyVisible = false

  modules.forEach(function(module) {
    // Skip modules hidden by category tab
    if (module.classList.contains('hidden')) return

    if (!q) {
      // No search: show all cards in visible modules
      module.classList.remove('search-empty')
      module.querySelectorAll('.nav-card').forEach(function(card) {
        card.classList.remove('search-hidden')
      })
      anyVisible = true
      return
    }

    var cards = module.querySelectorAll('.nav-card')
    var moduleTitle = module.querySelector('.module-title')
    var moduleName = moduleTitle ? moduleTitle.textContent.toLowerCase() : ''

    // If module title matches, show all cards in it
    var moduleMatch = moduleName.includes(q)
    var visibleCards = 0

    cards.forEach(function(card) {
      var name = (card.querySelector('.nav-card-name') || {}).textContent || ''
      var match = moduleMatch || name.toLowerCase().includes(q)
      card.classList.toggle('search-hidden', !match)
      if (match) visibleCards++
    })

    var hasVisible = visibleCards > 0
    module.classList.toggle('search-empty', !hasVisible)
    if (hasVisible) anyVisible = true
  })

  noResults.style.display = anyVisible ? 'none' : 'block'
}

// ===================================================
// SHARE
// ===================================================
function shareOpenAA() {
  var shareData = {
    title: 'OpenAA 华人导航',
    text: '美国华人必备导航，政府、银行、DMV、购物一站搞定',
    url: 'https://openaa.com'
  }
  if (navigator.share) {
    navigator.share(shareData).catch(function() {})
  } else {
    // Fallback: copy to clipboard
    var url = shareData.url
    if (navigator.clipboard) {
      navigator.clipboard.writeText(url).then(function() {
        showToast('链接已复制 📋')
      }).catch(function() {
        showToast('分享：' + url)
      })
    } else {
      var ta = document.createElement('textarea')
      ta.value = url
      ta.style.position = 'fixed'
      ta.style.opacity = '0'
      document.body.appendChild(ta)
      ta.select()
      try { document.execCommand('copy'); showToast('链接已复制 📋') } catch(e) {}
      document.body.removeChild(ta)
    }
  }
}

function showToast(msg) {
  var existing = document.getElementById('oaa-toast')
  if (existing) existing.remove()

  var toast = document.createElement('div')
  toast.id = 'oaa-toast'
  toast.textContent = msg
  toast.style.cssText = [
    'position:fixed',
    'bottom:88px',
    'left:50%',
    'transform:translateX(-50%)',
    'background:rgba(24,24,27,0.9)',
    'color:#fff',
    'font-size:13px',
    'font-weight:500',
    'padding:10px 20px',
    'border-radius:999px',
    'z-index:9999',
    'pointer-events:none',
    'white-space:nowrap',
    'backdrop-filter:blur(8px)',
    '-webkit-backdrop-filter:blur(8px)',
    'box-shadow:0 4px 16px rgba(0,0,0,0.2)'
  ].join(';')
  document.body.appendChild(toast)
  setTimeout(function() { toast.remove() }, 2500)
}
