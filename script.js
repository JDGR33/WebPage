document.addEventListener("DOMContentLoaded", async function () {
    const postsPageUrl = "BlogPosts/blogMain.html"; // Correct path to the blog posts page

    try {
        // Fetch the blogMain.html file
        const response = await fetch(postsPageUrl);
        const text = await response.text();

        // Parse the HTML from the response
        const parser = new DOMParser();
        const doc = parser.parseFromString(text, "text/html");

        // Select all blog posts
        const allPosts = Array.from(doc.querySelectorAll(".blog-posts article"));

        // Shuffle the posts and pick three
        const randomPosts = allPosts.sort(() => Math.random() - 0.5).slice(0, 3);

        // Add the random posts to the main page
        const container = document.querySelector(".blog-posts");
        container.innerHTML = ''; // Clear existing content

        randomPosts.forEach(post => container.appendChild(post));
    } catch (error) {
        console.error("Error fetching blog posts:", error);
    }
});

