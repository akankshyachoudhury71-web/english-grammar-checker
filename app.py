import gradio as gr
import requests
import os

API_URL = "https://api.languagetool.org/v2/check"

def check_grammar(text):
    if not text.strip():
        return "Please enter some text."

    try:
        response = requests.post(
            API_URL,
            data={
                "text": text,
                "language": "en-US"
            },
            timeout=30
        )

        response.raise_for_status()
        data = response.json()

        mistakes = data.get("matches", [])

        result = "GRAMMAR CHECK RESULTS\n\n"

        if mistakes:
            result += f"Found {len(mistakes)} possible mistake(s).\n\n"

            for i, mistake in enumerate(mistakes, 1):
                result += f"Mistake {i}: {mistake['message']}\n"

                replacements = mistake.get("replacements", [])

                if replacements:
                    suggestions = [
                        item["value"] for item in replacements[:5]
                    ]
                    result += "Suggestions: " + ", ".join(
                        suggestions
                    ) + "\n"

                result += "\n"

            corrected_text = text

            for mistake in sorted(
                mistakes,
                key=lambda item: item["offset"],
                reverse=True
            ):
                replacements = mistake.get("replacements", [])

                if replacements:
                    start = mistake["offset"]
                    end = start + mistake["length"]
                    corrected_text = (
                        corrected_text[:start]
                        + replacements[0]["value"]
                        + corrected_text[end:]
                    )

        else:
            result += "No grammar mistakes found!\n\n"
            corrected_text = text

        result += "CORRECTED TEXT:\n"
        result += corrected_text

        return result

    except requests.RequestException as error:
        return f"Grammar checking service error: {error}"

    except Exception as error:
        return f"Unexpected error: {error}"


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

demo.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", "10000"))
)
