# coding=gbk


import asyncio
from agents import Runner, trace, set_tracing_disabled


from video_agents.planner import planner_agent
from video_agents.script import script_agent
from video_agents.story_board import storyboard_agent
from video_agents.reviewer import reviewer_agent,ReviewerOutput

set_tracing_disabled(True)

async def generate_video_plan(init_input: str):
    with trace('test'):
        planneroutput=await Runner.run(planner_agent,input=init_input)
        print("1.Planner 完成")
        scriptoutput=await Runner.run(script_agent,input=f"""
【用户原始需求】
{init_input}

【Planner结果】
{planneroutput.final_output.model_dump_json()}
""")
        print("2. Script 完成")
        storyboardoutput=await Runner.run(storyboard_agent,input=scriptoutput.final_output.model_dump_json())
        print("3. Storyboard 完成")
        passed = False
        for i in range(3):
            revieweroutput=await Runner.run(reviewer_agent,input=f"""
【用户原始要求】
{init_input}

【策划】
{planneroutput.final_output.model_dump_json()}

【脚本】
{scriptoutput.final_output.model_dump_json()}

【分镜】
{storyboardoutput.final_output.model_dump_json()}
""")
            print(f"\n===== 第 {i + 1} 次 Reviewer =====")
            print("状态：", revieweroutput.final_output.status)
            print("原因：", revieweroutput.final_output.reason)
            print("修改建议：", revieweroutput.final_output.revision_advice)
            assert isinstance(revieweroutput.final_output,ReviewerOutput)
            if revieweroutput.final_output.status.lower() == 'pass':
                passed = True
                break
            else:

                scriptoutput = await Runner.run(script_agent, input=f"""
【原始策划】
{planneroutput.final_output.model_dump_json()}

【当前脚本】
{scriptoutput.final_output.model_dump_json()}

【Reviewer认为存在的问题】
{revieweroutput.final_output.reason}

【Reviewer修改建议】
{revieweroutput.final_output.revision_advice}

请根据审核意见修改当前脚本。
"""
            )
                storyboardoutput = await Runner.run(storyboard_agent, input=f"""
【修改后的脚本】
{scriptoutput.final_output.model_dump_json()}

【Reviewer认为存在的问题】
{revieweroutput.final_output.reason}

【Reviewer修改建议】
{revieweroutput.final_output.revision_advice}

请根据修改后的脚本重新生成分镜。
""")
                continue
        if passed:
            print("\n===== 审核通过 =====")
        else:
            print("\n===== 已达到最大审核次数，仍未完全通过 =====")

        return (
            scriptoutput.final_output,
            storyboardoutput.final_output,
            revieweroutput.final_output,
        )


async def main():
    init_input=input('请你输入一段提示词')
    final_script, final_storyboard, final_review = await generate_video_plan(init_input)

    print("\n===== 最终脚本 =====")
    print(final_script)

    print("\n===== 最终分镜 =====")
    print(final_storyboard)

    print("\n===== 最终审核结果 =====")
    print(final_review)
if __name__ == "__main__":
    asyncio.run(main())

