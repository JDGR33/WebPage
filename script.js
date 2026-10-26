(function () {
    const savedTheme = localStorage.getItem("theme");
    const prefersDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
    const initialTheme = savedTheme || (prefersDark ? "dark" : "light");
    document.documentElement.setAttribute("data-theme", initialTheme);
})();

document.addEventListener("DOMContentLoaded", async function () {
    // 1. Setup Theme Toggle Button in Navbar
    const nav = document.querySelector("header nav") || document.querySelector("nav");
    if (nav && !nav.querySelector(".theme-toggle")) {
        const toggleBtn = document.createElement("button");
        toggleBtn.className = "theme-toggle";
        toggleBtn.type = "button";
        toggleBtn.setAttribute("aria-label", "Toggle color theme");

        const updateIcon = () => {
            const current = document.documentElement.getAttribute("data-theme");
            toggleBtn.textContent = current === "dark" ? "☀️" : "🌙";
            toggleBtn.title = current === "dark" ? "Switch to light mode" : "Switch to dark mode";
        };
        updateIcon();

        toggleBtn.addEventListener("click", () => {
            const current = document.documentElement.getAttribute("data-theme");
            const next = current === "dark" ? "light" : "dark";
            document.documentElement.setAttribute("data-theme", next);
            localStorage.setItem("theme", next);
            updateIcon();
        });

        nav.appendChild(toggleBtn);
    }

    // 2. Setup Blog Search Filter on blogMain.html
    const searchInput = document.getElementById("blog-search");
    const postCountEl = document.getElementById("post-count");
    const blogContainer = document.querySelector(".blog-posts");

    if (searchInput && blogContainer) {
        const articles = Array.from(blogContainer.querySelectorAll("article"));
        const updateCount = (visibleCount) => {
            if (postCountEl) {
                postCountEl.textContent = `${visibleCount} of ${articles.length} posts`;
            }
        };
        updateCount(articles.length);

        searchInput.addEventListener("input", (e) => {
            const query = e.target.value.trim().toLowerCase();
            let visible = 0;
            articles.forEach((article) => {
                const text = article.textContent.toLowerCase();
                const match = !query || text.includes(query);
                article.style.display = match ? "" : "none";
                if (match) visible++;
            });
            updateCount(visible);
        });
    }

    // 3. Featured Posts Loader on Home Page (index.html)
    const isHomePage = !window.location.pathname.includes("/BlogPosts/");
    if (!isHomePage || !blogContainer) {
        return;
    }

    const postsPageUrl = "BlogPosts/blogMain.html";

    try {
        const response = await fetch(postsPageUrl);
        if (!response.ok) {
            throw new Error(`Request failed with status ${response.status}`);
        }

        const text = await response.text();
        const parser = new DOMParser();
        const doc = parser.parseFromString(text, "text/html");
        const allPosts = Array.from(doc.querySelectorAll(".blog-posts article"));

        if (allPosts.length === 0) {
            throw new Error("No blog posts found in blogMain.html");
        }

        const randomPosts = allPosts.sort(() => Math.random() - 0.5).slice(0, 3);

        blogContainer.innerHTML = "";
        randomPosts.forEach((post) => {
            const postClone = post.cloneNode(true);

            // Keep links working when content is copied from BlogPosts/blogMain.html to index.html.
            postClone.querySelectorAll("a[href]").forEach((anchor) => {
                const href = anchor.getAttribute("href") || "";
                const isExternal = /^(?:[a-z]+:|\/\/|#)/i.test(href);

                if (!isExternal && !href.startsWith("BlogPosts/")) {
                    anchor.setAttribute("href", `BlogPosts/${href.replace(/^\.\//, "")}`);
                }
            });

            blogContainer.appendChild(postClone);
        });
    } catch (error) {
        console.error("Error fetching blog posts:", error);
    }
});
