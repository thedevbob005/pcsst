const root = document.documentElement;
const themeStorageKey = "pcsst-theme";
const navToggle = document.querySelector("[data-nav-toggle]");
const navMenu = document.querySelector("[data-site-menu]");
const searchInput = document.querySelector("[data-doc-search]");
const searchResults = document.querySelector("[data-search-results]");
const searchCount = document.querySelector("[data-search-count]");

function updateThemeButtons() {
  const activeTheme = root.dataset.pcsstTheme || "treasure";
  document.querySelectorAll("[data-theme-switch]").forEach((button) => {
    button.setAttribute(
      "aria-pressed",
      button.dataset.themeSwitch === activeTheme ? "true" : "false"
    );
  });
}

function applyStoredTheme() {
  const storedTheme = window.localStorage.getItem(themeStorageKey);
  if (storedTheme) {
    root.dataset.pcsstTheme = storedTheme;
  }
  updateThemeButtons();
}

function setCurrentNavLink() {
  const currentPage = window.location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll("[data-nav-link]").forEach((link) => {
    const href = (link.getAttribute("href") || "").split("#")[0];
    if (href.endsWith(currentPage)) {
      link.setAttribute("aria-current", "page");
    }
  });
}

function registerThemeSwitcher() {
  document.querySelectorAll("[data-theme-switch]").forEach((button) => {
    button.addEventListener("click", () => {
      root.dataset.pcsstTheme = button.dataset.themeSwitch;
      window.localStorage.setItem(themeStorageKey, button.dataset.themeSwitch);
      updateThemeButtons();
    });
  });
}

function registerCopyButtons() {
  document.querySelectorAll("[data-copy]").forEach((button) => {
    const originalHTML = button.innerHTML;
    const originalLabel = button.getAttribute("aria-label") || "Copy to clipboard";
    let timeout;

    button.addEventListener("click", async () => {
      const container = button.closest(".code-card, .command-card");
      const block = container?.querySelector("code");

      if (!block) {
        return;
      }

      window.clearTimeout(timeout);

      try {
        await navigator.clipboard.writeText(block.innerText.trim());
        button.innerHTML = "Copied";
        button.setAttribute("aria-label", "Copied to clipboard");
        button.classList.add("is-valid");
      } catch {
        button.innerHTML = "Error";
        button.setAttribute("aria-label", "Copy failed");
        button.classList.add("is-invalid");
      }

      timeout = window.setTimeout(() => {
        button.innerHTML = originalHTML;
        button.setAttribute("aria-label", originalLabel);
        button.classList.remove("is-valid", "is-invalid");
      }, 1400);
    });
  });
}

function registerNavToggle() {
  if (!navToggle || !navMenu) {
    return;
  }

  navToggle.addEventListener("click", () => {
    const isOpen = navMenu.classList.toggle("is-open");
    navToggle.setAttribute("aria-expanded", String(isOpen));
  });

  navMenu.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      navMenu.classList.remove("is-open");
      navToggle.setAttribute("aria-expanded", "false");
    });
  });
}

function renderSearchResults(entries, query) {
  if (!searchResults || !searchCount) {
    return;
  }

  const normalizedQuery = query.trim().toLowerCase();
  const filteredEntries = normalizedQuery
    ? entries.filter((entry) => {
        const haystack = [entry.title, entry.summary, ...(entry.keywords || [])]
          .join(" ")
          .toLowerCase();
        return haystack.includes(normalizedQuery);
      })
    : entries;

  searchResults.innerHTML = "";
  searchCount.textContent = normalizedQuery
    ? `${filteredEntries.length} result${filteredEntries.length === 1 ? "" : "s"}`
    : `${filteredEntries.length} docs entries`;

  if (!filteredEntries.length) {
    const emptyState = document.createElement("article");
    emptyState.className = "search-empty";
    emptyState.textContent = "No docs entries matched that query.";
    searchResults.appendChild(emptyState);
    return;
  }

  filteredEntries.forEach((entry) => {
    const card = document.createElement("article");
    card.className = "card section-card stack stack-3";

    const badge = document.createElement("span");
    badge.className = "badge badge--accent";
    badge.textContent = entry.section;

    const title = document.createElement("h2");
    title.textContent = entry.title;

    const summary = document.createElement("p");
    summary.className = "muted";
    summary.textContent = entry.summary;

    const link = document.createElement("a");
    link.className = "button button--ghost";
    link.href = entry.url;
    link.textContent = "Open entry";

    card.append(badge, title, summary, link);
    searchResults.appendChild(card);
  });
}

async function setupSearch() {
  if (!searchInput || !searchResults || !searchCount) {
    return;
  }

  try {
    const response = await fetch("./search-index.json");
    const entries = await response.json();
    const params = new URLSearchParams(window.location.search);
    const initialQuery = params.get("q") || "";

    searchInput.value = initialQuery;
    renderSearchResults(entries, initialQuery);

    searchInput.addEventListener("input", () => {
      const nextQuery = searchInput.value;
      const nextParams = new URLSearchParams(window.location.search);

      if (nextQuery) {
        nextParams.set("q", nextQuery);
      } else {
        nextParams.delete("q");
      }

      const nextUrl = `${window.location.pathname}${nextParams.toString() ? `?${nextParams.toString()}` : ""}`;
      window.history.replaceState({}, "", nextUrl);
      renderSearchResults(entries, nextQuery);
    });

    if (!initialQuery) {
      searchInput.focus();
    }
  } catch {
    searchCount.textContent = "Search index unavailable";
    searchResults.innerHTML = "";
    const emptyState = document.createElement("article");
    emptyState.className = "search-empty";
    emptyState.textContent = "The search index could not be loaded on this page.";
    searchResults.appendChild(emptyState);
  }
}

function registerSearchShortcut() {
  window.addEventListener("keydown", (event) => {
    const isShortcut = event.key.toLowerCase() === "k" && (event.metaKey || event.ctrlKey);
    if (!isShortcut) {
      return;
    }

    event.preventDefault();

    if (searchInput) {
      searchInput.focus();
      searchInput.select();
      return;
    }

    window.location.href = "./search.html";
  });
}

applyStoredTheme();
setCurrentNavLink();
registerThemeSwitcher();
registerCopyButtons();
registerNavToggle();
registerSearchShortcut();
setupSearch();
