(function () {
  "use strict";

  var root = document.documentElement;
  var body = document.body;
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var themeColors = {
    midnight: "#070b16",
    aurora: "#0b0616",
    daylight: "#f6f7fb",
    ember: "#110906",
    forest: "#04120d"
  };

  function setTheme(theme, persist) {
    root.setAttribute("data-theme", theme);

    if (persist) {
      try {
        window.localStorage.setItem("portfolio-theme", theme);
      } catch (error) {}
    }

    var meta = document.getElementById("metaThemeColor");
    if (meta && themeColors[theme]) {
      meta.setAttribute("content", themeColors[theme]);
    }

    document.querySelectorAll("[data-theme-value]").forEach(function (button) {
      var isActive = button.getAttribute("data-theme-value") === theme;
      button.classList.toggle("is-active", isActive);
      button.setAttribute("aria-pressed", isActive ? "true" : "false");
    });
  }

  setTheme(root.getAttribute("data-theme") || "midnight", false);

  var themePicker = document.querySelector("[data-theme-picker]");
  var themeToggle = themePicker && themePicker.querySelector(".theme-toggle");

  function closeThemePicker() {
    if (!themePicker) return;
    themePicker.classList.remove("is-open");
    if (themeToggle) themeToggle.setAttribute("aria-expanded", "false");
  }

  if (themeToggle) {
    themeToggle.addEventListener("click", function (event) {
      event.stopPropagation();
      var isOpen = themePicker.classList.toggle("is-open");
      themeToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    });
  }

  document.querySelectorAll("[data-theme-value]").forEach(function (button) {
    button.addEventListener("click", function () {
      setTheme(button.getAttribute("data-theme-value"), true);
      closeThemePicker();
    });
  });

  document.addEventListener("click", function (event) {
    if (themePicker && !themePicker.contains(event.target)) {
      closeThemePicker();
    }
  });

  var navToggle = document.querySelector(".nav-toggle");
  var siteNav = document.getElementById("siteNav");

  function closeNav() {
    body.classList.remove("nav-open");
    if (navToggle) navToggle.setAttribute("aria-expanded", "false");
  }

  if (navToggle) {
    navToggle.addEventListener("click", function () {
      var isOpen = body.classList.toggle("nav-open");
      navToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    });
  }

  if (siteNav) {
    siteNav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", closeNav);
    });
  }

  document.querySelectorAll("[data-nav-close]").forEach(function (element) {
    element.addEventListener("click", closeNav);
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
      closeNav();
      closeThemePicker();
    }
  });

  var header = document.getElementById("siteHeader");
  var scrollBar = document.getElementById("scrollProgress");
  var toTop = document.getElementById("toTop");

  function onScroll() {
    var scrollTop = window.scrollY || window.pageYOffset;
    var scrollable = document.documentElement.scrollHeight - window.innerHeight;

    if (header) {
      header.classList.toggle("is-scrolled", scrollTop > 12);
    }

    if (toTop) {
      toTop.classList.toggle("is-visible", scrollTop > 600);
    }

    if (scrollBar) {
      var progress = scrollable > 0 ? (scrollTop / scrollable) * 100 : 0;
      scrollBar.style.width = Math.min(progress, 100) + "%";
    }
  }

  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  if (toTop) {
    toTop.addEventListener("click", function () {
      window.scrollTo({
        top: 0,
        behavior: reduceMotion ? "auto" : "smooth"
      });
    });
  }

  var revealElements = Array.prototype.slice.call(
    document.querySelectorAll(".reveal")
  );

  if ("IntersectionObserver" in window && !reduceMotion) {
    var revealObserver = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            revealObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );

    revealElements.forEach(function (element) {
      revealObserver.observe(element);
    });
  } else {
    revealElements.forEach(function (element) {
      element.classList.add("is-visible");
    });
  }

  function animateCounter(element) {
    var target = parseInt(element.getAttribute("data-count"), 10) || 0;

    if (reduceMotion || target === 0) {
      element.textContent = target;
      return;
    }

    var duration = 1100;
    var startTime = null;

    function step(timestamp) {
      if (!startTime) startTime = timestamp;
      var progress = Math.min((timestamp - startTime) / duration, 1);
      var eased = 1 - Math.pow(1 - progress, 3);
      element.textContent = Math.round(target * eased);

      if (progress < 1) {
        window.requestAnimationFrame(step);
      } else {
        element.textContent = target;
      }
    }

    window.requestAnimationFrame(step);
  }

  var counters = document.querySelectorAll("[data-count]");

  if ("IntersectionObserver" in window && !reduceMotion) {
    var counterObserver = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            animateCounter(entry.target);
            counterObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.6 }
    );

    counters.forEach(function (counter) {
      counterObserver.observe(counter);
    });
  } else {
    counters.forEach(animateCounter);
  }

  var filterBar = document.querySelector("[data-project-filters]");

  if (filterBar) {
    var filterButtons = Array.prototype.slice.call(
      filterBar.querySelectorAll("[data-filter]")
    );
    var projectCards = Array.prototype.slice.call(
      document.querySelectorAll("[data-project-card]")
    );
    var emptyState = document.querySelector("[data-filter-empty]");
    var filterCount = document.querySelector("[data-filter-count]");

    function applyFilter(filter) {
      var visible = 0;

      projectCards.forEach(function (card) {
        var technologies = (card.getAttribute("data-technologies") || "")
          .split("|")
          .filter(Boolean);
        var matches = filter === "all" || technologies.indexOf(filter) !== -1;
        card.hidden = !matches;
        if (matches) visible += 1;
      });

      if (emptyState) emptyState.hidden = visible !== 0;
      if (filterCount) {
        filterCount.textContent =
          visible + " project" + (visible === 1 ? "" : "s");
      }
    }

    filterButtons.forEach(function (button) {
      button.addEventListener("click", function () {
        filterButtons.forEach(function (item) {
          item.classList.remove("is-active");
        });
        button.classList.add("is-active");
        applyFilter(button.getAttribute("data-filter"));
      });
    });
  }

  document.querySelectorAll("[data-toast]").forEach(function (toast) {
    var closeButton = toast.querySelector("[data-toast-close]");
    var dismissed = false;

    function dismiss() {
      if (dismissed) return;
      dismissed = true;
      toast.classList.add("is-leaving");
      window.setTimeout(function () {
        toast.remove();
      }, 280);
    }

    if (closeButton) closeButton.addEventListener("click", dismiss);
    window.setTimeout(dismiss, 6000);
  });

  if (window.Swiper) {
    var testimonialSlider = document.querySelector(".testimonialSwiper");
    var certificatesSlider = document.querySelector(".certificatesSlider");

    if (testimonialSlider) {
      new window.Swiper(testimonialSlider, {
        slidesPerView: 1,
        spaceBetween: 20,
        navigation: {
          nextEl: ".test-swiper-button-next",
          prevEl: ".test-swiper-button-prev"
        },
        breakpoints: {
          768: {
            slidesPerView: 2,
            spaceBetween: 22
          }
        }
      });
    }

    if (certificatesSlider) {
      new window.Swiper(certificatesSlider, {
        slidesPerView: 1,
        spaceBetween: 16,
        pagination: {
          el: ".swiper-pagination--inline",
          clickable: true
        },
        navigation: {
          nextEl: ".cert-swiper-button-next",
          prevEl: ".cert-swiper-button-prev"
        },
        breakpoints: {
          640: {
            slidesPerView: 2,
            spaceBetween: 18
          },
          1024: {
            slidesPerView: 3,
            spaceBetween: 20
          }
        }
      });
    }
  }
})();
