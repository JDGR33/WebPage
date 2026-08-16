# ToDo
- [x] `WRITE`: Simple about me section
- [x] `WRITE`: Simple Contact section
- [x] `RE DO`: The blog posts in the main page should be "feature articles"
- [x] `ADD`: Create a page for all the blog posts
- [x] `WRITE`: First blog post.
- [x] `RE DO`: Add emjois to the sctions
- [x] Post template
- [x] `GIT`: Upload this to git.  
- [x] `ADD`: Add CV
- [x] `ADD`: A way to go back to the main page and the BlogPosts
- [ ] `ADD`: Give it more life
- [ ] `WRITE`: A about page with more detail (add a table of contents on it.)
- [ ] `ADD`: Add a script to add new post

## Run Locally

Use a local server so JavaScript `fetch` works reliably:

```bash
cd /home/julio/WebPage
python3 -m http.server 8000
```

Then open:

http://localhost:8000/

## Generate New Blog Posts

Install dependencies:

```bash
cd /home/julio/WebPage
python3 -m pip install -r requirements.txt
```

Convert a markdown post into HTML and add it to the blog index:

```bash
python3 utils.py BlogPosts/post13.md
```

Optional metadata at the top of the markdown file:

```md
---
title: My Post Title
description: One line summary for blogMain.html
date: 2026-08-16
tags: AI, Python
---

## My Post Title
```

Useful flags:

```bash
# Override metadata from CLI
python3 utils.py BlogPosts/post13.md --title "Custom Title" --description "Short summary"

# Generate HTML but do not update blogMain.html
python3 utils.py BlogPosts/post13.md --no-index
```

Link to the local page: ["\\wsl.localhost\Ubuntu\home\julio\WebPage\index.html"](file://wsl.localhost/Ubuntu/home/julio/WebPage/index.html)

# BrainStorm:
* A page where I list My Job experience with summaries for each work and a link for a full story about it. That way I could document my job experiences.

