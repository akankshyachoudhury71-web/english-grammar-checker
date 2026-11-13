import gradio as gr
import language_tool_python

tool = language_tool_python.LanguageTool("en-US")

def check_grammar(text):
    if not text.strip():
        return "Please enter some text."

    mistakes = tool.check(text)
    corrected_text = language_tool_python.utils.correct(
        text, mistakes
    )

    result = "GRAMMAR CHECK RESULTS\n\n"

    if mistakes:
        result += f"Found {len(mistakes)} possible mistake(s).\n\n"

        for i, mistake in enumerate(mistakes, 1):
            result += f"Mistake {i}: {mistake.message}\n"

            if mistake.replacements:
                result += "Suggestions: " + ", ".join(
                    mistake.replacements[:5]
                ) + "\n\n"
    else:
        result += "No grammar mistakes found!\n\n"

    result += "CORRECTED TEXT:\n"
    result += corrected_text

    return result

demo = gr.Interface(
    fn=check_grammar,
    inputs=gr.Textbox(
        lines=5,
        label="Enter your English text"
    ),
    outputs=gr.Textbox(
        lines=12,
        label="Grammar checking results"
    ),
    title="AI-Based English Grammar Checker",
    description="Enter English text to find possible grammar mistakes and get corrections."
)

demo.launch()
