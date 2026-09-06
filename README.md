# Short Video Agent

一个面向短视频创作的多智能体编排原型。

项目将短视频创作拆分为策划、脚本生成、分镜生成和审核等任务，并通过多个 Agent 串联成完整 Workflow。

目前主要用于实践：

- Multi-Agent Workflow
- Structured Output
- Tool Calling
- Reviewer Feedback Loop
- Gradio Web UI

## Workflow

```text
User Request
      ↓
Planner Agent
      ↓
Script Agent
      ↓
Storyboard Agent
      ↓
Reviewer Agent
      ↓
   PASS / REVISE
      ↓
Final Output
```

如果 Reviewer 判断需要修改：

```text
Reviewer
   ↓
Script Agent
   ↓
Storyboard Agent
   ↓
Reviewer
```

最多进行三轮审核。

## Agents

### Planner Agent

根据用户需求生成：

- 目标受众
- 核心信息
- 开头 Hook
- 内容结构

### Script Agent

根据 Planner 的策划结果生成短视频脚本。

### Storyboard Agent

把脚本进一步转换成分镜，包括画面、旁白和镜头时长等信息。

### Reviewer Agent

综合检查：

- 用户原始需求
- 策划结果
- 脚本
- 分镜

输出审核状态和修改建议。

## Data Flow

Agent 之间主要通过 Pydantic 结构化输出传递数据。

例如：

```text
PlannerOutput
    ↓
JSON
    ↓
Script Agent
    ↓
ScriptOutput
    ↓
JSON
    ↓
Storyboard Agent
```

这样可以减少不同 Agent 之间输出格式不稳定的问题。

## Tool Calling

Reviewer 可以调用 Python Tool 对生成内容进行辅助检查。

目前实现了简单的视频时长估算功能，用于辅助判断脚本长度是否符合目标视频时长。

## Web UI

项目使用 Gradio 提供简单网页界面。

用户可以输入短视频需求并运行完整 Agent Workflow。

## Project Structure

```text
short_video_agent/
├── main.py
├── gradio_app.py
├── requirements.txt
├── video_agents/
│   ├── planner.py
│   ├── script.py
│   ├── story_board.py
│   ├── reviewer.py
│   └── model_config.py
└── tools/
    └── duration.py
```

## Run

安装依赖：

```bash
pip install -r requirements.txt
```

配置模型 API Key 后运行：

```bash
python gradio_app.py
```
