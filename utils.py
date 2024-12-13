import sys

import markdown


def add_post_to_index(post_name: str, post_title: str, description="") -> None:

    blog_main_path = "BlogPosts/blogMain.html"
    location_placeholder = "<!--ADD -->"
    text_to_add = f"""
            <article>
                <h3><a href="/BlogPosts/{post_name}">{post_title}</a></h3>
                <p>{description}</p>
            </article>
            {location_placeholder}
            """
    # Update blogMain
    with open(blog_main_path, "r", encoding="utf-8") as blog_main:
        text = blog_main.read()

    with open(blog_main_path, "w", encoding="utf-8") as blog_main:
        new_text = text.replace(location_placeholder, text_to_add)
        blog_main.write(new_text)


if __name__ == "__main__":

    # Files and references
    input_path = sys.argv[1]
    template = "BlogPosts/postTemplate.html"

    # Convert the input file to html
    with open(input_path, "r", encoding="utf-8") as input_file:
        md_text = input_file.read()
    html = markdown.markdown(md_text)

    # Load the template as a string
    with open(template, "r", encoding="utf-8") as template_file:
        template_text = template_file.read()

    # Replace placeholder with the generated html
    output_text = template_text.replace("{ post_content }", html)

    # Save html output_text as a html file
    save_path = input_path.replace("md", "html")
    with open(
        save_path, "w", encoding="utf-8", errors="xmlcharrefreplace"
    ) as output_file:
        output_file.write(output_text)

    # Update the index of the Blogs (blogMain.html)
    title = md_text.split("\n")[0].replace("## ", "")
    add_post_to_index(save_path.split("/")[1], title)
