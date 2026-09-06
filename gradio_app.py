import gradio as gr

from main import generate_video_plan


async def generate_from_web(
    topic: str,
    target_audience: str,
    duration: str,
    style: str,
):
    init_input = f"""
【视频主题】
{topic}

【目标受众】
{target_audience}

【视频时长】
{duration}

【视频风格或补充要求】
{style}
""".strip()

    final_script, final_storyboard, final_review = await generate_video_plan(init_input)

    return (
        final_script.model_dump(),
        final_storyboard.model_dump(),
        final_review.model_dump(),
    )


with gr.Blocks(title="短视频 Agent") as demo:
    gr.Markdown("# 短视频 Agent")

    topic = gr.Textbox(
        label="视频主题",
        placeholder="例如：用简单语言介绍人工智能",
        lines=3,
    )
    target_audience = gr.Textbox(
        label="目标受众",
        placeholder="例如：对人工智能感兴趣的普通用户",
    )
    duration = gr.Textbox(
        label="视频时长",
        placeholder="例如：60 秒",
    )
    style = gr.Textbox(
        label="视频风格或补充要求",
        placeholder="例如：轻松、口语化、节奏紧凑",
        lines=2,
    )

    submit_button = gr.Button("生成短视频方案", variant="primary")

    final_script = gr.JSON(label="最终 Script")
    final_storyboard = gr.JSON(label="最终 Storyboard")
    final_review = gr.JSON(label="Reviewer 最终审核结果")

    submit_button.click(
        fn=generate_from_web,
        inputs=[topic, target_audience, duration, style],
        outputs=[final_script, final_storyboard, final_review],
    )


if __name__ == "__main__":
    demo.launch()
