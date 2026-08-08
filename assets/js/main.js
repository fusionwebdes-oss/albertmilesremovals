(function () {
  'use strict';

  /* ---------- Mobile navigation ---------- */
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.main-nav');
  var backdrop = document.querySelector('.nav-backdrop');

  function closeNav() {
    if (nav) nav.classList.remove('open');
    if (toggle) toggle.classList.remove('open');
    if (backdrop) backdrop.classList.remove('show');
  }

  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      nav.classList.toggle('open');
      toggle.classList.toggle('open');
      if (backdrop) backdrop.classList.toggle('show');
    });
  }
  if (backdrop) backdrop.addEventListener('click', closeNav);

  /* Mobile dropdown toggle for has-children */
  var parents = document.querySelectorAll('.has-children');
  parents.forEach(function (p) {
    if (window.innerWidth <= 860) {
      var link = p.querySelector('a');
      if (link) {
        link.addEventListener('click', function (e) {
          if (window.innerWidth <= 860 && p.classList.contains('open')) {
            return; // let it follow the link
          }
          if (window.innerWidth <= 860) {
            e.preventDefault();
            p.classList.toggle('open');
          }
        });
      }
    }
  });

  /* Close nav on resize to desktop */
  window.addEventListener('resize', function () {
    if (window.innerWidth > 860) closeNav();
  });

  /* ---------- Testimonial slider ---------- */
  var slider = document.querySelector('[data-slider]');
  if (slider) {
    var track = slider.querySelector('.slider-track');
    var slides = track.children;
    var prevBtn = slider.querySelector('[data-prev]');
    var nextBtn = slider.querySelector('[data-next]');
    var index = 0;

    function slideWidth() { return slider.clientWidth; }
    function go(i) {
      if (i < 0) i = slides.length - 1;
      if (i > slides.length - 1) i = 0;
      index = i;
      track.style.transform = 'translateX(-' + (index * 100) + '%)';
    }

    if (prevBtn) prevBtn.addEventListener('click', function () { go(index - 1); });
    if (nextBtn) nextBtn.addEventListener('click', function () { go(index + 1); });

    var timer = setInterval(function () { go(index + 1); }, 7000);
    slider.addEventListener('mouseenter', function () { clearInterval(timer); });
    slider.addEventListener('mouseleave', function () {
      timer = setInterval(function () { go(index + 1); }, 7000);
    });

    window.addEventListener('resize', function () {
      track.style.transform = 'translateX(-' + (index * 100) + '%)';
    });
  }

  /* ---------- Quote form stepper ---------- */
  var quoteForm = document.getElementById('quoteForm');
  if (quoteForm) {
    var steps = quoteForm.querySelectorAll('.form-step');
    var pills = quoteForm.querySelectorAll('.step-pill');
    var currentStep = 0;

    function goToStep(i) {
      if (i < 0 || i >= steps.length) return;
      currentStep = i;
      steps.forEach(function (s, idx) {
        s.classList.toggle('is-active', idx === i);
      });
      pills.forEach(function (p, idx) {
        p.classList.toggle('is-active', idx === i);
        p.classList.toggle('is-done', idx < i);
      });
      var back = steps[i].querySelector('.btn-back');
      if (back) back.hidden = (i === 0);
      if (i === steps.length - 1) {
        quoteForm.querySelector('.quote-stepper').scrollIntoView({ behavior: 'smooth', block: 'start' });
      } else {
        steps[i].scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
      var first = steps[i].querySelector('input, select, textarea');
      if (first) first.focus({ preventScroll: true });
    }

    steps.forEach(function (step, i) {
      var next = step.querySelector('.btn-next');
      if (next) {
        next.addEventListener('click', function () {
          var fields = step.querySelectorAll('input, select, textarea');
          for (var f = 0; f < fields.length; f++) {
            if (!fields[f].checkValidity()) {
              fields[f].reportValidity();
              return;
            }
          }
          goToStep(i + 1);
        });
      }
      var back = step.querySelector('.btn-back');
      if (back) {
        back.addEventListener('click', function () { goToStep(i - 1); });
      }
    });
  }

  /* ---------- Lazy images fallback ---------- */
  if ('loading' in HTMLImageElement.prototype) { /* native lazy ok */ }

  /* ---------- Quote / call popup ---------- */
  var popup = document.getElementById('quotePopup');
  if (popup && !sessionStorage.getItem('amPopupShown')) {
    var closePopup = function () {
      popup.classList.remove('open');
      setTimeout(function () { popup.hidden = true; }, 300);
    };
    setTimeout(function () {
      popup.hidden = false;
      requestAnimationFrame(function () { popup.classList.add('open'); });
      sessionStorage.setItem('amPopupShown', '1');
    }, 3500);
    var popupCloseBtn = popup.querySelector('.popup-close');
    if (popupCloseBtn) popupCloseBtn.addEventListener('click', closePopup);
    popup.addEventListener('click', function (e) { if (e.target === popup) closePopup(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closePopup(); });
  }
})();
