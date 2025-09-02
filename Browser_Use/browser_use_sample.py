import gradio as gr
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from browser_use import Agent

load_dotenv()


llm=ChatOpenAI(base_url='https://api.deepseek.com/v1', model='deepseek-chat', api_key="sk-81d695f0638f4520b1360e8b5cf7e94b", use_vision=False)

def run_browser_task(
    task: str,
) -> str:
    try:
        print('task', task)
        agent = Agent(
            task=task,
            llm=llm,
            use_vision=False
        )
        result = agent.run()
        print('final_result()', result.final_result())
        return result
    except Exception as e:
        return f'Error: {str(e)}'


def create_ui():
    with gr.Blocks(title='Browser Use GUI') as interface:
        gr.Markdown('# Browser Use Task Automation')

        with gr.Row():
            with gr.Column():
                task = gr.Textbox(
                    label='Task Description',
                    placeholder='Task 描述',
                    lines=3,
                )
                model = gr.Dropdown(
                    choices=['deepseek-chat'], label='Model', value='deepseek-chat'
                )
                headless = gr.Checkbox(label='Run Headless', value=True)
                submit_btn = gr.Button('Run Task')

            with gr.Column():
                output = gr.Textbox(label='Output', lines=10, interactive=False)

        submit_btn.click(
            fn=lambda task, model, headless: run_browser_task(task),
            inputs=[task, model, headless],
            outputs=output,
        )

    return interface


if __name__ == '__main__':
    demo = create_ui()
    demo.launch()
