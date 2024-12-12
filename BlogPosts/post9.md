## 🤖 Building with AI #08 - Multimodality ⚒️
Modern LLMs (Large Language Models) aren’t limited to just text—they can also "see" images, thanks to multimodality. This capability allows models like OpenAI’s GPT-4 (Vision) to process images alongside text, opening up a world of possibilities, especially when combined with RAG systems.

### 🛠️ How Does IIt Work?
Take OpenAI’s GPT-4 Vision as an example. Implementing multimodality is straightforward:

1. **Write a Prompt:** Define the task you want the model to perform, such as extracting insights from an image or analyzing a chart.
2. **Send the Request:** Use the API to send your prompt along with the image. Local images can be encoded in base64 for upload.
For detailed instructions, OpenAI’s documentation provides a step-by-step guide to setting up Vision capabilities.

### 📚 Use Cases
Traditional extraction or scraping techniques work well when all information is text-based. However, many tasks rely on visuals to convey key insights. Multimodal capabilities let you handle these cases efficiently:

* **Extracting Data from Visual Reports:** Analyze PowerPoint presentations, reports with charts, or image-heavy documents to retrieve meaningful data.
* **Image Classification:** Categorize or tag images based on content, enhancing workflows like  social media analysis.
* **Enriching RAG Systems:** Process images with an LLM, convert the extracted text into usable insights, and store it in your RAG system for future queries.

### 🔧 Things to Keep in Mind
While multimodality is powerful, it comes with limitations:

* **Cost:** Processing images with LLMs can be expensive. For tasks involving large volumes of images, traditional image classification models might be more cost-effective.
* **Image Resolution:** Test the resolution that works best for your task, as higher resolutions can increase costs.
* **Complexity vs. Volume:** Multimodal models shine when tasks are complex (e.g., summarizing a dashboard image) or vary frequently. For repetitive tasks with high volumes, other ML solutions may be more practical.

### 🌟 Conclusion
When used thoughtfully, multimodality is a game-changer for building AI solutions. In a world filled with charts, diagrams, and visual data, giving AI the ability to "see" creates powerful optimization opportunities for businesses. Paired with RAG systems, this capability can unlock new ways to handle and leverage information.

Links:

OpenAI Documentation on Vison: https://platform.openai.com/docs/guides/vision?lang=node

