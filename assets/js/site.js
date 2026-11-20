(() => {
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)');

  /* Hero reel: plays muted on loop, with a pause control. Stays still under reduced motion. */
  const heroVideo = document.querySelector('.hero__video');
  const pauseBtn = document.querySelector('.hero__pause');
  if (heroVideo && pauseBtn) {
    const setLabel = () => {
      const paused = heroVideo.paused;
      pauseBtn.textContent = paused ? 'Play' : 'Pause';
      pauseBtn.setAttribute('aria-pressed', String(paused));
    };
    pauseBtn.hidden = false;
    pauseBtn.addEventListener('click', () => {
      if (heroVideo.paused) heroVideo.play().catch(() => {}); else heroVideo.pause();
    });
    heroVideo.addEventListener('play', setLabel);
    heroVideo.addEventListener('pause', setLabel);
    let userPaused = false;
    pauseBtn.addEventListener('click', () => { userPaused = !heroVideo.paused; });
    if (!reduce.matches) {
      // Only play while on screen.
      new IntersectionObserver(([e]) => {
        if (e.isIntersecting && !userPaused) heroVideo.play().catch(() => {});
        else heroVideo.pause();
      }, { threshold: 0.25 }).observe(heroVideo);
    }
    setLabel();
  }

  /* Reels: one at a time. */
  const reels = [...document.querySelectorAll('.reel video')];
  reels.forEach((v) => v.addEventListener('play', () => {
    reels.forEach((o) => { if (o !== v) o.pause(); });
    if (heroVideo) heroVideo.pause();
  }));

  /* Reels: show eight, then the rest on request. */
  const reelSection = document.querySelector('.reels');
  const moreBtn = document.querySelector('.reels__more');
  if (reelSection && moreBtn && document.querySelector('.reel[data-more]')) {
    reelSection.classList.add('is-collapsed');
    moreBtn.hidden = false;
    moreBtn.addEventListener('click', () => {
      const open = reelSection.classList.toggle('is-collapsed') === false;
      moreBtn.setAttribute('aria-expanded', String(open));
      moreBtn.textContent = open ? 'Show fewer reels' : moreBtn.dataset.label;
      if (!open) reelSection.scrollIntoView({ block: 'start' });
    });
    moreBtn.dataset.label = moreBtn.textContent;
  }

  /* Gallery dialog per sector. */
  const dialog = document.querySelector('.gallery');
  const data = window.GALLERY || {};
  if (dialog && typeof dialog.showModal === 'function') {
    const title = dialog.querySelector('.gallery__title');
    const grid = dialog.querySelector('.gallery__grid');
    let opener = null;
    document.querySelectorAll('[data-gallery]').forEach((btn) => {
      btn.hidden = false;
      btn.addEventListener('click', () => {
        const set = data[btn.dataset.gallery];
        if (!set) return;
        opener = btn;
        title.textContent = set.title;
        grid.innerHTML = set.items.map(([n, w, h]) => {
          const id = String(n).padStart(2, '0');
          return `<li><a href="assets/work/w${id}.webp" target="_blank" rel="noopener" aria-label="Open post ${id} full size"><img src="assets/work/w${id}-s.webp" width="${w}" height="${h}" alt="" loading="lazy" decoding="async"></a></li>`;
        }).join('');
        dialog.showModal();
        dialog.scrollTop = 0;
      });
    });
    dialog.querySelector('.gallery__close').addEventListener('click', () => dialog.close());
    dialog.addEventListener('click', (e) => { if (e.target === dialog) dialog.close(); });
    dialog.addEventListener('close', () => { if (opener) opener.focus(); });
  }

  /* Stacked cards: a card recedes slightly as the next one slides over it. */
  const cards = [...document.querySelectorAll('.sector')];
  const stackable = window.matchMedia('(min-width: 60rem) and (min-height: 680px)');
  let ticking = false;
  const update = () => {
    ticking = false;
    if (reduce.matches || !stackable.matches) { cards.forEach((c) => { c.style.transform = ''; }); return; }
    cards.forEach((card, i) => {
      const next = cards[i + 1];
      if (!next) return;
      const a = card.getBoundingClientRect();
      const b = next.getBoundingClientRect();
      const overlap = Math.min(Math.max((a.bottom - b.top) / a.height, 0), 1);
      card.style.transform = overlap ? `scale(${1 - overlap * 0.05})` : '';
    });
  };
  const onScroll = () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } };
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll, { passive: true });
  update();

  /* Rail: mark the section in view. */
  const links = [...document.querySelectorAll('.rail ul a')];
  const sections = links.map((a) => document.querySelector(a.getAttribute('href'))).filter(Boolean);
  if ('IntersectionObserver' in window && sections.length) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (!e.isIntersecting) return;
        links.forEach((a) => a.toggleAttribute('aria-current', a.getAttribute('href') === `#${e.target.id}`));
        links.forEach((a) => { if (a.hasAttribute('aria-current')) a.setAttribute('aria-current', 'true'); });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    sections.forEach((s) => io.observe(s));
  }
})();
