document.addEventListener("DOMContentLoaded", async function () {
    const postsPageUrl = "BlogPosts/blogMain.html";
    const container = document.querySelector(".blog-posts");

    if (!container) {
        return;
    }

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

        container.innerHTML = "";
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

            container.appendChild(postClone);
        });
    } catch (error) {
        console.error("Error fetching blog posts:", error);
    }
});

