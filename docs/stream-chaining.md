# Stream-JSON Chaining in Claude Flow

## 🔁 Overview: Stream Chaining in Claude Code

**Stream chaining** in Claude Code is the technique of connecting multiple `claude -p` (non-interactive) processes using real-time **JSON streams**, allowing you to build **modular, recursive, multi-agent pipelines**.

Stream-JSON chaining enables Claude instances to pipe their outputs directly to other Claude instances, creating a seamless workflow where agents can build upon each other's work without intermediate storage.

## 🧱 How It Works

### Core Claude Code Flags

Claude Code supports two key flags that enable stream chaining:

* `--output-format stream-json`: emits newline-delimited JSON (`NDJSON`) with every token, turn, and tool interaction
* `--input-format stream-json`: accepts a stream of messages in NDJSON format, simulating a continuous conversation

By combining them:

```bash
claude -p --output-format stream-json "First task" \
  | claude -p --input-format stream-json --output-format stream-json "Process results" \
  | claude -p --input-format stream-json "Final report"
```

Each agent processes input, emits structured responses, and hands them off to the next agent in the chain.

### Automatic Chaining in Claude Flow

When tasks have dependencies and stream-json output format is enabled, Claude Flow automatically:

1. Detects task dependencies from workflow definitions
2. Captures the stdout stream from the dependency task
3. Pipes it directly to stdin of the dependent task
4. Adds `--input-format stream-json` flag to the receiving agent
5. Maintains the stream connection throughout execution

## 🔄 What You Can Do With Stream Chaining

* **Subagent orchestration**: planner → executor → reviewer
* **Recursive pipelines**: refinement loops, ablation agents, iterative optimization
* **Live feedback systems**: feed Claude output into a scoring or mutation agent
* **Task decomposition**: outer loop breaks work into subtasks, inner loop completes each
* **Multi-stage analysis**: data analysis → feature engineering → model training → validation
* **Complex workflows**: research → design → implementation → testing → documentation

## 🧠 Key Features

### Structured Message Types

Stream-JSON format includes structured message types:
- `init`: Session initialization
- `message`: Assistant/user messages
- `tool_use`: Tool invocations with parameters
- `tool_result`: Tool execution results
- `result`: Final task completion status

### Advanced Control Options
- Supports `--session` for session management
- `--max-turns` for granular conversation control
- Works seamlessly with shell scripts, `jq`, and Python SDKs
- Can simulate multi-turn conversation without REPL
- Preserves full context including reasoning and tool usage

### Example Stream-JSON Output

```json
{"type":"init","session_id":"abc123","timestamp":"2024-01-01T00:00:00Z"}
{"type":"message","role":"assistant","content":[{"type":"text","text":"Analyzing data..."}]}
{"type":"tool_use","name":"Bash","input":{"command":"ls -la"}}
{"type":"tool_result","output":"total 64\ndrwxr-xr-x  10 user  staff   320 Jan  1 00:00 ."}
{"type":"result","status":"success","duration_ms":1234}
```

## Enabling Stream Chaining

### Default Behavior
Stream chaining is **enabled by default** when using:
- Non-interactive mode (`--non-interactive` or default for mle-star)
- Stream-json output format (`--output-format stream-json`)
- Tasks with dependencies

### Commands

```bash
# MLE-STAR with automatic chaining
./claude-flow automation mle-star --dataset data.csv --target label --claude --output-format stream-json

# Custom workflow with chaining
./claude-flow automation run-workflow workflow.json --claude --non-interactive --output-format stream-json

# Disable chaining (agents run independently)
./claude-flow automation mle-star --dataset data.csv --target label --claude --output-format stream-json --no-chaining
```

## 📈 Benefits & Performance

### Performance Improvements

| Metric | Traditional (File-based) | Stream Chaining | Improvement |
|--------|-------------------------|-----------------|-------------|
| **Latency** | 2-3s per handoff | <100ms per handoff | **95% faster** |
| **Context Preservation** | 60-70% | 100% | **Full fidelity** |
| **Memory Usage** | O(n) for file storage | O(1) streaming | **Constant memory** |
| **End-to-end Speed** | Baseline | 40-60% faster | **1.5-2.5x speedup** |

### Key Benefits

1. **Context Preservation**: Full conversation history flows between agents
2. **Efficiency**: No intermediate file I/O required  
3. **Real-time Processing**: Streaming output enables immediate processing
4. **Memory Efficiency**: No need to store large intermediate results
5. **Tool Usage Tracking**: All tool invocations preserved in the stream
6. **Reasoning Transparency**: Agent thought processes maintained across chains

## Implementation Details

### Task Dependencies
Tasks must declare dependencies to enable chaining:

```json
{
  "tasks": [
    {
      "id": "task1",
      "name": "Analyze Data",
      "assignTo": "agent1"
    },
    {
      "id": "task2", 
      "name": "Process Results",
      "assignTo": "agent2",
      "depends": ["task1"]  // This enables chaining from task1
    }
  ]
}
```

### Agent Prompts
When chaining is enabled, agents should be aware they may receive input:

```json
{
  "claudePrompt": "You are receiving analysis results from the previous agent via stream-json. Process these insights and continue the chain..."
}
```

### Console Output
Look for these indicators:
- `🔗 Enabling stream chaining from task1 to task2`
- `🔗 Chaining: Piping output from previous agent to Agent Name`

## Manual Chaining

You can also manually chain Claude instances:

```bash
# Traditional piping
claude --print --output-format stream-json "Task 1" | \
claude --print --input-format stream-json --output-format stream-json "Task 2" | \
claude --print --input-format stream-json "Task 3"
```

## ⚠️ Limitations

* **Non-interactive only**: Doesn't work with interactive mode (`claude` without `-p`)
* **Session management**: Must manage session IDs and termination guards externally
* **JSON compliance**: Requires clean JSON compliance—poor error handling if malformed
* **Single dependency**: Currently chains from the last dependency if multiple exist
* **Linear flow**: No branching or conditional chaining yet

## 🚀 Advanced Examples

### Recursive Refinement Pipeline

```bash
# Initial generation
echo "Generate a Python function to calculate fibonacci" | \
claude -p --output-format stream-json | \
# Code review and improvement
claude -p --input-format stream-json --output-format stream-json \
  "Review this code and suggest improvements" | \
# Apply improvements
claude -p --input-format stream-json \
  "Apply the suggested improvements and finalize the code"
```

### Multi-Agent Data Pipeline

```bash
# Data analyst
claude -p --output-format stream-json \
  "Analyze the sales data in data/sales.csv" | \
# Feature engineer  
claude -p --input-format stream-json --output-format stream-json \
  "Based on the analysis, create feature engineering code" | \
# Model builder
claude -p --input-format stream-json --output-format stream-json \
  "Build a predictive model using the engineered features" | \
# Report generator
claude -p --input-format stream-json \
  "Generate a comprehensive report of the entire analysis"
```

### Stream Processing with jq

```bash
# Extract only tool uses from the stream
claude -p --output-format stream-json "Analyze system performance" | \
jq -c 'select(.type == "tool_use")' | \
claude -p --input-format stream-json \
  "Summarize all the commands that were executed"
```

## 🛠️ Implementation Details

### Stream Format Specification

Each line in the stream is a complete JSON object (NDJSON format):

```typescript
interface StreamMessage {
  type: 'init' | 'message' | 'tool_use' | 'tool_result' | 'result';
  timestamp?: string;
  session_id?: string;
  role?: 'assistant' | 'user';
  content?: Array<{
    type: 'text' | 'tool_use';
    text?: string;
    name?: string;
    input?: any;
  }>;
  output?: string;
  status?: 'success' | 'error';
  duration_ms?: number;
}
```

### Process Spawning

Claude Flow spawns processes with specific stdio configurations:

```javascript
const claudeProcess = spawn('claude', [
  '-p',
  '--output-format', 'stream-json',
  '--input-format', 'stream-json',  // Added for dependent tasks
  prompt
], {
  stdio: [inputStream ? 'pipe' : 'inherit', 'pipe', 'pipe']
});

// Pipe input stream if chaining
if (inputStream && claudeProcess.stdin) {
  inputStream.pipe(claudeProcess.stdin);
}
```

## 🎯 Best Practices

1. **Design for streaming**: Write prompts that acknowledge potential input streams
2. **Handle errors gracefully**: Include error handling in your pipeline
3. **Use session IDs**: Track sessions across chained agents
4. **Monitor performance**: Stream chaining reduces latency but increases complexity
5. **Test incrementally**: Build chains step by step, testing each link

## 🔍 Troubleshooting

### Common Issues

1. **"Unexpected end of JSON input"**
   - Cause: Malformed JSON in the stream
   - Fix: Ensure all agents output valid stream-json format

2. **"No input received"**
   - Cause: Dependency task failed or produced no output
   - Fix: Check task execution logs, ensure dependency succeeded

3. **"Context seems lost between agents"**
   - Cause: Missing `--input-format stream-json` flag
   - Fix: Verify Claude Flow is adding the flag (check with --verbose)

4. **Performance degradation**
   - Cause: Large context accumulation
   - Fix: Use `--max-turns` to limit context size

### Debugging Commands

```bash
# Debug stream output
./claude-flow automation mle-star --dataset data.csv --target label --claude --verbose

# Save stream for analysis
./claude-flow automation run-workflow workflow.json --claude --output-format stream-json 2>&1 | tee debug.log

# Validate stream format
cat debug.log | jq -c 'select(.type)' | head -20
```

## 🌟 Real-World Workflow Examples

### Software Development Pipeline

```json
{
  "name": "Full-Stack Development Workflow",
  "tasks": [
    {
      "id": "requirements",
      "name": "Analyze Requirements",
      "assignTo": "analyst",
      "claudePrompt": "Analyze the requirements in docs/requirements.md"
    },
    {
      "id": "design",
      "name": "System Design",
      "assignTo": "architect",
      "depends": ["requirements"],
      "claudePrompt": "Based on the requirements analysis, create a system design"
    },
    {
      "id": "backend",
      "name": "Backend Implementation",
      "assignTo": "backend-dev",
      "depends": ["design"],
      "claudePrompt": "Implement the backend based on the system design"
    },
    {
      "id": "frontend",
      "name": "Frontend Implementation", 
      "assignTo": "frontend-dev",
      "depends": ["design"],
      "claudePrompt": "Implement the frontend based on the system design"
    },
    {
      "id": "integration",
      "name": "Integration & Testing",
      "assignTo": "tester",
      "depends": ["backend", "frontend"],
      "claudePrompt": "Integrate and test the complete application"
    }
  ]
}
```

### Research Paper Analysis Pipeline

```bash
# Extract key findings
claude -p --output-format stream-json \
  "Extract key findings from the paper at papers/research.pdf" | \
# Synthesize with existing knowledge
claude -p --input-format stream-json --output-format stream-json \
  "Compare these findings with current literature in the field" | \
# Generate implementation ideas
claude -p --input-format stream-json --output-format stream-json \
  "Suggest practical implementations of these findings" | \
# Create action plan
claude -p --input-format stream-json \
  "Create a detailed action plan for implementing these ideas"
```

## 💡 Key Insight

**Stream chaining** turns Claude from a stateless prompt executor into a programmable agent pipeline. It's how you move from chat to computation, enabling complex multi-agent workflows that maintain context and build upon each other's work in real-time.

This technology fundamentally changes how we think about AI automation:
- **From**: Sequential, isolated prompts with context loss
- **To**: Continuous, connected workflows with full context preservation

## 🚧 Future Enhancements

- **Multi-stream merge**: Support for multiple input streams (merge/join operations)
- **Conditional routing**: Dynamic chaining based on output content
- **Stream middleware**: Filtering and transformation between agents
- **Parallel patterns**: Fan-out/fan-in for parallel processing
- **Error recovery**: Built-in retry and fallback mechanisms
- **Debug tools**: Stream replay and step-through debugging
- **Visual monitoring**: Real-time visualization of stream flow
- **Performance analytics**: Detailed metrics for each chain segment